

# importing NLTK stuff
from nltk.tag import pos_tag
from nltk import word_tokenize


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

        if list_of_vals[-1] == '' and len(list_of_vals) !=1:
            return i[0]
        if len(list_of_vals) == 1:
            return None

        return list_of_vals[-1]