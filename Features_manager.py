__author__ = 'mirko'

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
from scipy.sparse import csr_matrix, hstack



class Features_manager(object):

    def __init__(self):


        return

    def get_stance(self,tweets):

        stance  = []

        for tweet in tweets:
            stance.append(tweet.stance)


        return stance

    def get_gender(self,tweets):

        gender  = []

        for tweet in tweets:
            gender.append(tweet.gender)


        return gender

    #features extractor
    def create_feature_space(self,tweets,featureset,tweet_test=None):


        global_featureset={
            "BoW"  : self.get_BoW_features(tweets,tweet_test),
            "BoP"  : self.get_BoP_features(tweets,tweet_test),
            "BoL"  : self.get_BoL_features(tweets,tweet_test),
            "BoHMc"  : self.get_BoHMc_features(tweets,tweet_test),
            "hashtag" : self.get_hashtag_features(tweets,tweet_test),
            "numhashtag" : self.get_numhashtag_features(tweets,tweet_test),
            "mention"  : self.get_mention_features(tweets,tweet_test),
            "nummention"  : self.get_nummention_features(tweets,tweet_test),
            "punctuation_marks": self.get_puntuaction_marks_features(tweets,tweet_test),
            "SVM_unigrams_word": self.get_SVM_unigrams_word_features(tweets,tweet_test),
            "SVM_ngrams": self.get_SVM_ngrams_features(tweets,tweet_test),
            "SVM_chargrams": self.get_SVM_chargrams_features(tweets,tweet_test),
            "language": self.get_language_features(tweets,tweet_test),
            "#uppercase": self.get_numuppercase_features(tweets,tweet_test),
            "urlredirect": self.get_UrlRedirect_features(tweets,tweet_test),
            "lens": self.get_length_features(tweets,tweet_test),
        }

        if tweet_test is None:
            all_feature_names=[]
            all_feature_index=[]
            all_X=[]
            index=0
            for key in featureset:
                X,feature_names=global_featureset[key]

                current_feature_index=[]
                for i in range(0,len(feature_names)):
                    current_feature_index.append(index)
                    index+=1
                all_feature_index.append(current_feature_index)

                all_feature_names=np.concatenate((all_feature_names,feature_names))
                if all_X!=[]:
                    all_X=csr_matrix(hstack((all_X,X)))
                else:
                    all_X=X

            return all_X, all_feature_names, np.array(all_feature_index)
        else:
            all_feature_names=[]
            all_feature_index=[]
            all_X=[]
            all_X_test=[]
            index=0
            for key in featureset:
                print(key)
                X,X_test,feature_names=global_featureset[key]

                current_feature_index=[]
                for i in range(0,len(feature_names)):
                    current_feature_index.append(index)
                    index+=1
                all_feature_index.append(current_feature_index)

                all_feature_names=np.concatenate((all_feature_names,feature_names))
                if all_X!=[]:
                    all_X=csr_matrix(hstack((all_X,X)))
                    all_X_test=csr_matrix(hstack((all_X_test,X_test)))
                else:
                    all_X=X
                    all_X_test=X_test

            return all_X, all_X_test, all_feature_names, np.array(all_feature_index)

    def get_BoW_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)


        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(tweet.text)

            for tweet in tweet_test:
                feature_test.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names


    def get_BoL_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(' '.join([ "feature_Lemma_"+t.split("\t")[2] if len(t.split("\t"))==3  else " " for t in  tweet.pos ]))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:
                feature.append( ' '.join([ "feature_Lemma_"+t.split("\t")[2] if len(t.split("\t"))==3  else " " for t in  tweet.pos ]))
            for tweet in tweet_test:
                feature_test.append( ' '.join([ "feature_Lemma_"+t.split("\t")[2] if len(t.split("\t"))==3  else " " for t in  tweet.pos ]))



            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names


    def get_BoP_features(self, tweets,tweet_test=None):
        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          lowercase=True,
                                          binary=False,
                                          max_features=500000)
        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                string=""
                for t in  tweet.pos:
                    if len(t.split("\t"))==3:
                        #for t1 in t.split("\t")[1].split("."):

                        string=string+' f_POS_'+t.split("\t")[1].replace(".","")
                feature.append( string )

            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:
                string=""
                for t in  tweet.pos:
                    if len(t.split("\t"))==3:
                        #for t1 in t.split("\t")[1].split("."):

                        string=string+' f_POS_'+t.split("\t")[1].replace(".","")
                feature.append( string )


            for tweet in tweet_test:
                string=""

                for t in  tweet.pos:
                    if len(t.split("\t"))==3:
                        #for t1 in t.split("\t")[1].split("."):

                        string=string+' f_POS_'+t.split("\t")[1].replace(".","")
                feature_test.append( string )

            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names


    def get_BoHMc_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.tags_content)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:
                feature.append(tweet.tags_content)

            for tweet in tweet_test:
                feature_test.append(tweet.tags_content)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names


    def get_UrlRedirect_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)


        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.ulrs.replace(" "," featureredirectURL"))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()
            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:
                feature.append(tweet.ulrs.replace(" "," featureredirectURL"))
            for tweet in tweet_test:
                feature_test.append(tweet.ulrs.replace(" "," featureredirectURL"))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()


            return X_train, X_test, feature_names


    def get_SVM_unigrams_word_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          analyzer="word",
                                          #stop_words="english",
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(tweet.text)

            for tweet in tweet_test:

                feature_test.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names


    def get_SVM_ngrams_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(2,5),
                                          analyzer="char",
                                          #stop_words="english",
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(tweet.text)

            for tweet in tweet_test:

                feature_test.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()


        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          analyzer="word",
                                          #stop_words="english",
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X2 = tfidfVectorizer.transform(feature)

            feature_names2=tfidfVectorizer.get_feature_names()

            return csr_matrix(hstack((X,X2))), np.concatenate((feature_names,feature_names2))

        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(tweet.text)

            for tweet in tweet_test:
                feature_test.append(tweet.text)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train2 = tfidfVectorizer.transform(feature)
            X_test2 = tfidfVectorizer.transform(feature_test)

            feature_names2=tfidfVectorizer.get_feature_names()

            return csr_matrix(hstack((X_train,X_train2))),csr_matrix(hstack((X_test,X_test2))), np.concatenate((feature_names,feature_names2))





    def get_SVM_chargrams_features(self, tweets,tweet_test=None):

        tfidfVectorizer = CountVectorizer(ngram_range=(2,3),
                                          analyzer="char",
                                          #stop_words="english",
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)


        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(tweet.tags_content)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(tweet.tags_content)

            for tweet in tweet_test:

                feature_test.append(tweet.tags_content)


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names



    def get_hashtag_features(self, tweets,tweet_test=None):


        tfidfVectorizer = CountVectorizer(ngram_range=(1,2),
                                          #stop_words="english",
                                          lowercase=True, #true 0.507 false 0.51
                                          binary=True,
                                          max_features=500000)

        if tweet_test is None:
            feature  = []
            for tweet in tweets:

                feature.append(' '.join(re.findall(r"#(\w+)", tweet.text)))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X, feature_names
        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:

                feature.append(' '.join(re.findall(r"#(\w+)", tweet.text)))

            for tweet in tweet_test:

                feature_test.append(' '.join(re.findall(r"#(\w+)", tweet.text)))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()

            return X_train, X_test, feature_names




        feature  = []
        for tweet in tweets:
            feature.append()



        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()


        return X, feature_names

    def get_numhashtag_features(self, tweets,tweet_test=None):


        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"#(\w+)", tweet.text)))

            return csr_matrix(np.vstack(feature)),["feature_numhashtag"]

        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"#(\w+)", tweet.text)))

            for tweet in tweet_test:
                feature_test.append(len(re.findall(r"#(\w+)", tweet.text)))

            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_numhashtag"]





    def get_mention_features(self, tweets,tweet_test=None):


        tfidfVectorizer = CountVectorizer(ngram_range=(1,2),
                                          #stop_words="english",
                                          lowercase=True, #true 0.507 false 0.51
                                          binary=True,
                                          max_features=500000)
        if tweet_test is None:
            feature  = []
            for tweet in tweets:
                feature.append(' '.join(re.findall(r"@(\w+)", tweet.text)))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X = tfidfVectorizer.transform(feature)

            feature_names=tfidfVectorizer.get_feature_names()

            return X,feature_names

        else:
            feature  = []
            feature_test  = []
            for tweet in tweets:
                feature.append(' '.join(re.findall(r"@(\w+)", tweet.text)))
            for tweet in tweet_test:
                feature_test.append(' '.join(re.findall(r"@(\w+)", tweet.text)))


            tfidfVectorizer = tfidfVectorizer.fit(feature)

            X_train = tfidfVectorizer.transform(feature)
            X_test = tfidfVectorizer.transform(feature_test)

            feature_names=tfidfVectorizer.get_feature_names()


        return X_train, X_test,feature_names

    def get_nummention_features(self, tweets,tweet_test=None):


        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"#(\w+)", tweet.text)))

            return csr_matrix(np.vstack(feature)),[""]

        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"@(\w+)", tweet.text)))

            for tweet in tweet_test:
                feature_test.append(len(re.findall(r"@(\w+)", tweet.text)))

            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_mention"]

    def get_numuppercase_features(self, tweets,tweet_test=None):


        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"[A-Z]{1,}", tweet.text)))

            return csr_matrix(np.vstack(feature)),["feature_uppercase"]

        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append(len(re.findall(r"[A-Z]{1,}", tweet.text)))

            for tweet in tweet_test:
                feature_test.append(len(re.findall(r"[A-Z]{1,}", tweet.text)))

            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_uppercase"]



    def get_language_features(self,tweets,tweet_test):

        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append(0 if tweet.language == "ca" else 1)

            return csr_matrix(np.vstack(feature)),["feature_language"]

        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append(0 if tweet.language == "ca" else 1)

            for tweet in tweet_test:
                feature_test.append(0 if tweet.language == "ca" else 1)

            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_language"]


    def get_puntuaction_marks_features(self,tweets,tweet_test):
        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append([
                len(re.findall(r"[!]", tweet.text)),
                len(re.findall(r"[?]", tweet.text)),
                len(re.findall(r"[.]", tweet.text)),
                len(re.findall(r"[,]", tweet.text)),
                len(re.findall(r"[;]", tweet.text)),
                len(re.findall(r"[!?.,;]", tweet.text)),
                ]

            )


            return csr_matrix(np.vstack(feature)),["feature_esclamativo","feature_domanda","feature_punto","feature_virgola","feature_puntovirgola","feature_tutti"]


        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append([
                len(re.findall(r"[!]", tweet.text)),
                len(re.findall(r"[?]", tweet.text)),
                len(re.findall(r"[.]", tweet.text)),
                len(re.findall(r"[,]", tweet.text)),
                len(re.findall(r"[;]", tweet.text)),
                len(re.findall(r"[!?.,;]", tweet.text)),
                ]

            )


            for tweet in tweet_test:
                feature_test.append([
                len(re.findall(r"[!]", tweet.text)),
                len(re.findall(r"[?]", tweet.text)),
                len(re.findall(r"[.]", tweet.text)),
                len(re.findall(r"[,]", tweet.text)),
                len(re.findall(r"[;]", tweet.text)),
                len(re.findall(r"[!?.,;]", tweet.text)),
                ]

            )


            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_esclamativo","feature_domanda","feature_punto","feature_virgola","feature_puntovirgola","feature_tutti"]


    def get_length_features(self,tweets,tweet_test):
        if tweet_test is None:
            feature  = []

            for tweet in tweets:
                feature.append([
                len(tweet.text),
                np.average([len(w) for w in tweet.text.split(" ")]),
                len(tweet.text.split(" ")),

                ]

            )


            return csr_matrix(np.vstack(feature)),["feature_charlen","feature_avgwordleng","feature_numword"]

        else:
            feature  = []
            feature_test  = []

            for tweet in tweets:
                feature.append([
                len(tweet.text),
                np.average([len(w) for w in tweet.text.split(" ")]),
                len(tweet.text.split(" ")),

                ]

            )


            for tweet in tweet_test:
                feature_test.append([
                len(tweet.text),
                np.average([len(w) for w in tweet.text.split(" ")]),
                len(tweet.text.split(" ")),

                ]

            )


            return csr_matrix(np.vstack(feature)),csr_matrix(np.vstack(feature_test)),["feature_charlen","feature_avgwordleng","feature_numword"]

#inizializer
def make_feature_manager():

    features_manager = Features_manager()

    return features_manager

