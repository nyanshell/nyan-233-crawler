import datetime
from google.appengine.ext import db
    
# zh-user but uncheck his follower
class temp_user(db.Model):
    user_id = db.IntegerProperty()
    user_name = db.StringProperty() #screen name
    last_tweet_date = db.DateProperty(auto_now_add=True)
    tweet_cnt = db.IntegerProperty()
    user_lang = db.StringProperty()
    is_lock = db.BooleanProperty(default=False)
    
# zh-user but not check activity
class zh_user(temp_user):
    day_cnt = db.IntegerProperty(default=1)
    average_tweet = db.FloatProperty(default=1.000)
    
# zh-user but not active
class dead_zh_user(db.Model):
    user_id = db.IntegerProperty()
    
# user number count
class Count(db.Model):
    user_active = db.IntegerProperty(default=0)
    user_dead = db.IntegerProperty(default=0)
    count_start_date = db.DateTimeProperty(auto_now_add=True)
