# Notes: You must have a Twitter 

# For sending GET requests from the API
import requests

# For saving access tokens and for file management when creating and adding to the dataset
import os

# For dealing with json responses we receive from the API
import json

# For displaying the data after
import pandas as pd

# For saving the response data in CSV format
import csv

# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata

#To add wait time between requests
import time

from requests.models import Response

# In the terminal, export BEARER_TOKEN='<Your Bearer Token>'
bearer_token = os.environ.get('BEARER_TOKEN')

# Create auth() function to retrieve the token from the environment
def auth():
  return os.getenv('BEARER_TOKEN')

# Create Headers
def create_headers(bearer_token):
  headers = { 'Authorization': f'Bearer {bearer_token}' }
  return headers


# Create URL
def create_url(keyword, start_date, end_date, max_results = 10):
    search_url = 'https://api.twitter.com/2/tweets/search/recent' 

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields':'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields':'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields':'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}

    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token  # params object received from create_url function
    response = requests.request('GET', url, headers=headers, params=params)
    print(f'Endpoint Response Code: {str(response.status_code)}')
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()

# Inputs for the request

bearer_token = auth()
headers = create_headers(bearer_token)
keyword = 'xbox lang:en'
start_time = '2021-12-29T00:00:00.000Z'  # Change this to be today - 7 days
end_time = '2022-01-02T00:00:00.000Z' # change this to be now - 10 seconds
max_results = 15

url = create_url(keyword, start_time, end_time, max_results)
json_response = connect_to_endpoint(url[0], headers, url[1])

#data = json_response

#print(json.dumps(json_response, indent=4, sort_keys=True))

# Save Results to a JSON file
with open('data.json', 'w') as output_file:
  json.dump(json_response, output_file)


# Save Results to CSV
# Approach A: (Simple Approach)
df = pd.DataFrame(json_response['data'])
df.to_csv('dataA.csv')

# Approach B: (Custom Approach)
# Create file
csvFile = open("dataB.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

#Create headers for the data you want to save, in this example, we only want save these columns in our dataset
csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
csvFile.close()

def append_to_csv(json_response, fileName):
    counter = 0

    # Open Or create the target CSV file
    csvFile = open('data.csv', 'a', newline='', encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    # Loop through each tweet
    for tweet in json_response['data']:
        # Create a variable for each field since some of the keys might not exist 
        # for some tweets.

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Geolocation
        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else: 
            geo = " "

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. Source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']

        # Assemble all data in a list
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, 
                reply_count, retweet_count, source, text]

        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print(f'# of Tweets added from this response: {counter}')


append_to_csv(json_response, 'dataB.csv')