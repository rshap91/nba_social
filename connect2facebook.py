import facebook
import requests
import sqlite3
import psycopg2

class fbObj:

    def __init__(self, DBINFO, client_id, client_secret, access_token=None):
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
        self.graph = self._build_graph(self.client_id, self.client_secret, self.access_token)
        self.load_posts = self.useQuery(self.load_posts)

    @staticmethod
    def parse_post(post, page_name, page_id):
        out_dic = {
            "post_id": post['id'],
            'page_name': page_name,
            'page_id': page_id,
            "created_timestamp": post['created_time'],
            "story": post.get('story', '').lower(),

        }

        msg = post.get('message', '')

        urls = _utils.get_urls(msg)
        for url in urls:
            msg = msg.replace(url, '')

        emojis = _utils.get_emojis(msg)
        hashtags = _utils.get_hashtags(msg)
        # usr_mentions = _utils.get_usr_mentions(msg)
        out_dic["message"] = msg
        out_dic['emojis'] = emojis
        out_dic['hashtags'] = hashtags


        return out_dic


        # users, tags(@), hashtags, named_entities, emojis, shares?


    def useQuery(self, func):
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


    def _build_graph(self, client_id, client_secret, access_token=None):
        # you can skip all this by supplying an access_token
        if not access_token:
            auth_url = "https://www.facebook.com/v2.12/dialog/oauth?"

            auth_params = {
                'client_id':client_id,
                'redirect_uri': 'https://www.facebook.com/connect/login_success.html',
                'state': {'st':'abcdefg', 'dt':123456789}
            }

            resp = requests.get(auth_url, params=auth_params)
            print('Go the url below in a browser.')
            print('If you are already logged in to facebook you will be redirected, otherwise log in to give permissions.')
            print('Once you are redirected, quickly copy the url and paste below.')
            print("You will have ~ 3 seconds before being redirected again and losing the code.")
            print()
            print(resp.request.url)
            print()
            code_url = input('Paste URL Here:')
            start = code_url.find('code=') +5
            end = code_url.find('&state')
            code = code_url[start:end]

            token_params = {
                'client_id':client_id,
                'client_secret': client_secret,
                'redirect_uri': 'https://www.facebook.com/connect/login_success.html',
                'code': code
            }

            token_url = "https://graph.facebook.com/oauth/access_token?"
            resp = requests.get(token_url, params=token_params)
            access_token = resp.json()['access_token']
        return facebook.GraphAPI(access_token)


    def find_posts(self, player=None, pageid=None, npages=10, thresh = 100):
        """
        Tries it's best to get pageid from player name if passed.

        Returns page_name, page_id, posts_generator
        """
        # you can just supply pageid and it skips this
        if not pageid:
            assert player, 'must pass either player or pageid.'
            pages = self.graph.search('page', q=player)

            # use the player with the most data
            nposts = {}
            print('Searching Pages ...')
            for page in pages['data']:
                if page['name'].lower() == player.lower():
                    print(page)
                    posts =  self.graph.get_all_connections(page['id'], 'posts')
                    nposts[(page['id'], page['name'])] = len(list(posts))
            numpages=1

            if nposts:
                chosen = max(list(nposts.items()), key = lambda tup: tup[1])
            else:
                chosen = ([],0)
            while chosen[1] < thresh and (numpages < npages): # we only go on to next page if no matches so far
                # get next page token
                try:
                    after = pages['paging']['cursors']['after']
                except KeyError as e:
                    print('No More Pages')
                    break
                pages = self.graph.search('page', q=player, after=after)
                for page in pages['data']:
                    if page['name'].lower() == player.lower():
                        print(page)
                        posts =  self.graph.get_all_connections(page['id'], 'posts')
                        nposts[(page['id'], page['name'])] = len(list(posts))

                numpages+=1
                if nposts:
                    chosen = max(list(nposts.items()), key = lambda tup: tup[1])
                else:
                    chosen = ([],0)

            if chosen[1] < thresh:
                print('Could not find page with at least {} number of posts!'.format(thresh))
                return None, None, None
            print('Done!')
            chosen_id = chosen[0][0]
            chosen_name = chosen[0][1]
            # iterator of all posts for given page
            return chosen_name, chosen_id, self.graph.get_all_connections(chosen_id, 'posts')


    def load_posts(self,page_name, page_id, posts_generator):
        """
        positional args are
            - page_name
            - page_id
            - posts_generator
        """
        q = """
        INSERT INTO fb_posts (
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

                parsed = fbObj.parse_post(post, page_name, page_id)
                cols = list(parsed.keys())
                vals = list(parsed.values())

                for emoji in parse['emojis']:
                    cur.execute('''
                        INSERT OR IGNORE INTO emojis (emoji)
                        VALUES (?);
                    ''', (emoji,))
                    cur.execute('''
                        SELECT emoji_id FROM emojis
                        WHERE emoji = %s;
                    ''', (emoji,))
                    emoji_id = cur.fetchone()
                for htag in parse['hashtags']:
                    cur.execute('''
                        INSERT OR IGNORE INTO emojis (emoji)
                        VALUES (?);
                    ''', (emoji,))
                    cur.execute('''
                        SELECT emoji_id FROM emojis
                        WHERE emoji = %s;
                    ''', (emoji,))
                    emoji_id = cur.fetchone()


                cur.execute(
                    q.format(cols, ','.join(['?']*len(cols))), #format column names and binds
                    (*vals)
                )
                post_num+=1
        except Exception as e:
            print(str(e))
            return False
        return True