__author__ = 'mirko'
import numpy
from sklearn.linear_model.logistic import LogisticRegression
import Features_manager
import Database_manager
import pymysql
import config as cfg

db = pymysql.connect(host=cfg.mysql['host'],
                     user=cfg.mysql['user'],
                     passwd=cfg.mysql['passwd'],
                     db=cfg.mysql['db'],
                     charset='utf8mb4',
                     use_unicode=True)
cur = db.cursor()
cur.execute('SET NAMES utf8mb4')
cur.execute("SET CHARACTER SET utf8mb4")
cur.execute("SET character_set_connection=utf8mb4")
db.commit()

print("Task B - Test 2")

database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()

tweets_train=numpy.array(database_manager.return_training())
gender_train=numpy.array(feature_manager.get_gender(tweets_train))

tweets_test=numpy.array(database_manager.return_test())

features_set=[
"BoW","BoL","BoP","SVM_chargrams","urlredirect","numhashtag","punctuation_marks","lens"
]

feature_names=features_set

X_train,X_test,feature_name_global,feature_index_global=feature_manager.create_feature_space(tweets_train,feature_names,tweets_test)

print(X_train.shape,X_test.shape)

clf = LogisticRegression()

clf.fit(X_train,gender_train)
test_predict = clf.predict(X_test)

for i in range( 0,len(test_predict)):
    print(test_predict[i])
    print(tweets_test[i].id)
    cur.execute(" INSERT INTO `test_2`"
                " (`id`, `language`, `gender` ) "
                " VALUES (%s,%s,%s) "
                " on  duplicate key  update `gender`=%s ",(tweets_test[i].id,tweets_test[i].language,test_predict[i],test_predict[i],))


