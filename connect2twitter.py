# connect2twitter
import tweepy
import requests
import sqlite3
import psycopg2
import traceback
import _utils

class twitterObj:

    @staticmethod
    def parse_tweet(tweet, username, usr_id):
        out_dic = {
            'tweet_id' : tweet.id_str,
            'username' : username,
            'user_id' : usr_id,
            'date': tweet.created_at,
            'retweet_count':tweet.retweet_count,
            'favorite_count': tweet.favorite_count,
            'possibly_sensitive': tweet.possibly_sensitive if hasattr(tweet, 'possibly_sensitive') else None,
            'hashtags': [tag['text'] for tag in tweet.entities['hashtags']],
            'user_mentions': [m['screen_name'] for m in tweet.entities['user_mentions']],
            'in_response_to': tweet.in_reply_to_screen_name
        }

        text = tweet.text
        out_dic['emojis'] = _utils.get_emojis(text)
        if tweet.entities['symbols']:
            print('THIS POST HAS SYMBOLS!')
            print(tweet.text)
            print(tweet.entities['symbols'])
        # get rid of urls
        urls = [u.get('url',None) for u in tweet.entities.get('urls',{})] \
                + [u.get('url',None) for u in tweet.entities.get('media', {})]
        urls = [url for url in urls if url]
        for url in urls:
            text = text.replace(url, '')
        # text = _utils.remove_stop_words(text) # also not defined
        out_dic['text'] = text
        return out_dic

    def __init__(self, DBINFO, client_id, client_secret, access_token=None, secret_token=None):
        if isinstance(DBINFO, str):
            self.dbinfo = DBINFO
        else:
            assert isinstance(DBINFO, dict),\
            'Must pass either .db filename or dict with keys: host, port, dbname, user, password'
            assert all([key in DBINFO for key in ['host','port','dbname', 'user', 'password']]),\
            'Must pass either .db filename or dict with keys: host, port, dbname, user, password'
            self.dbinfo = DBINFO
        self.conn = None
        self.client_id=client_id
        self.client_secret=client_secret
        self.access_token=access_token
        self.secret_token=secret_token
        self.api = self._build_api(self.client_id, self.client_secret, self.access_token, self.secret_token)
        self.load_tweets = self._useQuery(self.load_tweets)


    def _useQuery(self, func):
        # decorator that opens and closes conn for you
        def inner(*args, **kwargs):
            if isinstance(self.dbinfo, str):
                self.conn = sqlite3.connect(self.dbinfo)
            else:
                self.conn = pyscopg2.connect(**self.dbinfo)
            ret  = func(*args, **kwargs)
            self.conn.commit()
            self.conn.close()
            return ret
        return inner


    def _build_api(self, client_id, client_secret, access_token, secret_token):
        auth = tweepy.OAuthHandler(client_id, client_secret)
        if not access_token:
            redirect_url = auth.get_authorization_url()
            print('Go the url below in a browser.')
            print('If you are already logged in to facebook you will be redirected, otherwise log in to give permissions.')
            print('Once you are redirected, copy the new url and paste below.')
            print()
            print(redirect_url)
            print()
            url = input('Paste URL Here: ')
            verifier = url[url.find('&oauth_verifier=') + len('&oauth_verifier='):]
            access_token, secret_token = auth.get_access_token(oauth_verifier)
        auth.set_access_token(access_token, secret_token)
        return tweepy.API(auth)


    def get_user_data(self, username):
        usr = self.api.get_user(username)
        pg = 1
        tweets = []
        new_tweets = usr.timeline(page=pg)
        while new_tweets:
            tweets.extend([twitterObj.parse_tweet(p, username, usr.id_str) for p in new_tweets])
            pg +=1
            new_tweets = usr.timeline(page=pg)
        return tweets


    def load_tweets(self,player, username, tweets):
        """
        positional args are
            - player_name
            - username
            - list of processed posts
        """
        cur = self.conn.cursor()
        tweet_num = 1
        try:
            for tweet in tweets:
                if tweet_num % 100 == 0:
                    print('Loading Post Number', tweet_num)

                cols = list(tweet.keys())
                vals = list(tweet.values())
                # print(cols)
                # print(vals)

                # insert post info into post dim table
                cur.execute('''
                    INSERT OR IGNORE INTO tweets (
                        tweet_id,
                        retweet_count,
                        favorite_count,
                        possibly_sensitive,
                        in_response_to,
                        status_text
                    )
                    VALUES (?,?,?,?,?,?);
                ''',
                (tweet['tweet_id'], tweet['retweet_count'], tweet['favorite_count'],
                 tweet['possibly_sensitive'], tweet['in_response_to'], tweet['text'])  #binds
                )
                # insert page info into page table
                cur.execute('''
                    INSERT OR IGNORE INTO twitter_users (
                        user_id,
                        user_name,
                        player_name
                    )
                    VALUES (?, ?, ?);
                ''', (tweet['user_id'], tweet['username'], player)
                )

                for emoji in tweet['emojis']:
                    # find if the emoji is already in the table...
                    cur.execute('''
                        SELECT emoji_id FROM emojis
                        WHERE emoji = ?;
                    ''', (emoji,))
                    eid = cur.fetchone()
                    # if it's not there, insert it
                    if not eid:
                        cur.execute('''
                            INSERT INTO emojis (emoji)
                            VALUES (?);
                        ''', (emoji,))
                        # and get the generated id
                        cur.execute('''
                            SELECT emoji_id FROM emojis
                            WHERE emoji = ?;
                        ''', (emoji,))
                        eid = cur.fetchone()
                    eid = eid[0] # it's a tuple
                    # now do the same thing for each hash tag for each emoji...
                    # something MUST be wrong with this design, but i don't know how else to do it other than a flat table with arrays
                    for htag in tweet['hashtags']:
                        cur.execute('''
                            SELECT hashtag_id FROM hashtags
                            WHERE hashtag = ?;
                        ''', (htag,))
                        hid = cur.fetchone()
                        # if it's not there, insert it
                        if not hid:
                            cur.execute('''
                                INSERT INTO hashtags (hashtag)
                                VALUES (?);
                            ''', (htag,))
                            # and get the generated id
                            cur.execute('''
                                SELECT hashtag_id FROM hashtags
                                WHERE hashtag = ?;
                            ''', (htag,))
                            hid = cur.fetchone()
                        hid = hid[0] # it's a tuple
                        # last loop to get all user_mentions
                        for mention in tweet['user_mentions']:
                            cur.execute('''
                                SELECT user_id FROM twitter_users
                                WHERE user_name = ?;
                            ''', (mention,))
                            uid = cur.fetchone()
                            # if it's not there, insert it
                            if not uid:
                                uid = self.api.get_user(mention).id_str
                                cur.execute('''
                                    INSERT INTO twitter_users (user_id, user_name)
                                    VALUES (?, ?);
                                ''', (uid, mention))
                            else:
                                uid = uid[0] # it's a tuple
                            # now insert ALL ids into the main data table
                            cur.execute('''
                                INSERT INTO twitter_data (
                                    tweet_id,
                                    user_id,
                                    date,
                                    hashtag_id,
                                    user_mention,
                                    emoji_id
                                )
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''',
                            (tweet['tweet_id'], tweet['user_id'], tweet['date'],
                            hid, uid, eid)
                            )
                tweet_num+=1
        except Exception as e:
            traceback.print_exc()
            return False
        return True
