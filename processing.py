import ast
import re, math
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize

## find the relevance documents
# parameter : queryVector : list  , diction : dict => dictionary represent vectors
import vectorMath


def find_relevance_documents(queryVector, diction):
    result = {}
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector = list(value_dic.values())
        result.update({key_dic: vectorMath.angle_between_two_vector(queryVector, vector)})
    return result


# remove stop words
# parameters  :  t => tokens have stop words  , st => stop word
def remove_stop_words(t, st):
    clean_data = []
    for w in t:
        if w not in st:
            clean_data.append(w)

    return clean_data


# return two list : list for verbs and list for nouns
# parameters : s => string
def filter_verbs_nouns(s):
    train = state_union.raw("2005-GWBush.txt")
    # sample_text = open("corpus/1.txt", "r").read()
    # print(s)
    cust = PunktSentenceTokenizer(train)
    tok = cust.tokenize(s)

    # tokenized_word = word_tokenize(sample_text)
    # print(len(tokenized_word))
    # print(tokenized_word)
    verbs = []
    nouns = []
    for i in tok:
        words = nltk.word_tokenize(i)
        tag = nltk.pos_tag(words)
        for c in tag:
            # print(c[0])
            if c[1] == "VBD" or c[1] == "VBG" or c[1] == "VBN" or c[1] == "VBN" or c[1] == "VBP" or c[1] == "VBZ" or \
                    c[1] == "VP":
                verbs.append(c[0])
            else:
                nouns.append(c[0])

            # print(c[0])
            # print(c)

    return [verbs, nouns]


## regEX for phones
# (\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})
# 000-000-0000
# 000 000 0000
# 000.000.0000

# (000)000-0000
# (000)000 0000
# (000)000.0000
# (000) 000-0000
# (000) 000 0000
# (000) 000.0000
#
# 000-0000
# 000 0000
# 000.0000
#
# 0000000
# 0000000000
# (000)0000000

## regEX for emails
# \w+@\w+[.]\w+

## regEX for dates
# (0[1-9]|[12]\d|3[01])[/.-](0[1-9]|1[012])[/.-](\d{4})
# (0[1-9]|[12]\d|3[01])[/.-](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/.-](\d{4})
# (0[1-9]|[12]\d|3[01])[/.-](January|February|March|April|May|June|July|August|September|October|November|December)[/.-](\d{4})

def convert_to_regular_date(s):
    # s is output ==>   re.findall("regEx",str)
    _date = []
    s1 = ""
    for d in s:
        s1 = d[0]
        s1 += "-"
        if d[1] == "01" or d[1] == "January":
            s1 += "Jan"
        elif d[1] == "02" or d[1] == "February":
            s1 += "Feb"
        elif d[1] == "03" or d[1] == "March":
            s1 += "Mar"
        elif d[1] == "04" or d[1] == "April":
            s1 += "Apr"
        elif d[1] == "05" or d[1] == "May":
            s1 += "May"
        elif d[1] == "06" or d[1] == "June":
            s1 += "Jun"
        elif d[1] == "07" or d[1] == "July":
            s1 += "Jul"
        elif d[1] == "08" or d[1] == "August":
            s1 += "Aug"
        elif d[1] == "09" or d[1] == "September":
            s1 += "Sep"
        elif d[1] == "10" or d[1] == "October":
            s1 += "Oct"
        elif d[1] == "11" or d[1] == "November":
            s1 += "Nov"
        elif d[1] == "12" or d[1] == "December":
            s1 += "Dec"
        else:
            s1 += d[1]

        s1 += "-{}".format(d[2])
        _date.append(s1)
    return _date


####################################################################
##  to read file and convert it to dict :
# import ast
# f = open("x.txt", "r")
# t = f.read()
# f.close()
# print(type(t))
#
# res = dict(ast.literal_eval(t))
# print(type(res))
#
# print(res)

######################################################################


