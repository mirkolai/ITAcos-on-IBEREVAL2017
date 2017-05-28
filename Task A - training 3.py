__author__ = 'mirko'
import numpy
import Features_manager
import Database_manager
from sklearn.cross_validation import KFold
from collections import Counter
import pymysql
import config as cfg
from sklearn.metrics.classification import precision_recall_fscore_support, accuracy_score
from itertools import combinations
from sklearn.linear_model.logistic import LogisticRegression


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

print("Task A - Test 3")

database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()
tweets=numpy.array(database_manager.return_training())
stances=numpy.array(feature_manager.get_stance(tweets))

for language in ["es","ca"]:

    count = Counter(stances)
    
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
    X,feature_name_global,feature_index_global=feature_manager.create_feature_space(tweets,feature_names)
    
    
    features_set=numpy.array([
    #["BoW","BoL","SVM_chargrams","urlredirect","BoHMc","numhashtag","#uppercase"],
    ["BoW","BoL","BoP","SVM_chargrams","urlredirect","hashtag","numhashtag","lens"],
    #["BoW","BoL","BoP","SVM_chargrams","urlredirect","numhashtag","language","lens"],
    #["BoW","BoL","BoP","SVM_chargrams","urlredirect","numhashtag","punctuation_marks","lens"],
    #["BoW","BoL","BoP","SVM_chargrams","urlredirect","hashtag","punctuation_marks","language"],
    ])
    
    clfs={
          "lg": {"clf":LogisticRegression()},
          #"svm":{"clf":SVC(kernel='linear')},
          #"dt":{"clf":DecisionTreeClassifier()},"rf":{"clf":RandomForestClassifier()},"aamnb":{"clf":MultinomialNB()}}#"nb":{"clf":GaussianNB()}
          }
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
            X_filter=X[:,feature_index_filtered]
    
            print(X_filter.shape)
    
            kf = KFold(len(tweets),n_folds=10, shuffle=True, random_state=0)
    
            fmacros=[]
            for index_train, index_test in kf:
    
                X_train=X_filter[index_train]
                X_test=X_filter[index_test]
    
                for clfname,clf in clfs.items():
    
                    clf["clf"].fit(X_train,stances[index_train])
    
                    test_predict = clf["clf"].predict(X_test)
                    print(clfname)
    
                    for i in range(0,len(tweets[index_test])):
    
                        if (tweets[index_test])[i].id in agreement:
                            if test_predict[i] in agreement[(tweets[index_test])[i].id]:
                                agreement[(tweets[index_test])[i].id][test_predict[i]]+=1
                            else:
                                agreement[(tweets[index_test])[i].id][test_predict[i]]=1
                        else:
                            agreement[(tweets[index_test])[i].id]={test_predict[i]:1}
    
                print("kfol")
    
    
    for k, value in agreement.items():
        print(k, value)
    
    majority_voting=[]
    stance_language=[]
    for i in range(0,len(tweets)):

        if tweets[i].language==language:

            stance_language.append(stances[i])
            gender=""
            support=0
            annotators=0

            for k, value in agreement[(tweets[i]).id].items():
                annotators+=value
                if value>support:
                    support=value
                    gender=k

            majority_voting.append(gender)
    
    
    
    prec, recall, f, support = precision_recall_fscore_support(
    stance_language,
    majority_voting,
    beta=1)
    
    accuracy = accuracy_score(
    stance_language,
    majority_voting
    )
    
    print(prec,recall,f,support,accuracy)
    print(((f[0]+f[1])/2))
    count = Counter(stances)
    print(count)
    count = Counter(majority_voting)
    print(count)



    file = open("Task A - training 3 "+language+".csv","a")
    file.write(str(prec)+","+str(recall)+","+str(f)+","+str(support)+","+str(accuracy)+","+str(((f[0]+f[1])/2))+"\n")
    file.close()


