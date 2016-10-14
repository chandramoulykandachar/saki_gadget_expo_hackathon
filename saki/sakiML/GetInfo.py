# importing NLTK stuff
from nltk.tag import pos_tag
from nltk import word_tokenize

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC


class Relavence():
    def __init__(self, buckets):
        mn_list = []
        Y = []
        d = CountVectorizer()
        for i in buckets:
            for j in buckets[i]:
                mn_list.append(buckets[i][j])
                Y.append('yes')
        list_of_nons = pickle.load(open("irrilavent", "rb"))
        try:
            list_of_nons = list_of_nons[:len(mn_list)]
        except Exception as e:
            pass
        for i in list_of_nons:
            mn_list.append(i)
            Y.append('no')
        self.s = LinearSVC()
        h = d.fit_transform(mn_list)
        self.s.fit(h, Y)
        self.d = d

    def predict(self, string):
        return self.s.predict(self.d.transform([string]))


class GetInfo():
    def get_info(self, string):
        """
        Returns the required data from the given string
        :param string: the string from which the data needs to be extracted
        :return: the words that occur after an interjection which is usually the information in the given string
        """

        tagged = pos_tag(word_tokenize(string))
        temp_string = ""
        list_of_vals = []

        for i in tagged:
            if i[1] == 'IN' or i[1] == 'VBZ':
                list_of_vals.append(temp_string)
                temp_string = ''
            else:
                temp_string = temp_string + i[0] + ' '
        list_of_vals.append(temp_string)
        del temp_string

        if list_of_vals[-1] == '' and len(list_of_vals) != 1:
            return i[0]
        if len(list_of_vals) == 1:
            return None

        return list_of_vals[-1]
