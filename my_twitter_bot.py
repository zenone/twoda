#!/usr/bin/env python
# coding=utf-8
#
# This script will generate tweets using a Markcov Chain
# and will post the tweets to Twitter.
#
# Twitter API Documentation
#  - https://dev.twitter.com/oauth
#  - https://dev.twitter.com/rest/reference/post/statuses/update
#  - https://dev.twitter.com/rest/public/uploading-media
#  - https://dev.twitter.com/rest/reference/get/trends/place
#
# Twitter Terms of Service
#  - https://twitter.com/tos
#
# Giphy API Documentation
#  - https://github.com/giphy/GiphyAPI
#
# Github Repository:
#  - https://github.com/zenone/twoda
#
# Written by Zenone on 2015-10-06


"""Usage:
    my_twitter_bot.py
    my_twitter_bot.py -s <hours>
    my_twitter_bot.py -i
    my_twitter_bot.py -i -s <hours>
    my_twitter_bot.py -h | --help
    my_twitter_bot.py --version

Options:
    -i            Download a relevant image from Giphy and tweet it
    -s            Sleep before executing
    -h --help     Show this help information
    --version     Show version

Arguments:
    hours         Number of hours to sleep
"""


# Local libraries
from random import randint
from time import sleep

# Third party libraries
from docopt import docopt

# Local libraries
from classes.twoda import Twoda


#############################
# CONFIGURATION INFORMATION #
#############################
config_file_path = "/changeme/"
config_filename = "config.txt"
geolocation = True
#############################

# Script version
_VERSION = "1.0"


def delay(seconds):
    """
    This function waits a random amount of time before generating and
    posting a tweet
    :param seconds:  Number of seconds to pick a random time from
    """

    time_to_sleep = randint(1, seconds)
    print("[*] Sleeping {} seconds...".format(time_to_sleep))
    sleep(time_to_sleep)


def display_results(response_json):
    """
    Display the tweet URL and geolocation of the tweet
    :param response:  The requests response from Twitter
    """

    # Display some additional information regarding the tweet
    tweet_id = response_json['id']
    if 'screen_name' in response_json:
        screen_name = response_json['screen_name'].encode('utf-8')
    else:
        screen_name = response_json['user']['screen_name'].encode('utf-8')

    # Display tweet URL
    print("[+] Tweet URL: https://twitter.com/{}/status/{}".format(screen_name, tweet_id))

    # Display geolocation
    if response_json['place']:
        if response_json['place']['full_name']:
            location = response_json['place']['full_name'].encode('utf-8')
            print("[+] Location: {}".format(location))


def run(tweet_image):
    """
    This function that performs the magic
    :param tweet_image:  If True, this script will tweet an image
    """

    # Set things up
    media_id = None
    tw = Twoda(config_file_path, config_filename)

    if tweet_image:
        # Get image from Giphy
        print("[*] Getting animated GIF from Giphy...")
        img = tw.get_animated_gif()
        print("[+] Giphy search terms used: {}".format(" ".join(img['search_terms'])))
        print("[+] Source image URL: {}".format(img['url']))

        # Upload image to Twitter
        print("[*] Uploading animated GIF to Twitter...")
        media = tw.upload_image(img['image'])
        media_id = media['media_id']
        print("[+] Media ID: {}".format(media_id))
        twt = tw.generate_hashtags()
        tweet = " ".join(twt['hashtags'])

    else:
        # Generate Tweet verbiage
        twt = tw.generate_tweet()
        tweet = twt['tweet']

    # Post tweet to Twitter
    print("[+] Generated tweet: {}".format(tweet))
    print("[*] Posting tweet to Twitter...")
    results = tw.post_tweet(tweet=tweet, media_id=media_id, geolocation=geolocation)

    # Print status of the tweet
    if results['status_code'] == 200:
        print("[+] Tweet posted successfully")
        display_results(results['response'])
    else:
        print("[-] Tweet post failed")


def main():
    """
    Parse the arguments first
    """
    arguments = docopt(__doc__, version=_VERSION)
    if arguments['-s']:
        hours = int(arguments['<hours>'])
        minutes = hours * 60
        seconds = minutes * 60
        delay(seconds)
    if arguments['-i']:
        tweet_image = True
    else:
        tweet_image = False
    run(tweet_image)


if __name__ == '__main__':
    main()
