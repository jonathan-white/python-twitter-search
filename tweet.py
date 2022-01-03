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

# In the terminal, export BEARER_TOKEN='<Your Bearer Token>'
bearer_token = os.environ.get("BEARER_TOKEN")

# Create auth() function to retrieve the token from the environment
def auth():
  return os.getenv('BEARER_TOKEN')

# Create Headers
def create_headers(bearer_token):
  headers = { 'Authorization': f'Bearer {bearer_token}' }
  return headers


# Create URL
def create_url(keyword, start_date, end_date, max_results = 10):
  search_url = "https://api.twitter.com/2/tweets/search/recent" 

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
  response = requests.request("GET", url, headers=headers, params=params)
  print(f'Endpoint Response Code: {str(response.status_code)}')
  if response.status_code != 200:
    raise Exception(response.status_code, response.text)

  return response.json()

# Inputs for the request

bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "xbox lang:en"
start_time = "2021-12-29T00:00:00.000Z"  # Change this to be today - 7 days
end_time = "2022-01-02T00:00:00.000Z" # change this to be now - 10 seconds
max_results = 15

url = create_url(keyword, start_time, end_time, max_results)
json_response = connect_to_endpoint(url[0], headers, url[1])

print(json.dumps(json_response, indent=4, sort_keys=True))

