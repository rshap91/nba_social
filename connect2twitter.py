# connect2twitter
import tweepy
import requests
import sqlite3
import psycopg2

class twitterObj:

    @staticmethod
    def parse_post(post, username, usr_id):
        out_dic = {
            'post_id' : post.id_str,
            'username' : username,
            'user_id' : usr_id
            'date': post.created_at,
            'retweet_count':post.retweet_count,
            'favorite_count': post.favorite_count,
            'possibly_sensitive': post.possibly_sensitive,
            'hastags': [tag['text'] for tag in post.entities['hashtags']],
            'user_mentions': [m['screen_name'] for m in post.entitites['user_mentions']],
            'in_response_to': post.in_reply_to_screen_name
        }

        text = p.text
        out_dic['emojis'] : _utils.get_emojis(text) # NOT DEFINED!
        if post.entities['symbols']:
            print('THIS POST HAS SYMBOLS!')
            print(post.text)
            print(post.entities['symbols'])
        # get rid of urls
        urls = [u['url'] for u in post['urls']] + [u['url'] for u in posts['media']]
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
        self.client_id=client_id,
        self.client_secret=client_secret
        self.access_token=access_token
        self.secret_token=secret_token
        self.api = self._build_api(self.client_id, self.client_secret, self.access_token, self.secret_token)
        self.load_posts = self.useQuery(self.load_posts)


    def _build_api(self, client_id, client_secret, access_token, secret_token):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
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
        usr = api.get_user(username)
        pg = 1
        posts = []
        new_posts = usr.timeline(page=pg)
        while new_posts:
            posts.append([twitterObj.parse_post(p, username, usr.id_str) for p in new_posts])
            pg +=1
            new_posts = usr.timeline(page=pg)
        return posts

    def load_posts(self,user_name, user_id, posts):
        """
        positional args are
            - user_name
            - user_id
            - posts
        """
        q = """
        INSERT INTO twitter_posts (
            {}
        )
        VALUES (
            {}
        )
        """ # we can simplify above

        cur = self.conn.cursor()
        post_num = 1
        try:
            for post in posts_generator:
                if post_num % 100 == 0:
                    print('Loading Post Number', post_num)

                cols = list(post.keys())
                vals = list(posts.values())

                cur.execute(
                    q.format(cols, ','.join(['?']*len(cols))), #format column names and binds
                    (*cols)
                )
                post_num+=1
        except Exception as e:
            print(str(e))
            return False
        return True
