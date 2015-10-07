# coding=utf-8
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
# Written by Steve Zenone on 2015-10-06


"""
Python module to generate and upload content to Twitter for parody accounts
"""


# Local imports
import base64
import shutil
import urllib
from random import choice, randint
from StringIO import StringIO


# Third party imports
import requests
from requests_oauthlib import OAuth1


# Base URL for Twitter calls
base_twitter_url = "https://api.twitter.com/1.1/"
base_twitter_media_url = "https://upload.twitter.com/1.1/"

# Base URL for Giphy
base_giphy_url = "https://api.giphy.com/v1/gifs/search"

# user-agent
user_agent = "Twoda v1.0"


class Twoda(object):
    """
    This class object will read in the config file and setup
    oauth for Twitter
    :param base_path:  The absolute path of your config file
    :param config_file:  The filename of your config file
    """

    def __init__(self, base_path, config_file):
        f = open(base_path + config_file, 'rb')
        raw_config = f.readlines()
        f.close()
        configs = {}
        for config in raw_config:
            key = config.split(':')[0]
            value = config.split(':')[1].strip('\n')
            configs[key] = value
        client_key = configs['twitter_client_key']
        client_secret = configs['twitter_client_secret']
        token = configs['twitter_token']
        token_secret = configs['twitter_token_secret']
        self.default_hashtag = configs['default_hashtag']
        self.default_image_search = configs['default_image_search']
        self.giphy_api_key = configs['giphy_api_key']
        self.hashtags_file = base_path + configs['hashtags_file']
        self.quotes_file1 = base_path + configs['quotes_file1']
        self.quotes_file2 = base_path + configs['quotes_file2']
        self.user_agent = {'user-agent': user_agent}
        self.oauth = OAuth1(client_key, client_secret, token, token_secret)

    def generate_tweet(self):
        """
        This function orchestrates the creation of the tweet
        :return:  Retunrs the tweet as a string
        """

        quotes_list = []
        for filename in [self.quotes_file1, self.quotes_file2]:
            f = open(filename, 'rb')
            quotes = f.readlines()
            f.close()
            for quote in quotes:
                quotes_list.append(quote.strip('\n'))
        quotes = " ".join(quotes_list)
        markcov_dict = Twoda.create_markcov_dict(quotes)
        tweet = Twoda.create_markcov_tweet(markcov_dict)
        return tweet

    def post_tweet(self, tweet, media_id=None, geolocation=False):
        """
        This function posts the tweet to Twitter
        :param geolocation:  True = post coordinates, False = don't
        :param tweet:  The tweet to post
        :param media_id:  ID number of media [optional]
        :param tweet:  The text to tweet
        :return:  Return the response from requests.post()
        """

        # Make the URL
        api_url = "{}statuses/update.json".format(base_twitter_url)
        api_url += "?status={}".format(urllib.quote(tweet, safe=''))
        if geolocation:
            coordinates = Twoda.get_geolocation()
            api_url += "&lat={}&long={}".format(coordinates['lat'], coordinates['long'])
            api_url += "&display_coordinates=true"
        if media_id:
            api_url += "&media_ids={}".format(media_id)

        # tweet
        response = requests.post(api_url, headers=self.user_agent, auth=self.oauth)
        return response

    def generate_hashtags(self, count=3):
        """
        This function generates relevant hashtags for image tweets
        :param count:
        :return:
        """
        f = open(self.hashtags_file, 'rb')
        hashtags = f.read().splitlines()
        f.close()
        results = []
        for i in xrange(0, count):
            random_hashtag = choice(hashtags)
            results.append("#" + random_hashtag.title().replace(' ', ''))
            hashtags.remove(random_hashtag)
        results.append(self.default_hashtag)
        return " ".join(results)

    def get_animated_gif(self):
        """
        This will download an relevant image from giphy
        :return:
        """

        # Build Giphy search term
        f = open(self.hashtags_file, 'rb')
        hashtags = f.read().splitlines()
        f.close()
        random_hashtag = choice(hashtags)
        search_terms = [self.default_image_search, random_hashtag.title()]

        # Make the URL
        api_url = base_giphy_url
        api_url += "?api_key={}".format(self.giphy_api_key)
        api_url += "&q={}".format(" ".join(search_terms))

        # Query Giphy and get random URL of a relevant image
        response = requests.get(api_url, headers=self.user_agent)
        response_json = response.json()
        images = []
        for result in response_json['data']:
            images.append(result['images']['original']['url'])
        random_image_url = choice(images)

        # Download image
        r = requests.get(random_image_url, headers=self.user_agent, timeout=5, stream=True)
        r.raw.decode_content = True
        buf = StringIO()
        shutil.copyfileobj(r.raw, buf)
        return buf

    def upload_image(self, image):
        """
        This function posts the image from Giphy to Twitter
        :param image:  The raw data of the image to upload
        :return:  Return the response from requests.post()
        """

        # Make the URL
        api_url = "{}media/upload.json".format(base_twitter_media_url)
        payload = {'media_data': base64.b64encode(image.getvalue())}
        payload = urllib.urlencode(payload)

        # Upload to Twitter
        response = requests.post(api_url, headers=self.user_agent, auth=self.oauth, data=payload)
        return response.json()['media_id']

    def get_trending(self, woeid=2458410):
        """
        This function will get the latest trending items on twitter
        :param woeid:  1 = global, "2458410" = United States
        :return:  Returns a list with the latest trending hashtags
        """

        # Make the URL
        api_url = "{}trends/place.json".format(base_twitter_url)
        api_url += "?id={}".format(woeid)  # Using 1 as WOEID gets global information

        response = requests.get(api_url, headers=self.user_agent, auth=self.oauth)

        trending_hashtags = []
        if response.status_code == 200:
            response_json = response.json()
            trends = response_json[0]['trends']
            for x in trends:
                trend = x['name']
                if trend.startswith('#'):
                    trending_hashtags.append(trend.encode('utf-8'))
        else:
            trending_hashtags.append('#starwars')
        return trending_hashtags

    @staticmethod
    def get_geolocation():
        """
        This function generates a random latitude and longitude, somwhere
        in Northern America.
        :return:  Returns a dict with the lat and long
        """

        latitude = "{}.{:07d}".format(randint(28, 69), randint(0, 999999))
        longitude = "{}.{:07d}".format(randint(-128, -64), randint(0, 999999))
        return {'lat': latitude, 'long': longitude}

    @staticmethod
    def create_markcov_dict(original_text):
        """
        This function takes the quotes and creates a dictionary with the words
        in Markcov chunks
        :param original_text:  The plaintext to chunck up
        :return:  Return the dictionary with Markcov chunks
        """

        original_text = original_text
        split_text = original_text.split()
        markcov_dict = {}
        for i in xrange(len(split_text) - 2):
            key_name = (split_text[i], split_text[i + 1])
            key_value = split_text[i + 2]
            if key_name in markcov_dict:
                markcov_dict[key_name].append(key_value)
            else:
                markcov_dict[key_name] = [key_value]
        return markcov_dict

    @staticmethod
    def create_markcov_tweet(markcov_dict):
        """
        This function creates the Tweet using the Markov Chain
        :param markcov_dict:  The dictionary with the text in Markcov chunks
        :return:  Return the tweet
        """

        # Pick a random starting point
        selected_words_tuple = choice(markcov_dict.keys())
        markcov_tweet = [selected_words_tuple[0].capitalize(), selected_words_tuple[1]]

        # Generate the Markcov text, ending the Markcov text when we create a "key" that doesn't exist
        while selected_words_tuple in markcov_dict:
            next_word = choice(markcov_dict[selected_words_tuple])
            if len(" ".join(markcov_tweet) + " " + next_word) < 140:
                if (markcov_tweet[-1]).endswith('.'):
                    markcov_tweet.append(next_word.capitalize())
                else:
                    markcov_tweet.append(next_word)
                selected_words_tuple = (selected_words_tuple[1], next_word)
            else:
                tweet = " ".join(markcov_tweet).strip()
                if tweet.endswith(","):
                    tweet = tweet.rstrip(',') + '.'
                elif not (tweet.endswith(".") or
                          tweet.endswith("!") or
                          tweet.endswith("?") or
                          tweet.endswith(";") or
                          tweet.endswith(":")):
                    tweet += '.'
                return tweet
