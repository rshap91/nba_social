#_utils
import re


"""
We are actually gonna have to do these in a certain order since the presence
of one affects the determination of the others.

For example, a url with an anchor tag would affect how I identify hashtags.


"""

def get_urls(text):
    # went with this guy minus the carat (^) for start of line
    # https://www.regextester.com/93652
    ulr_re = re.compile('(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')

    return re.findall(url_re, text)



def get_emojis(text):
    # amazingly this seems to work
    # might be kinda slow...
    emoji_range = range(127744, 128760)
    emojis = []
    for c in text:
        if ord(c) in emoji_range:
            emojis.append(c)

    return list(set(emojis))



def get_hashtags(text):
    """
    This is actually kinda crazy.

    This source:
    http://erictarn.com/post/1060722347/the-best-twitter-hashtag-regular-expression
    says he's duplicated twitters hastag identifying methodology.

    But see here:
    https://shkspr.mobi/blog/2010/02/hashtag-standards/
    for a very interesting discussion on hastag syntax with some good edge cases
    and why twitter might not be the best.

    """
    # alternatives
    "#[^ :\n\t\.,\?\/’'!]+"
    "#[a-zA-Z1-9]+"

    # frankly I"m happy with this as it's simple and I will go down a rabbit hole on these other ones.
    # it seems to do a decent job
    htag = re.compile(r'#[a-zA-Z0-9\U0001f3c0]')
    # tested it on all of these: https://top-hashtags.com/hashtag/basketball/
    # got all of them (the unicode one is the basketball emoji)

    return list(set(re.findall(htag, text)))



def get_usr_mentions(text):


    return