def build_vec_mod():
    # read stop words
    f = open("stop words.txt", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)
    # print(stop_words)
    # read files in corpus Folder
    tokines = []  # contait all terms for all docs
    termsInAfile = []  # this contain all terms in current file without stop words
    diction = {}  # dictionary for all tokens

    for x in range(1, 424):
        f = open("corpus/{}.txt".format(x), "r")
        contentAFile = f.read()
        f.close()
        ## processing dates
        # extract dates from string
        dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                           "(0[1-9]|1[012])"
                           "[/.-](\d{4})", contentAFile)
        dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                                "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                                "[/.-](\d{4})", contentAFile))
        dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                                "(January|February|March|April|May|June|July|August|September|October|November|December)"
                                "[/.-](\d{4})", contentAFile))
        years = re.findall("\d{4}", contentAFile)

        # remove dates from string
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(0[1-9]|1[012])"
                              "[/.-](\d{4})", "", contentAFile)
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                              "[/.-](\d{4})", "", contentAFile)
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(January|February|March|April|May|June|July|August|September|October|November|December)"
                              "[/.-](\d{4})", "", contentAFile)
        contentAFile = re.sub("\d{4}", "", contentAFile)
        # convert dates to regular form 01-Mar-2020
        dates = convert_to_regular_date(dates)

        ## processing emails
        # extract emails from string in contentAFile
        emails = re.findall("\w+@\w+[.]\w+", contentAFile)
        # remove emails from string
        contentAFile = re.sub("\w+@\w+[.]\w+", "", contentAFile)

        ## processing phones
        # extract phones from string in contentAFile
        phones = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                            "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                            "\d{3}[-\.\s]??\d{4})", contentAFile)
        # remove phones from string
        contentAFile = re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                              "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                              "\d{3}[-\.\s]??\d{4})", "", contentAFile)

        verbs_nounes = filter_verbs_nouns(contentAFile)
        verbs = remove_stop_words(verbs_nounes[0], stop_words)
        nounes = remove_stop_words(verbs_nounes[1], stop_words)

        #######################################################################

        lmtzr = WordNetLemmatizer()
        lemmatizedVerbs = []
        for v in verbs:
            lemmatizedVerbs.append(WordNetLemmatizer().lemmatize(v, 'v'))

        verbs = lemmatizedVerbs

        porter = PorterStemmer()
        porteredNouns = []
        for n in nounes:
            porteredNouns.append(porter.stem(n))

        nounes = porteredNouns

        ################################################################

        # tokenized_word = word_tokenize(contentAFile)

        # tokenized_word.extend(dates)
        # tokenized_word.extend(years)
        # tokenized_word.extend(emails)
        # tokenized_word.extend(phones)

        termsInAfile.extend(verbs)
        termsInAfile.extend(nounes)
        termsInAfile.extend(years)
        termsInAfile.extend(phones)
        termsInAfile.extend(dates)
        termsInAfile.extend(emails)

        for w in termsInAfile:
            if w not in tokines:
                tokines.append(w)

        temp_dic = {}  # dictionary for each term
        for y in termsInAfile:
            temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})

        diction.update({x: temp_dic})
        print("document number : {} Done".format(x))
        termsInAfile.clear()

    # Extension of the previous diction in order to contain all terms
    # and show their repetition within the document
    for a in range(1, 424):
        temp_dic2 = diction.get(a).copy()
        diction.get(a).clear()
        # print(temp_dic2)
        # for y in list(dict.fromkeys(tokines)):
        for y in tokines:
            if y not in temp_dic2.keys():
                diction.get(a).update({y: 0.0})
            else:
                diction.get(a).update({y: temp_dic2[y]})

    f1 = open("vector model.txt", "w")
    f1.write(str(diction))
    f1.close()

    f2 = open("terms.txt", "w")
    f2.write(str(tokines))
    f2.close()
    print(len(tokines))
    return diction
