# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:

    """stores known word stems of various part-of-speech categories"""
    """storing new word stems as we encounter them """

    def __init__(self):
        self.lx = {}

    def add(self, stem, cat):
        """for adding a word stem with a given part-of-speech category """

        if cat not in self.lx:
            self.lx[cat] = [] 
            self.lx[cat] += [stem]
        else:
            self.lx[cat] += [stem]

    def getAll(self, cat):
        """which returns all known word stems of a given category."""
        if cat in self.lx:
            return (((self.lx[cat]))) #pront
        else:
            []

    #"P" proper names (John, Mary)
    #"N" common nouns (duck, student)
    #"A" adjectives (purple, old)
    #"I" intransitive verbs (fly, swim)
    #"T" transitive verbs (like, hit)


class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.fb = {}

    def addUnary(self, pred, e1):
        # duck(John)
        if pred not in self.fb:
            self.fb[pred] = []
            self.fb[pred] += [e1]
        else:
            self.fb[pred] = []

    def addBinary(self, pred, e1, e2):
        # love(John, Mary)
        if pred not in self.fb:
            self.fb[pred] = {}
            if e1 not in self.fb[pred]:
                self.fb[pred][e1] = []
                self.fb[pred][e1] += [e2]
        elif (pred in self.fb and e1 not in self.fb[pred]):
            self.fb[pred][e1] += [e2]
        else:
            self.fb[pred][e1][e2] = []

    def queryUnary(self, pred, e1):
        try:
            return e1 in self.fb[pred]
        except KeyError:
            return False
            

    def queryBinary(self, pred, e1, e2):
        try:
            return e2 in self.fb[pred][e1]
        except KeyError:
            return False


import re
from nltk.corpus import brown 
b = brown.tagged_words()
vb = [(w, t) for (w, t) in b if (t == "VB" or t == "VBZ")]

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
   
    #If the stem is have, its 3s form is has.
    if s == "has" :
        str = "have"
    
    #If the stem ends in anything except s,x,y,z,ch,sh or a vowel, add s (eats, tells, shows)
    elif re.match(r"[A-z]+([^sxyzaeiou]|[^cs]h)s\b", s):
        str = s[:-1]

    #If the stem ends in y preceded by a vowel, simply add s (pays, buys).
    elif re.match(r"[A-z]+[aeiou][y]s\b", s):
        str = s[:-1]

    #If the stem ends in y preceded by a non-vowel and contains at least three letters, change the y to ies (flies, tries, unifies).
    elif re.match(r"[A-z]+[^aeiou]ies\b", s):
        str = s[:-3] + 'y'

    #If the stem is of the form Xie where X is a single letter other than a vowel, simply add s (dies, lies, ties — note that this doesn’t account for unties).
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

    else: 
        str = ""


    hits  = [(w, t) for (w, t) in vb if (w == s or w == str)]

    ts = [(w, t) for (w, t) in hits if w == s and t == 'VBZ']

    if ts:
        return str
    else:
        tstr = [t for (w, t) in hits if w == str and t == 'VB']
    if not (ts or tstr):
        str = ""
    return str
   


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.



# Test
if __name__ == "__main__":
    """
    lx = Lexicon()
    lx.add("John","P")      #P
    lx.add("Mary","P")      #P
    lx.add("duck", "N")     #P  
    lx.add("student", "N")  #N
    lx.add("old", "A")      #A
    lx.add("fly", "I")      #I
    lx.add("hit","T")       #T
    lx.add("hits","T")      #T
    lx.add("likes","T")     #T
    print (lx.getAll("T"))
    print (lx.getAll("VBZ")) #error

    fb = FactBase()
    fb.addUnary("duck","John")
    fb.addBinary("love","John","Mary")
    print (fb.queryUnary("duck","John"))            # returns True
    print (fb.queryBinary("love","Mary","John"))    # returns False    
    """
    

    print((verb_stem("eats")))
    print((verb_stem("tells")))
    print((verb_stem("pays")))
    print((verb_stem("buys")))
    print((verb_stem("flies")))
    print((verb_stem("tries")))
    print((verb_stem("unifies")))
    print((verb_stem("dies")))
    print((verb_stem("lies")))
    print((verb_stem("goes")))
    print((verb_stem("attaches")))
    print((verb_stem("dresses")))
    print((verb_stem("dazes")))   
    print((verb_stem("analyses")))
    print((verb_stem("loses")))
    print((verb_stem("has"))) 
    print((verb_stem("says")))
    print((verb_stem("likes")))
    print((verb_stem("bathes")))
    print((verb_stem("hates"))) 
    print((verb_stem("unties"))) 
    print((verb_stem("says")))