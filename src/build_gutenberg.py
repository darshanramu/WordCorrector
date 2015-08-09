#!/usr/bin/python

import sys
import os
import nltk
import utility

with open("gutenberg_full.txt", 'w+') as gf:
	for file in os.listdir("gutenberg_corpora"):
        	with open("gutenberg_corpora/" + file) as ipf:
                    for line in ipf:
                        gf.write(line)
#print "Gutenberg Corpora Created"

fulltext = open("gutenberg_full.txt")
replaced_text = fulltext.read().replace('\n', ' ').replace('\r', ' ')
fulltext.close()
tok_dump=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
tok_sen = tok_dump.tokenize(replaced_text)
callutility = utility.Mainclass()
for s in tok_sen:
     words = []
     rwords = s.split(' ')
     for w in rwords:
            if w.isspace():
                continue
            w = w.lower()
            w = w.replace('.', '')
            w = w.replace('?', '')
            w = w.replace(',', '')
            w = w.replace(';', '')
            w = w.replace(':', '')
            w = w.replace('"', '')
            #w = w.replace("'", '') this removes the input formatting
            if not w:
                continue
            words.append(w)
            
     no_of_words = len(words)
     taggedpos = nltk.pos_tag(words)
        
     for i, w in enumerate(words):
            wtype = callutility.gettype(w)
            if  wtype != -1:
                wclass = callutility.getclass(w)
                if i > 1:
                    prev2tag = taggedpos[i-2][1]
                else:
                    prev2tag = "notag"
                if i > 0:
                    prevtag = taggedpos[i-1][1]
                else:
                    prevtag = "notag"
                if i < (no_of_words-1):
                    posttag = taggedpos[i+1][1]
                else:
                    posttag = "notag"
                if i < (no_of_words-2):
                    post2tag = taggedpos[i+2][1]
                else:
                    post2tag = "notag"
                #if i > 0:
                #    prevtag = taggedpos[i-1][1]
                #else:
                #    prevtag = "notag"
                #if i < (no_of_words-1):
                #    posttag = taggedpos[i+1][1]
                #else:
                #    posttag = "notag"
                
                features = [callutility.searchtag(prev2tag), callutility.searchtag(prevtag), callutility.searchtag(posttag), callutility.searchtag(post2tag)]
                #features = [callutility.searchtag(prevtag), callutility.searchtag(posttag)]
                callutility.appendtypes(wtype, wclass, features)

#print "create gutenberg_model"
callutility.writemodel("gutenberg_model")


