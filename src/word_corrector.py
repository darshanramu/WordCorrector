#!/usr/bin/python

from sklearn import svm
import sys
import nltk
import utility

if len(sys.argv) == 3:
	test_filename = sys.argv[1]
	output_filename = sys.argv[2]
else:
	print "Invalid Arguments. Usage: ./word_corrector.py TESTFILE OUTPUTFILE"
	sys.exit()

callutility = utility.Mainclass()
classifiers = []
with open("gutenberg_model") as f:
	line = f.readline()
	tokens = line.split(' ')
	no_of_tags = int(tokens[1])
	for tag_index in range(0, no_of_tags):
   		line = f.readline()
    		tokens = line.split(' ')
    		callutility.pos_tags[tokens[0]] = int(tokens[1])
	for type_index in range(0,5):
    		line = f.readline()
    		tokens = line.split(' ')
    		no_of_samples = int(tokens[3])
    		for sample_index in range(0, no_of_samples):
        		line = f.readline()
        		tokens = line.split(' ')
       	 		callutility.wordtypes[type_index].labels.append(int(tokens[0]))
    		for sample_index in range(0, no_of_samples):
        		line = f.readline()
        		tokens = line.split(' ')
        		features = [int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])]
        		callutility.wordtypes[type_index].training.append(features)


for wtype in callutility.wordtypes:
	classifier = svm.SVC(kernel='linear')
	classifier.fit(wtype.training, wtype.labels)
	classifiers.append(classifier)

with open(test_filename) as testfile:
	raw_text = testfile.read()

raw_text_index = 0

tok_dump=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
tok_sen = tok_dump.tokenize(raw_text)

with open(output_filename, 'w+') as outfile:
	for i,sentence in enumerate(tok_sen):
	    s = sentence.replace('\n', ' ').replace('\r', ' ')
	    s = s.strip()
	    rwords = s.split(' ')
	    words = []

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
    		#w = w.replace("'", '')
        	if not w:
            		continue
        	words.append(w)

    	
    	    pos_tagged_words = nltk.pos_tag(words)
    	    len_words = len(words)

    	    for i, w in enumerate(words):
        	while(raw_text[raw_text_index].lower() != w[0]):
           		 raw_text_index += 1
        
        	#Take prev two tags and next two tags
        	wtype = callutility.gettype(w)
        	if  wtype != -1:
           		wclass = callutility.getclass(w)
    			if i > 1:
               			 prev2tag = pos_tagged_words[i-2][1]
           		else:
             	   		prev2tag = "notag"
           	    	if i > 0:
			        prevtag = pos_tagged_words[i-1][1]
			else:
		        	prevtag = "notag"
		        if i < (len_words-1):
		    		posttag = pos_tagged_words[i+1][1]
		    	else:
		        	posttag = "notag"
		        if i < (len_words-2):
		    		post2tag = pos_tagged_words[i+2][1]
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
            		#TODO: Words also as features
            		features = [callutility.searchtag(prev2tag), callutility.searchtag(prevtag), callutility.searchtag(posttag), callutility.searchtag(post2tag)]
	    		#features = [callutility.searchtag(prevtag), callutility.searchtag(posttag)]
            
            		classification = classifiers[wtype].predict(features)
           
            		if classification != wclass:
               			correction = callutility.searchword(wtype, classification)
 				first_half = raw_text[:raw_text_index]
				second_half = raw_text[(raw_text_index + len(w)):]
				raw_text = first_half + correction + second_half
 				raw_text_index += len(correction)
			else:
				raw_text_index += len(w)
       		else:
             		raw_text_index += len(w)


	outfile.write(raw_text)

       



