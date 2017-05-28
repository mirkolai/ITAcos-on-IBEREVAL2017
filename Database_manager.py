__author__ = 'mirko'

from sklearn.externals import joblib
from Tweet import make_tweet
import os.path
import pymysql
import config as cfg

class Database_manager(object):

    db=None
    cur=None

    def __init__(self):

        self.db = pymysql.connect(host=cfg.mysql['host'],
                 user=cfg.mysql['user'],
                 passwd=cfg.mysql['passwd'],
                 db=cfg.mysql['db'],
                 charset='utf8')
        self.cur = self.db.cursor()
        self.cur.execute('SET NAMES utf8mb4')
        self.cur.execute("SET CHARACTER SET utf8mb4")
        self.cur.execute("SET character_set_connection=utf8mb4")
        self.db.commit()

    def return_test(self):


        if os.path.isfile('test.pkl') :
            tweets= joblib.load('test.pkl')
            return tweets


        tweets=[]
        self.cur.execute(" SELECT `id`, `content`, `language`, `stance`, `gender` "
                         " FROM `test ")
        i=0
        for tweet in self.cur.fetchall():
                i+=1
                id=tweet[0]
                content=tweet[1]
                language=tweet[2]
                stance=tweet[3]
                gender=tweet[4]


                this_tweet=make_tweet(id, content,language, stance, gender )

                tweets.append(this_tweet)

        joblib.dump(tweets, 'test.pkl')

        return tweets



    def return_training(self, language=None):

        if language=="ca" or language=="es":
            filter=" where language='"+language+"'"
        else:
            filter=""


        if os.path.isfile('training'+filter+'.pkl') :
            tweets= joblib.load('training'+filter+'.pkl')
            return tweets


        tweets=[]


        self.cur.execute(" SELECT `id`, `content`, `language`, `stance`, `gender` "
                         " FROM `training` "+filter)
        i=0
        for tweet in self.cur.fetchall():
                i+=1
                id=tweet[0]
                content=tweet[1]
                language=tweet[2]
                stance=tweet[3]
                gender=tweet[4]


                this_tweet=make_tweet(id, content,language, stance, gender )

                tweets.append(this_tweet)

        joblib.dump(tweets, 'training'+filter+'.pkl')

        return tweets





def make_database_manager():
    database_manager = Database_manager()

    return database_manager


if __name__ == '__main__':
    database_manager = Database_manager()
    tweets=database_manager.return_training()

