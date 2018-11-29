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
        
        return list(set(noun_list))  
 

unchanging_plurals_list = unchanging_plurals()


def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    
    if s in unchanging_plurals_list:
        return s
    elif s[:-3] == "men":
        return s[:-3] + "man"
    else:
        # calls verb_stem from statements.py
        try:
            return verb_stem(s)
        except KeyError:
            return False


def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    
    #lexicon, verb stem, noun stem, tagged_functions_words/function_word_tag
    s_tags = []
    tags = []
    tagset = ['P', 'N', 'A', 'I', 'T']


    for tag in tagset:
        s_tags += [tag for w in lx.getAll(tag) or [] if w == wd]
        s_tags += [tag for v in lx.getAll(tag) or [] if v == verb_stem(wd)]
        s_tags += [tag for n in lx.getAll(tag) or [] if n == noun_stem(wd)]

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
    print (tag_word(lx,"John")) # returns ["P"]
    print (tag_word(lx,"orange")) # returns ["Ns","A"]
    print (tag_word(lx,"fish")) # returns ["Ns","Np","Ip","Tp"]
    print (tag_word(lx,"a")) # returns ["AR"]
    print (tag_word(lx,"zxghqw")) # returns []
    #print (tag_words(lx, ["John", "fish"]))
    #print (noun_stem("smashes"))
    #print (unchanging_plurals_list)
