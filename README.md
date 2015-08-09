Word corrector performs grammar corrections for the words it's/its, your/you're, lose/loose, their/they're
and to/too which are used in a wrong context of a sentence. The program uses class prediction based on POS tags .
Previous two tags and next two tags are used as features. Later SVM linear kernel matrix is used to classify 
which class among two classes(its/it's and so on) does the word belong. Gutenberg corpora is merged to a single 
file and nltk tokenizer is used to tokenize it and POS tagger of nltk is used to perform tagging on the gutenberg
training set. Number of tags found per each POS tag type and also encoding for different POS type is used to 
represent the features in the model per class type (for eg., its vs it's). Later the testfile is also tokenized using same 
english.pickle and POS tagged. Later using the same prev two tags and next two tags, the tag is predicted using SVM 
classifier for a test file word when it is one of "it's/its" and so on. If the predicted class is different then "it's"
might be replaced with "its" and similarly for others.

Usage:
------
./word_corrector TESTFILENAME   OUTPUTFILENAME

./build_guteberg; To generate gutenberg model file used by the classifier, requires all files to be under "gutenberg_corpora" directory.

Toolkits and data:
-----------------
NLTK
NLTK_Data/gutenberg and english.pickle tokenizer
SVM/sklearn