"""
some implement of twitter timeline api
Gestalt Lur
2013-05-29
"""
import httplib
import urllib
import os

from obtain_oauth import get_access_token
from obtain_oauth import get_oauth_header 
from gzip_decode import gzip_decode

# API : GET follower/list
def get_tweets( user_name, count ):
    access_token = get_access_token()
    #TODO raise a GetTweetError here
    host = 'api.twitter.com'
    url = '/1.1/statuses/user_timeline.json?count=' + str(count) + '&screen_name=' + user_name

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    #connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    #connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()

    zipped_tweets = twitter_response.read()

    tweets_entites = gzip_decode( zipped_tweets )

    connect.close()
    
    return tweets_entites

# get follower
def get_follow_list( user_id=None, user_name=None, page=-1 ):

    access_token = get_access_token()

    if ( user_id == None ) and ( user_name == None ):
        return "Must set either user_id or user_name"
    elif ( user_id != None ) and ( user_name != None ):
        return "user_id and user_name can't be used at same time"

    host = 'api.twitter.com'
    if user_name != None:
        url = '/1.1/followers/list.json?cursor=' + str(page) + '&screen_name=' + user_name + '&skip_status=true&include_user_entities=false'
    else:
        url = '/1.1/followers/list.json?cursor=' + str(page) + '&user_id=' + str(user_id) + '&skip_status=true&include_user_entities=false'

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()
    # if can't get follower list, return a status code
    if twitter_response.status != 200:
        logging.warning('Can\'t get follower list')
        return twitter_response.status
        
    zipped_tweets = twitter_response.read()

    follower_entites = gzip_decode( zipped_tweets )

    connect.close()

    return follower_entites

# API : search/tweets
def search_keyword( key_word, count=5 ):

    if not isinstance( key_word , str ):
        return "Keyword must be a string"

    access_token = get_access_token()

    host = 'api.twitter.com'
    url = '/1.1/search/tweets.json?q=' + urllib.quote( key_word, '' ) + '&result_type=mixed&count=' + str( count ) + '&include_entities=true'
    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()

    # Check that everything went ok.
    if twitter_response.status != 200:
        print "Failed to request tweets, code " + str(twitter_response.status)
        return "Failed to request tweets, code " + str(twitter_response.status)

    zipped_tweets = twitter_response.read()

    search_entites = gzip_decode( zipped_tweets )

    connect.close()

    return search_entites[ 'statuses' ]


# API : POST statuses/filter
# need user context
# unknown error, get 401
"""
def get_keyword( track ):

    if not isinstance( track , str ):
        return "Keyword must be a string"

    host = 'stream.twitter.com'
    url = '/1.1/statuses/filter.json'
    msg = "track=" + track
    oauth_header = get_oauth_header( "POST", host, url, msg )
    msg = urllib.quote( msg, '' )

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("POST", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", oauth_header )   
    connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders(message_body=msg)

    twitter_response = connect.getresponse()

    # Check that everything went ok.
    if twitter_response.status != 200:
        print "Failed to request tweets, code " + str(twitter_response.status) + str(twitter_response.read())
        return "Failed to request tweets, code " + str(twitter_response.status)

    zipped_tweets = twitter_response.read()

    search_entites = gzip_decode( zipped_tweets )

    connect.close()

    return search_entites
"""

# this function not use a bearer token but a token from dev.twitter.com
# API : user/lookup
def get_user(user_id=None, user_name=None ):

    if ( user_id == None ) and ( user_name == None ):
        return "Must set either user_id or user_name"
    elif ( user_id != None ) and ( user_name != None ):
        return "user_id and user_name can't be used at same time"

    host = 'api.twitter.com'
    url = '/1.1/users/lookup.json'
    if user_name != None:
        opt = 'screen_name=' + user_name
    else:
        opt = 'user_id=' + str( user_id ) 

    oauth_header = get_oauth_header( "GET", host, url, 'include_entities=true', opt )

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url + '?' + opt + '&include_entities=true')
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", oauth_header )   
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()

    # Check that everything went ok.
    if twitter_response.status != 200:
        print "Failed to request tweets, code " + str(twitter_response.status)
        #return "Failed to request tweets, code " + str(twitter_response.status)

    zipped_tweets = twitter_response.read()
    #print len(zipped_tweets)
    user_entites = gzip_decode( zipped_tweets )
    #print user_entites
    connect.close()

    return user_entites[ 0 ] # only return user
