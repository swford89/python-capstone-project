# Python-Programming-Capstone-Project

## Project-Goals
- Working with APIs to get and assess data
- Store information in a Database (MySQL)

## Analyzing the tone of tweets
This project uses the tweepy module to get tweets and the Tone Analyzer from IBMs watson module to analyze the tone of the tweets

## API-Documentation
- [IBM Cloud Creating Resources](https://cloud.ibm.com/docs/account?topic=account-manage_resource)
- [IBM Tone Analyzer](https://cloud.ibm.com/apidocs/tone-analyzer?code=python#tone)
- [Tweepy](https://docs.tweepy.org/en/v3.10.0/install.html)

 **You need to create the cloud resource and use the credentials that are generated upon creation (API key and endpoint URL) first, on your IBM cloud account**

**If you just generate an API key and use that in your script, without creating the resource, you'll get a `403: Forbidden` error**

## Overview

### config_db.py 
- contains function for creating a connection the the database you've created and want to save your information to

### config_twitter.py
- contains function for creating the twitter API object, which will be used to search for tweets

### config_tone.py
- contains function for creating API client and endpoint
- contains function for analyzing the tone of the tweets which we will pass into it

### tweets_db.py
- the main script where everything happens
- asks user for the word/topic they would like to query
- asks user for the number of tweets they would like returned
- runs query and gets tweets
- tweets are processed, analyzed, and then entered into the DB
- TONE ANALYZER: Lite Plan = 2500 API calls/month
- TWITTER API: [Rate Limit Doc](https://developer.twitter.com/en/docs/twitter-api/rate-limits)