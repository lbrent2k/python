# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q apple -d data
# 
# It will produce the list of tweets for the query "apple" 
# in the file data/stream_apple.json



import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import os


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='fired,job,laid off,pink slip')          ######
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory",
                        default='data')                     #####
    return parser
    
class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query):
        global query_fname                                       ####
        query_fname = format_filename(query)
         
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)
        self.outfile  = "%s/stream_%s_%s.json" % (data_dir, query_fname ,file_counter )  #####
        print(self.outfile)
        
    def on_data(self, data):
        global file_counter                                        ####    
        global query_fname                                         ####
        try:
            with open(self.outfile, 'a') as f:
                print(data)   
                f.write(data)
                
            statinfo = os.stat(self.outfile)     ### get filesize from system
            sz = statinfo.st_size                ###
            
            if sz > 500000:                      ### This is the file size
                print("flipping files")          ###
                time.sleep(30)                   ### Pause before deleting file
                os.remove(self.outfile)          ###
                file_counter = file_counter +1   ###
                self.outfile = "%s/stream_%s_%s.json" % ("data", query_fname ,file_counter )  ##### Names new file
                
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    file_counter= 10                             ### starting number for the file names
    

    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    twitter_stream.filter(track=[args.query])
