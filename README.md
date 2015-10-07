Twoda
=====
Twoda is a play on the words, *Twitter* and *Yoda*.

So, what exactly is Twoda?

I wrote a blog post titled, "[The Force Awakens ... on Twitter](http://blog.zenone.org/2015/10/the-force-awakens-on-twitter.html)". The post describes how I was used Markov Chains to generate tweets that blended quotes from Yoda with the wisdom of various Zen masters. It all began as a Saturday morning, "Hmmmm... I should try this." The result; the code in this repository, called Twoda, and the resulting [@YodaUncut](https://twitter.com/yodauncut) parody account.

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
    user-agent:Twoda v1.0

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

----------

Twitter API Documentation
======================
 - https://dev.twitter.com/oauth
 - https://dev.twitter.com/rest/reference/post/statuses/update
 - https://dev.twitter.com/rest/public/uploading-media
 - https://dev.twitter.com/rest/reference/get/trends/place

Giphy API Documentation
=====================
 - https://github.com/giphy/GiphyAPI