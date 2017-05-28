__author__ = 'mirko'
import re

class WORDLIST(object):


    def __init__(self):

        return

    def ParseSentence(self,sentence):
        new_sentence = "" # output

        hashtags= re.findall('[#][A-Za-z]*', sentence)
        mentions= re.findall('[@][A-Za-z]*', sentence)

        for hashtag in hashtags:
            new_sentence=new_sentence+" "+self.ParseTag(hashtag)

        for mention in mentions:
            new_sentence=new_sentence+" "+self.ParseTag(mention)


        return new_sentence





    def ParseTag(self, tag):
        words = re.findall('[A-Z][a-z]*', tag)
        return " ".join(words)


if __name__ == '__main__':

    sentence="@CatalunaesEspana @HolaaTosos"
    wordlist=WORDLIST()

    result=wordlist.ParseSentence(sentence)
    print(result)
