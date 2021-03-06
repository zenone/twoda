Twoda
=====
Twoda is a play on the words, *Twitter* and *Yoda*.

So, what is Twoda?

Twoda generates, and posts, amusing tweets using a Markcov Chain. Twoda can also tweet animated GIFs from Giphy that pertain to the general theme you've setup.

On 2015-10-04 I wrote a blog post titled, "[The Force Awakens ... on Twitter](http://blog.zenone.org/2015/10/the-force-awakens-on-twitter.html)". The post describes how I used Markov Chains to generate tweets that blended quotes from Yoda with the wisdom of various Zen masters. It all began as a Saturday morning, "Hmmmm... I should try this." The result; the code in this repository, called Twoda, that I quickly creatd ... and the resulting [@YodaUncut](https://twitter.com/yodauncut) parody account.

> Please review [Twitter's Terms of Service](https://twitter.com/tos) before using Twoda. 
> 
> Twoda is like Burger King, "*have it your way, but don't go crazy*".
> Do *not* abuse this with Twitter.

Twoda was created with the following criteria:

  1. Generate tweet, using a Markov Chain, that blends two different sources of quotes. For example, [@YodaUncut](https://twitter.com/yodauncut)  blends the wisdom of Yoda with the koans of various Zen masters
  2. Ensure that the generated tweet is 140 characters, or less, in length, to meet Twitter's requirements
  3. Create random coordinates (latitude and longitude in North America) that can be added to the tweet for geolocation
  4. Post the tweet on Twitter 

Additional after-the-fact features:

  1. Option to replace tweet with relevant hashtags and an animated GIF, downloaded from Giphy [the `-i` option]
  2. Option to delay the posting of the tweet by a randomly selected period of time given a time range, in hours, provided [the `-s <hours>`  option]
  3. If tweeted successfully, display the tweet URL and geolocation, if provided

Requirements
===========
 - `docopt`
 - `oauthlib`
 - `requests`
 - `requests-oauthlib`

If you get an "InsecurePlatformWarning" message, you'll also want to add:

 - `requests[security]`

Note: "`requests[security]`" might also require you to do: "`sudo apt-get install python-dev libffi-dev libssl-dev`"

Configuration
===========
In the subdirectory `data/` is a file called `config.txt`. The items in the config file are in key:value format, meaning, don't change what's on the left side of the colon ('`:`'). Only change what's on the right side. For example, the default config.txt contains the following:

    default_hashtag:#<PUT_A_DEFAULT_HASHTAG_HERE>
    default_image_search:<PUT_AN_IMAGE_SEARCH_TERM_HERE>
    giphy_api_key:<PUT_GIPHY_API_HERE>
    hashtags_file:hashtags.txt
    quotes_file1:quotes_file1.txt
    quotes_file2:quotes_file2.txt
    twitter_client_key:<PUT_YOUR_TWITTER_CLIENT_KEY_HERE>
    twitter_client_secret:<PUT_YOUR_TWITTER_CLIENT_SECRET_HERE>
    twitter_token:<PUT_YOUR_TWITTER_TOKEN_HERE>
    twitter_token_secret:<PUT_YOUR_TWITTER_TOKEN_SECRET_HERE>

You'll want to change replace everything in between the `<` and `>` symbols, including the symbols. For example:

    default_hashtag:#MickeyMouse  
    default_image_search:disney

...and so on.

You will also need to edit a few lines in my_twitter_bot.py:

    #############################
    # CONFIGURATION INFORMATION #
    #############################
    config_file_path = "/path/to/your/config.txt/and/quote_n_hashtags_files/"
    config_filename = "config.txt"
    geolocation=True
    #############################

Change `config_file_path` to point to the path where your config.txt, quotes files, and hashtags.txt file are located. You'll probably want to leave `config_filename` alone.  As for `geolocation`;  set it to *True* if you want random coordinates (latitude and longitude in North America) used for your tweets. Set it to `False` if you don't.

Usage
=====

    $ ./my_twitter_bot.py --help
    Usage:
        my_twitter_bot.py
        my_twitter_bot.py -s <hours>
        my_twitter_bot.py -i
        my_twitter_bot.py -i -s <hours>
        my_twitter_bot.py -h | --help
        my_twitter_bot.py --version
    
    Options:
        -s            Sleep before executing
        -h --help     Show this help information
        --version     Show version
    
    Arguments:
        hours         Number of hours to sleep

Below are example cron entries showing how the `-s` option can be used to have tweets posted randomly throughout the day.

Scheduling
=========
The first cron entry example will post a tweet at a random time every five hours:

    0 */5 * * * /path/to/python  /apps/twoda/my_twitter_bot.py -s 5

The next cron entry example will post a tweet with an image and hashtags at a random time every 20 hours:

    0 */20 * * * /path/to/python  /apps/twoda/my_twitter_bot.py -i -s 20

----------

Twitter API Documentation
======================
 - https://dev.twitter.com/oauth
 - https://dev.twitter.com/rest/reference/post/statuses/update
 - https://dev.twitter.com/rest/public/uploading-media
 - https://dev.twitter.com/rest/reference/get/trends/place

Twitter Terms of Service
====================
 - https://twitter.com/tos

Giphy API Documentation
=====================
 - https://github.com/giphy/GiphyAPI