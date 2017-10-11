# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:02:09 2017

@author: Trace
"""

import json
import time
import webbrowser
import pandas as pd
from pandas.io.json import json_normalize
from rauth import OAuth1Service
from rauth.utils import parse_utf8_qsl

credentials_file = open('oath.json')
credentials = json.load(credentials_file)
credentials_file.close()

oauth = OAuth1Service(consumer_key=credentials['consumer_key'],
                      consumer_secret=credentials['consumer_secret'],
                      name='yahoo',
                      request_token_url='https://api.login.yahoo.com/oauth/v2/get_request_token',
                      access_token_url='https://api.login.yahoo.com/oauth/v2/get_token',
                      authorize_url='https://api.login.yahoo.com/oauth/v2/request_auth',
                      base_url='http://fantasysports.yahooapis.com')

request_token, request_token_secret = oauth.get_request_token(params={'oauth_callback': 'oob'})

authorize_url = oauth.get_authorize_url(request_token)
webbrowser.open(authorize_url)
verify = input('Enter code: ')

raw_access = oauth.get_raw_access_token(request_token, request_token_secret, params={'oauth_verifier': verify})
parsed_access_token = parse_utf8_qsl(raw_access.content)
access_token = (parsed_access_token['oauth_token'], parsed_access_token['oauth_token_secret'])

start_time = time.time()
end_time = start_time + 3600

credentials['access_token'] = parsed_access_token['oauth_token']
credentials['access_token_secret'] = parsed_access_token['oauth_token_secret']
tokens = (credentials['access_token'], credentials['access_token_secret'])

s = oauth.get_session(tokens)

url = 'http://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.694463'
r = s.get(url, params={'format': 'json'})
r.status_code
r.json()