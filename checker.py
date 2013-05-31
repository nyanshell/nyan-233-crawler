#use to check whether a user active in zh_user
import webapp2
import time
import datetime

from google.appengine.ext import db
from tweetunity.request_timeline import get_user
from dbmodels import zh_user, dead_zh_user, Count

SLEEP_TIME = 43200 # 12 hours
AVERAGE_TWEET = 1.0

class CheckerHandler(webapp2.RequestHandler):
    def get(self):
        while True:
            if Count.all().get() != None:
                td = datetime.date.today()
                all_zh = zh_user.gql("WHERE last_tweet_date < :1 ", td - datetime.timedelta( 7 ) ).run()
                
                count = Count.all().get()
                print all_zh.count()
                time.sleep( 60 )
                for user in all_zh:
                    cur = get_user( user_name=user.user_name )
                    tc = cur[ 'statuses_count' ]
                    ava = ( float( tc - user.tweet_cnt ) / float( td - user.last_tweet_date ) + user.average_tweet ) / 2.000
                    
                    if ava < AVERAGE_TWEET:
                        count.user_active -= 1
                        count.user_dead += 1
                        user.delete()
                    else:
                        user.tweet_cnt = tc
                        user.last_tweet_date = td
                        user.average_tweet = ava
                        user.put()
                count.put()
            time.sleep( SLEEP_TIME )
#_ah/start
app = webapp2.WSGIApplication([('/', CheckerHandler)], debug=True)

