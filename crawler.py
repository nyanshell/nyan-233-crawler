import webapp2
import time
import logging
import os

from dbmodels import zh_user, temp_user, dead_zh_user, Count
from zhdetect import zhdetect, zhdetect_multi
from google.appengine.ext import db
from tweetunity.request_timeline import get_tweets, get_follow_list, search_keyword, get_user

ZH_RATE = 0.70
WAIT_TIME = 60

def temp_user_add( user ):
    if temp_user.gql("WHERE user_id = :1", user[ 'id' ] ) != None:
        return ;
    logging.info('Adding a temp user ' + user[ 'screen_name' ] + ' to temp_user')
    #time.sleep( WAIT_TIME )
    temp_user( user_id=user[ 'id' ],
    user_name=user[ 'screen_name' ], #screen name
    user_nick=user[ 'name' ],
    tweet_cnt=user[ 'statuses_count' ],
    user_lang=user[ 'lang' ],
    is_lock=user[ 'protected' ],
    ).put()

# get known user screen_name( user_name )
# use for initlization
def init_known_user():
    _curpath = os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
    abs_path = os.path.join( _curpath, 'known_users.txt')
    f = open( abs_path, 'rb' )
    ul = f.readlines()
    f.close()
    USER_ADDED = False
    for user_name in ul:
        user_name = user_name.replace( '\n', '' )
        user = get_user( user_name=user_name )
        # add user to temp_user
        if user != None:
            temp_user_add( user )
            USER_ADDED = True
    return USER_ADDED

#TODO this function should be shorten or refactor
def zh_user_add( user ):
    if not isinstance( user, temp_user ):
        logging.error('user to be add not belong temp_user')
        return
        
    zh_user( key_user_id = user.user_id,
    user_name = user.user_name, #screen name
    tweet_cnt = user.tweet_cnt,
    user_lang = user.user_lang,
    is_lock = user.is_lock,
    ).put()

def zh_user_checker( user ):
    if user[ 'lang' ] == 'zh-cn':
        return True
    elif user[ 'statuses_count' ] < 50:
        return False
    elif user[ 'protected' ] == True:
        if zhdetect( user[ 'description' ] ) >= ZH_RATE:
            return True
        # search if someone mention him
        res = search_keyword( user['screen_name'], count=50)
        if res == None:
            return False
        return zhdetect_multi( res )
    else:
        res = get_tweets( user[ 'screen_name' ], count=50 )
        return zhdetect_multi( res )

class CrawlerHandler(webapp2.RequestHandler):
    def get(self):
        while True: # TODO need add some wait time
            if temp_user.all().get() == None: # no one in data
                if init_known_user() == False: # get known user from file
                    logging.error('No known users, application should exit.')
                    pass # TODO no user avaliable in given user list, exit
            # fetch a user from temp_user
            someone = temp_user.all().get()
            # add user to zh_user
            zh_user_add( someone )
            # count ++
            count = Count.all().get()
            if count != None:
                count.user_active += 1
                count.put()
            else:
                Count().put()
                
            #fetch his follower, add to temp user if zh user detected
            cursor = -1
            while cursor != 0:
                res = get_follow_list( user_name=someone.user_name, page=cursor )
                if res == None:
                    break
                    pass # TODO wait for some time
                else:
                    for user in res[ 'users' ]:
                        if ( dead_zh_user.gql("WHERE user_id = :1", user[ 'id' ] ) != None ) or ( zh_user.gql("WHERE user_id = :1", user[ 'id' ] ) != None ): # check repeat
                            continue
                        if zh_user_checker( user ) == True:
                            temp_user_add( user )
                    cursor = res[ 'next_cursor' ]
                    if cursor == 0:
                        break

            # delete user from temp_user
            temp_user.delete( someone )
            #temp_user.put() seems can't do this if need delete

app = webapp2.WSGIApplication([('/_ah/start', CrawlerHandler)], debug=True)

