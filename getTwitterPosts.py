#getTwitterPosts
# Hit Twitter API and Load to DB

import json
import sqlite3
import pandas as pd
# load my custom object
from connect2twitter import *

# get list of ballers:
with open('ballers.txt', 'r') as f:
    ballers = [l.strip() for l in f.readlines()]

# get twitter accounts
accts = pd.read_csv('player_twitter_accts.csv', names=['player', 'username'])
accts = accts[accts.player.isin(ballers)]
print(accts.shape)

# Doing the data load in chunks so skipping those who have already been uploaded.
dbname = "nbaSocial.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('select distinct player_name from twitter_users')
skip = [c[0] for c in cur.fetchall() if c[0]]
print(skip)
conn.close()

# load credentials
with open('creds/twitterCreds.json','r') as f:
    creds = json.load(f)

creds
# instantiate custom object
twitter = twitterObj(dbname, **creds)

if ('access_token' not in creds) or ('secret_token' not in creds):
    creds['access_token'] = twitter.access_token
    creds['secret_token'] = twitter.secret_token

    with open('creds/twitterCreds.json','w') as f:
        json.dump(creds, f)

for i, row in accts.iterrows():
    player, usr = row
    print(usr)
    if player in skip:
        continue
    # returns parsed posts for given username
    print('Querying API For User Data')
    tweets = twitter.get_user_data(usr)
    print("Loading Data to DB")
    twitter.load_tweets(player, usr, tweets)
