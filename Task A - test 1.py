__author__ = 'mirko'
import numpy
import Features_manager
import Database_manager
import pymysql
from sklearn.svm.classes import SVC
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

print("Task A - Test 1")

database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()

tweets_train=numpy.array(database_manager.return_training())
stance_train=numpy.array(feature_manager.get_stance(tweets_train))

tweets_test=numpy.array(database_manager.return_test())

features_set=[
"BoW","BoL","SVM_chargrams","urlredirect","BoHMc","numhashtag","#uppercase"
]

feature_names=features_set

X_train,X_test,feature_name_global,feature_index_global=feature_manager.create_feature_space(tweets_train,feature_names,tweets_test)

print(X_train.shape,X_test.shape)

clf = SVC(kernel="linear")

clf.fit(X_train,stance_train)
test_predict = clf.predict(X_test)

for i in range( 0,len(test_predict)):
    print(test_predict[i])
    print(tweets_test[i].id)
    cur.execute(" INSERT INTO `test_1`"
                " (`id`, `language`, `stance` ) "
                " VALUES (%s,%s,%s) "
                " on  duplicate key  update `stance`=%s ",(tweets_test[i].id,tweets_test[i].language,test_predict[i],test_predict[i],))


