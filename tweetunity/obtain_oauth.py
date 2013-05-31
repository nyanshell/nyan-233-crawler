"""
twitter API oauth unities
date : 2013-05-29
author : Gestalt Lur
"""
import httplib
import urllib
import gzip
import StringIO
import ast
import random
import base64
import os
import hmac
import binascii
import time

from hashlib import sha1

from gzip_decode import gzip_decode
"""
according to this document, consumer key &
consumer secret were not change after encoding
to url, but this may change in future.
https://dev.twitter.com/docs/auth/application-only-auth
"""

def get_consumer_token(get_access=False):
    _curpath = os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
    abs_path = os.path.join( _curpath, 'oauth_key.txt')
    key_file = open( abs_path, 'rb' )
    consumer_key = key_file.readline().replace( '\n', '' )
    consumer_secret = key_file.readline().replace( '\n', '' )
    if get_access == True:
        access_token = key_file.readline().replace( '\n', '' )
        access_token_secret = key_file.readline().replace( '\n', '' )
        return consumer_key, consumer_secret, access_token, access_token_secret
    key_file.close()
    return consumer_key, consumer_secret

def get_access_token():
    consumer_key, consumer_secret = get_consumer_token()
    return obtain_bearer_token( consumer_key, consumer_secret ) 

"""
Authorization: 
OAuth oauth_consumer_key="", 
oauth_nonce="", 
oauth_signature="", 
oauth_signature_method="HMAC-SHA1",
oauth_timestamp="",
oauth_token="",
oauth_version="1.0"

steps from here:
https://dev.twitter.com/docs/auth/creating-signature
"""
def get_oauth_header( http_method, host, url, body="" ):
    consumer_key, consumer_secret, access_token, access_token_secret = get_consumer_token(True)
    
    nonce = get_nonce()
    timestamp = str( int( time.time() ) )
    sign_key = consumer_secret + "&" + access_token_secret

    #notice: options in url didn't included in parameter string here
    parameter_string = "oauth_consumer_key=" + consumer_key + "&oauth_nonce=" + nonce + "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + timestamp + "&oauth_token=" + access_token +"&oauth_version=1.0&" + urllib.quote( body, '')

    base_string = http_method + "&" + urllib.quote( host + url, '' ) + "&" + parameter_string 

    hashed = hmac.new( sign_key, base_string, sha1 )

    signature = binascii.b2a_base64( hashed.digest() )[ : -1 ]# delete '\n' 

    oauth_header = 'OAuth oauth_consumer_key="' + consumer_key + '",oauth_nonce="' + nonce + '", oauth_signature="' + signature + '", oauth_signature_method="HMAC-SHA1",oauth_timestamp="' + timestamp + '",oauth_token="' + access_token + '",oauth_version="1.0"'

    return oauth_header

def obtain_bearer_token( consumer_key, consumer_secret ):
    # use for test base64 encoding
    #consumer_key = b'xvz1evFS4wEEPTGEFPHBog'
    #consumer_secret = b'L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg'
    
    host = "api.twitter.com"
    url = "/oauth2/token"

    # POST request to obtain bearer token
    encoded_bearer = base64.b64encode( '%s:%s' % (consumer_key, consumer_secret)) 

    twitter_conn = httplib.HTTPSConnection( host )

    msg = r'grant_type=client_credentials'
    #msg = urllib.urlencode({'grant_type' : 'client_credentials'})
    #write headers
    twitter_conn.putrequest("POST", url )
    twitter_conn.putheader("Host", host )
    twitter_conn.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    twitter_conn.putheader("Authorization", "Basic %s" % encoded_bearer )   
    twitter_conn.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    twitter_conn.putheader("Content-Length", "%d" % len( msg ))
    twitter_conn.putheader("Accept-Encoding", "gzip" )
    twitter_conn.endheaders( message_body=msg )
    #twitter_conn.send( msg )

    twitter_response = twitter_conn.getresponse()

    # Check that everything went ok.
    if twitter_response.status != 200:
        #raise BearerGetException("Failed to request tweets, code " + str(twitter_response.status))
        print "Failed to request tweets, code " + str(twitter_response.status)
        return "Failed to request tweets, code " + str(twitter_response.status)

    # Read the response.
    # currently it will return .json file
    raw_data = twitter_response.read()
    respond_body_dict = gzip_decode( raw_data )

    #header_dict = twitter_response.getheaders()

    twitter_conn.close()

    return respond_body_dict['access_token']

def get_nonce():
    s = ""
    for i in range( 0 , 32 ):
        t = random.randint( 65, 90 )
        s = s + chr( t )
    return base64.b64encode( s )
