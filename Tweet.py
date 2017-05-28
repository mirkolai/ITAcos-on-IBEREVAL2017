__author__ = 'mirko'

import re
import treetaggerwrapper
from nltk.stem.porter import PorterStemmer
from urllib.request import urlopen

from Linguistic_resource_wordlist import WORDLIST

wordlist = WORDLIST()


porter_stemmer = PorterStemmer()

treetaggerwrapper.g_langsupport["ca"]={
        "encoding": "utf-8",
        "tagparfile": "catalan-utf8.par",
        "abbrevfile": "",
        "pchar": treetaggerwrapper.ALONEMARKS + "'",
        "fchar": treetaggerwrapper.ALONEMARKS + "'",
        "pclictic": "",
        "fclictic": "",
        "number": treetaggerwrapper.NUMBER_EXPRESSION,
        "dummysentence": "Felicitats pel nou títol mundial @noramurla, i a tota la família",
        "replurlexp": 'sustituir-url>',
        "replemailexp": 'sustituir-email',
        "replipexp": 'sustituir-ip',
        "repldnsexp": 'sustituir-dns'
    }

tagger = { "es" : treetaggerwrapper.TreeTagger(TAGLANG="es") , "ca" : treetaggerwrapper.TreeTagger(TAGLANG="ca") }


class Tweet(object):

    id=""
    content=""
    language=""
    stance=""
    gender=""

    def __init__(self, id, content,language, stance, gender):


        self.id=id

        self.text=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' URL ', content)
        self.row_text=content
        self.ulrs=self.getLongUrl(content)


        self.language=language
        self.pos = tagger[language].tag_text(content)
        self.tags_content=wordlist.ParseSentence(content)
        self.stance=stance
        self.gender=gender


    def getLongUrl(self,content):

        newcontent=""

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)

        for url in urls:
            try:
                response = urlopen(url)
                html = response.geturl()
                newcontent=newcontent+" "+html.split("/")[2].replace("."," ")
            except:
                newcontent=newcontent+"NotFound"
                print("Error: not found")
                pass

        if len(newcontent)==0:
            newcontent="NOURL"

        print(newcontent)

        return newcontent

def make_tweet(id, content,language, stance, gender):

    tweet = Tweet(id, content,language, stance, gender)

    return tweet



