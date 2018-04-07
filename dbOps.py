# Build DB
import sqlite3

def make_fb_table(conn):
    q = """
    CREATE TABLE fb_posts (
    post_id VARCHAR(32),
    page_id VARCHAR(32),
    created_timestamp TIMESTAMP,
    message TEXT,
    story TEXT,
    FOREIGN KEY(page_id) REFERENCES fb_pages(page_id)
    );
    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()

def make_twitter_table(conn):
    q = """
    CREATE TABLE tweets (
        tweet_id VARCHAR(32) PRIMARY KEY NOT NULL,
        user_id VARCHAR(32),
        date DATE,
        retweet_count INTEGER,
        favorite_count INTEGER,
        possibly_sensitive BOOLEAN,
        in_response_to VARCHAR(256),
        status_text TEXT,
        FOREIGN KEY (user_id) REFERENCES twitter_users (user_id)
    );

    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()

def make_dim_tables(conn):
    q = '''

    CREATE TABLE fb_pages (
        page_id VARCHAR(32) PRIMARY KEY NOT NULL,
        page_name VARCHAR(128),
        player_name VARCHAR(128)
    );

    CREATE TABLE twitter_users (
        user_id VARCHAR(32) PRIMARY KEY NOT NULL,
        user_name VARCHAR(128),
        player_name VARCHAR(128)
    );

    CREATE TABLE hashtags (
        hashtag_id INTEGER PRIMARY KEY NOT NULL,
        hashtag VARCHAR(256)
    );

    CREATE TABLE emojis (
        emoji_id INTEGER PRIMARY KEY NOT NULL,
        emoji VARCHAR(64)
    );

    CREATE TABLE fbpost_hashtags (
        hashtag_id INTEGER NOT NULL,
        post_id VARCHAR(32) NOT NULL,
        htag_count INTEGER,
        PRIMARY KEY (hashtag_id, post_id),
        FOREIGN KEY(hashtag_id) REFERENCES hashtags(hashtag_id),
        FOREIGN KEY(post_id) REFERENCES fb_posts(post_id)
    );

    CREATE TABLE fbpost_emojis (
        emoji_id INTEGER NOT NULL,
        post_id VARCHAR(32) NOT NULL,
        emoji_count INTEGER,
        PRIMARY KEY (emoji_id, post_id),
        FOREIGN KEY(emoji_id) REFERENCES emojis(emoji_id),
        FOREIGN KEY(post_id) REFERENCES fb_posts(post_id)
    );

    CREATE TABLE tweet_hashtags (
        hashtag_id INTEGER NOT NULL,
        tweet_id VARCHAR(32) NOT NULL,
        htag_count INTEGER,
        PRIMARY KEY (hashtag_id, tweet_id),
        FOREIGN KEY(hashtag_id) REFERENCES hashtags(hashtag_id),
        FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id)
    );

    CREATE TABLE tweet_emojis (
        emoji_id INTEGER NOT NULL,
        tweet_id VARCHAR(32) NOT NULL,
        emoji_count INTEGER,
        PRIMARY KEY (emoji_id, tweet_id),
        FOREIGN KEY(emoji_id) REFERENCES emojis(emoji_id),
        FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id)
    );

    CREATE TABLE tweet_usr_mentions (
        usr_mention_id VARCHAR(32) NOT NULL,
        tweet_id VARCHAR(32) NOT NULL,
        usr_mention_count INTEGER,
        PRIMARY KEY (usr_mention_id, tweet_id),
        FOREIGN KEY(usr_mention_id) REFERENCES twitter_users(user_id),
        FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id)
    );

    '''
    cur = conn.cursor()
    for stmt in q.split(';'):
        cur.execute(stmt)
    cur.close()


if __name__ == '__main__':
    dbname = "nbaSocial.db"
    conn = sqlite3.connect(dbname)

    make_dim_tables(conn)
    make_fb_table(conn)
    make_twitter_table(conn)

    conn.commit()
    conn.close()
