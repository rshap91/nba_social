# Build DB
import sqlite3

def make_fb_table(conn):
    q = """
    CREATE TABLE fb_data (
    post_id VARCHAR(32),
    page_id VARCHAR(32),
    emoji_id INTEGER,
    hashtag_id INTEGER,
    FOREIGN KEY (post_id) REFERENCES fb_posts (post_id),
    FOREIGN KEY (page_id) REFERENCES fb_pages (page_id),
    FOREIGN KEY (emoji_id) REFERENCES emojis (emoji_id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags (hashtag_id)
    )
    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()


def make_twitter_table(conn):
    q = """
    CREATE TABLE twitter_data (
        tweet_id VARCHAR (32),
        user_id VARCHAR(32),
        date DATE,
        hashtag_id INTEGER,
        user_mention VARCHAR(32),
        emoji_id INTEGER,
        FOREIGN KEY (tweet_id) REFERENCES tweets (tweet_id),
        FOREIGN KEY (user_id) REFERENCES twitter_users (user_id),
        FOREIGN KEY (hashtag_id) REFERENCES hashtags (hashtag_id),
        FOREIGN KEY (user_id) REFERENCES twitter_users (user_id),
        FOREIGN KEY (emoji_id) REFERENCES emojis (emoji_id)
    );
    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()


def make_dim_tables(conn):
    q = '''
    CREATE TABLE tweets (
        tweet_id VARCHAR(32) PRIMARY KEY NOT NULL,
        retweet_count INTEGER,
        favorite_count INTEGER,
        possibly_sensitive BOOLEAN,
        in_response_to VARCHAR(256),
        status_text TEXT
    );

    CREATE TABLE fb_posts (
        post_id VARCHAR(32) PRIMARY KEY NOT NULL,
        created_timestamp TIMESTAMP,
        message TEXT,
        story TEXT
    );

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
