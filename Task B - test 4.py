__author__ = 'mirko'
import numpy
import Features_manager
import Database_manager
import pymysql
import config as cfg
from itertools import combinations
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import  MultinomialNB
from sklearn.svm.classes import SVC
from sklearn.tree.tree import DecisionTreeClassifier

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

print("Task B - Test 4")

database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()

tweets_train=numpy.array(database_manager.return_training())
gender_train=numpy.array(feature_manager.get_gender(tweets_train))

tweets_test=numpy.array(database_manager.return_test())

feature_names=numpy.array([
               "BoW",
               "BoL",
               "BoP",
               "SVM_chargrams",
               "urlredirect",
               "BoHMc",
               "hashtag",
               "mention",
               "numhashtag",
               "nummention",
               "punctuation_marks",
               "language",
               "#uppercase",
               "lens",
    ])
features_set=numpy.array([
["BoW","BoL","SVM_chargrams","urlredirect","BoHMc","numhashtag","#uppercase"]])

X_train,X_test,feature_name_global,feature_index_global=feature_manager.create_feature_space(tweets_train,feature_names,tweets_test)


clfs={"lg": {"clf":LogisticRegression()},"svm":{"clf":SVC(kernel='linear')},"dt":{"clf":DecisionTreeClassifier()},"rf":{"clf":RandomForestClassifier()},"aamnb":{"clf":MultinomialNB()}}#"nb":{"clf":GaussianNB()}}
agreement={}
stuff = range(0, len(features_set) )
for L in range(1, 1+1):
    for subset in combinations(stuff, L):

        print(list(subset))
        feature_filtered=numpy.concatenate(features_set[list(subset)])
        feature_index_filtered=numpy.array([list(feature_names).index(f) for f in feature_filtered])
        feature_index_filtered=numpy.concatenate(feature_index_global[list(feature_index_filtered)])

        print(feature_filtered)#,feature_index_filtered)
        print(len(feature_index_global))
        X_train_filter=X_train[:,feature_index_filtered]
        X_test_filter=X_test[:,feature_index_filtered]


        for clfname,clf in clfs.items():

            clf["clf"].fit(X_train,gender_train)

            test_predict = clf["clf"].predict(X_test)

            for i in range(0,len(tweets_test)):

                if (tweets_test)[i].id in agreement:
                    if test_predict[i] in agreement[tweets_test[i].id]:
                        agreement[tweets_test[i].id][test_predict[i]]+=1
                    else:
                        agreement[tweets_test[i].id][test_predict[i]]=1
                else:
                    agreement[tweets_test[i].id]={test_predict[i]:1}



for k, value in agreement.items():
    print(k, value)

majority_voting=[]
for i in range(0,len(tweets_test)):
    gender=""
    support=0
    annotators=0

    for k, value in agreement[(tweets_test[i]).id].items():
        annotators+=value
        if value>support:
            support=value
            gender=k

    majority_voting.append(gender)


for i in range( 0,len(tweets_test)):
    print(majority_voting[i])
    print(tweets_test[i].id)
    cur.execute(" INSERT INTO `test_4`"
                " (`id`, `language`, `gender` ) "
                " VALUES (%s,%s,%s) "
                " on  duplicate key  update `gender`=%s ",(tweets_test[i].id,tweets_test[i].language,majority_voting[i],majority_voting[i],))


