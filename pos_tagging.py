# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():

 with open("sentences.txt", "r") as f:

        NNS_list = []
        NN_list = []
        noun_list = []
        count = 0

        for line in f:
            words = line.split(" ")
            for w in words:
                x = w.split("|") 
                
                if (x[1] == "NNS"):
                    NNS_list.append(x[0]) 
                elif (x[1] == "NN"):
                    NN_list.append(x[0])

        #lists with no duplicates
        n_NNS_list = list(set(NNS_list))   
        n_NN_list = list(set(NN_list))

        for i in range(len(n_NNS_list)):
            for j in range(len(n_NN_list)):
                if (n_NNS_list[i] == n_NN_list[j]):
                    noun_list.append(n_NNS_list[i]) 
                    break 
        
        #for i in range(len(noun_list)):
        #    print (noun_list[i])

        return list(set(noun_list))  
 

unchanging_plurals_list = unchanging_plurals()

def v_stem(s):

    #If the stem is have, its 3s form is has.
    if s == "has" :
        return "have"

    #If the stem ends in y preceded by a vowel, simply add s (pays, buys).
    elif re.match(r"[A-z]+[aeiou][y]s\b", s):
        str = s[:-1]

    #If the stem ends in y preceded by a non-vowel and contains at least three letters, change the y to ies (flies, tries, unifies).
    elif re.match(r"[A-z]+[^aeiou]ies\b", s):
        str = s[:-3] + 'y'

    #If the stem is of the form Xie where X is a single letter other than a vowel, simply add s (dies, lies, ties note that this doesnt account for unties).
    elif re.match(r"[^aeiou]ies\b", s):
        str = s[:-1]

    #If the stem ends in o,x,ch,sh,ss or zz, add es (goes, boxes, attaches, washes, dresses, fizzes).
    elif re.match(r"[A-z]+([ox]|[cs]h|[s]s|[z]z)es\b", s): 
        str = s[:-2]

    #If the stem ends in se or ze but not in sse or zze, add s (loses, dazes, lapses, analyses).
    elif re.match(r"[A-z]+([s][^s][e]|[z][^z][e])s\b", s):
        str = s[:-1]

    #If the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s (likes, hates, bathes).
    elif re.match(r"[A-z]+([^iosxz]|[^ch]|[^sh])es\b", s):
        str = s[:-1]
    
    #If the stem ends in anything except s,x,y,z,ch,sh or a vowel, add s (eats, tells, shows)
    elif re.match(r"[A-z]+([^sxyzaeiou]|[^cs]h)s\b", s):
        str = s[:-1]

    else: 
        str = ""

    return str


def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    
    if s in unchanging_plurals_list:
        return s
    elif s[-3:] == "men":
        return s[:-3] + "man"
    else: 
        if v_stem(s) in unchanging_plurals_list: #calls helper function v_stem
            return ""
        else:
            return v_stem(s)
    

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    
    #lexicon, verb stem, noun stem, tagged_functions_words/function_word_tag
    s_tags = []
    tags = []
    tagset = ['P', 'N', 'A', 'I', 'T']

    for x in tagset:
        s_tags += [x for w in lx.getAll(x) or [] if w == wd]
        s_tags += [x for v in lx.getAll(x) or [] if v == verb_stem(wd)]
        s_tags += [x for n in lx.getAll(x) or [] if n == noun_stem(wd)]

    if wd in function_words:
        tags += [t for (w, t) in function_words_tags if w == wd]

    if 'P' in s_tags:
        tags += ['P']

    if 'N' in s_tags:
        if wd in unchanging_plurals_list:
            tags += ['Np', 'Ns']
        elif noun_stem(wd):
            tags += ['Np']
        else:
            tags += ['Ns']

    if 'A' in s_tags:
        tags += ['A']

    if 'I' in s_tags:
        if verb_stem(wd):
            tags += ['Is']
        else:
            tags += ['Ip']

    if 'T' in s_tags:
        if verb_stem(wd):
            tags += ['Ts']
        else:
            tags += ['Tp']

    return tags
 

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.



if __name__ == "__main__":

    lx = Lexicon()
    lx.add("John","P")
    lx.add("Mary","P") 
    lx.add("fish","T")
    lx.add("fish","N")
    lx.add("fish","I")
    lx.add("orange", "N")
    lx.add("orange", "A")
   # lx.getAll("T")
    print (noun_stem("sheeps"))
    print (noun_stem("women"))
    print (tag_word(lx,"John")) # returns ["P"]
    print (tag_word(lx,"orange")) # returns ["Ns","A"]
    print (tag_word(lx,"fish")) # returns ["Ns","Np","Ip","Tp"]
    print (tag_word(lx,"a")) # returns ["AR"]
    print (tag_word(lx,"zxghqw")) # returns []
    #print (tag_words(lx, ["John", "fish"]))
    #print (noun_stem("smashes"))
    #print (unchanging_plurals_list)
