# Build DB
import sqlite3



def make_fb_table(conn):
    q = """
    CREATE TABLE fb_posts (
    post_id VARCHAR(32) PRIMARY KEY,
    page_name VARCHAR(128),
    page_id VARCHAR(32),
    created_timestamp TIMESTAMP,
    message TEXT,
    story TEXT,
    emoji_id INTEGER,
        FOREIGN KEY (emoji_id) REFERENCES emojis (emoji_id),
    hashtag_id INTEGER,
        FOREIGN KEY (hashtag_id) REFERENCES hashtags (hashtag_id)
    )
    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()

# def make_fb_indices(conn):
#     q = """
#     CREATE INDEX date_index ON fb_posts (created_timestamp);
#     CREATE INDEX player_index ON fb_posts (page_name);
#     CREATE INDEX player_date_index ON fb_posts (page_name, created_timestamp);
#     """
#     cur = conn.cursor()
#     for stmt in q.split(';'):
#         cur.execute(stmt)
#     cur.close()


def make_twitter_table(conn):
    q = """
    CREATE TABLE twitter_data (
        tweet_id VARCHAR (32),
            FOREIGN KEY (tweet_id) REFERENCES tweets (tweet_id),
        user_id VARCHAR(32),
            FOREIGN KEY (user_id) REFERENCES twitter_users (user_id),
        date DATE,
        hashtag_id INTEGER,
            FOREIGN KEY (hashtag_id) REFERENCES hashtags (hashtag_id),
        user_mention VARCHAR(32),
            FOREIGN KEY (user_id) REFERENCES twitter_users (user_id),
        emoji_id INTEGER,
            FOREIGN KEY (emoji_id) REFERENCES emojis (emoji_id)
    )
    """
    cur = conn.cursor()
    cur.execute(q)
    cur.close()


def make_dim_tables(conn):
    q = '''
    CREATE TABLE tweets (
        tweet_id VARCHAR(32) PRIMARY KEY,
        retweet_count INTEGER,
        favorite_count INTEGER,
        possibly_sensitive BOOLEAN,
        in_response_to VARCHAR(256),
        status_text TEXT
    );

    CREATE TABLE hashtags (
        hashtag_id INTEGER PRIMARY KEY,
        hashtag VARCHAR(128)
    );

    CREATE TABLE emojis (
        emoji_id INTEGER PRIMARY KEY,
        emoji VARCHAR(64)
    );

    CREATE TABLE twitter_users (
        user_id VARCHAR(32) PRIMARY KEY,
        user_name VARCHAR(128)
    )

    '''
    cur = conn.cursor()
    for stmt in q.split(';'):
        cur.execute(stmt)
    cur.close()


if __name__ == '__main__':
    dbname = "nbaSocial.db"
    conn = sqlite3.connect(dbname)

    make_fb_table(conn)
    make_fb_indices(conn)
