# coding: utf-8

# we're gonna need firebase for now
import firebase as firebase

# importing NLTK stuff
# import nltk
# from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer

# importing json
# import json

# PATTERNS
# from pattern.en import parsetree
# from pattern.en import tenses, PAST, PL

# IMPORTING STUFF
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer

# SCIKIT-LEARN IMPORTS
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer

# IMPORTING PICKLE
import pickle

# IMPORTING FROM IMPORTS
from GetInfo import GetInfo, Relavence


# In[215]:

class ActivityClassifier():
    def __init__(self, app_name):
        """
        :param app_name: The name of the package!
        """
        self.firebase = firebase.FirebaseApplication('https://sail-857f9.firebaseio.com/', None)
        self.database = self.firebase.get('/packages/' + app_name, None)
        self.app_name = app_name
        self.models = {}
        self.transformers = {}
        self.whys = {}
        self.tokenizer = PunktSentenceTokenizer()

    def train(self, user_name):
        """
        :return: None
        """
        for i in self.database['activities']:
            X = []
            Y = []

            self.buckets_at_this_level = {i: [self.database['bucket'][i][j] for j in self.database['bucket'][i]] for i
                                          in
                                          self.database['activities'][i]['views'].keys()}
            for y in self.buckets_at_this_level:
                for j in self.buckets_at_this_level[y]:
                    X.append(j)
                    Y.append(y)
            d = CountVectorizer()
            X = d.fit_transform(X)
            graph = LinearSVC()
            print graph.fit(X, Y)
            self.models[i] = graph
            self.transformers[i] = d
            new_list = []
            for tag in Y:
                if tag not in new_list:
                    new_list.append(tag)
            new_list.sort()
            self.whys[i] = new_list
            self.r = Relavence(self.database['bucket'])
        pickle.dump(self, open(user_name + '_' + self.app_name + '.pickle', "wb"))

    def transition(self, current_activity, statement):
        """

        :param current_activity:
        :param statement:
        :return:
        """
        g = GetInfo()
        tokenized = self.tokenizer.tokenize(statement)
        parts = []
        particles = ""
        for sentence in tokenized:
            for i in pos_tag(word_tokenize(sentence)):
                if i[1] == 'CC':
                    parts.append(particles)
                    particles = ""
                else:
                    particles = particles + i[0] + ' '
            parts.append(particles)
            particles = ""
        return_tuple = []
        for i in parts:
            print "here"
            ret = self.models[current_activity].predict(
                self.transformers[current_activity].transform([i]))
            return_tuple.append(({"id":ret[0],"info":g.get_info(i),"split_string":i}))
            if self.database['transitions'].has_key(ret[0]):
                current_activity = self.database['transitions'][ret[0]]
        return {"return_list":return_tuple,"confident":self.r.predict(statement)[0]}