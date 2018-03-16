# Scrape FB and Load to DB

import json
import sqlite3
# load my custom object
from connect2facebook import *

# get list of ballers:
with open('ballers.txt', 'r') as f:
    ballers = [l.strip() for l in f.readlines()]

# Doing the data load in chunks so skipping those who have already been uploaded.
dbname = "nbaSocial.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('select distinct page_name from fb_posts')
skip = [c[0] for c in cur.fetchall()]
print(skip)
conn.close()

# load credentials
with open('creds/facebookCreds.json','r') as f:
    creds = json.load(f)

# instantiate custom object
fb = fbObj(dbname, **creds)

for blr in ballers:
    if blr in skip:
        continue
    # returns page with most posts (minimum 100)
    page_name, page_id, posts = fb.find_posts(blr)

    # some don't show up using the graph api's search???
    # not really sure why or how to fix this so some will be done manually
    if not page_name:
        print("Could not find page for", blr)
        continue

    fb.load_posts(page_name, page_id, posts)


# had to look up some manually
manual_ids = [
    ('Dwayne Wade','79979913992'),
]

for page_name, page_id in manual_ids:
    posts = fb.graph.get_all_connections(page_id, 'posts')
    fb.load_posts(page_name,page_id, posts)
