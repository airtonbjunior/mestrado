# -*- coding: utf-8 -*-
import io
import time
import nltk
#nltk.download()
from nltk.collocations import *
from nltk.tokenize import word_tokenize

start = time.time()

myFile = io.open("D:/redditdata-cancer.txt", "r", encoding='utf-8').read()
saveFile = io.open("D:/redditdata-cancer-pmi.txt", "w", encoding='utf-8')
#myList = myFile.split()
#myCorpus = nltk.Text(myList)


bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(word_tokenize(myFile))

saveFile.write("## USING BIGRAM ##\n\n") 


for i in finder.score_ngrams(bigram_measures.pmi):
    #print (i)
    saveFile.write(str(i) + "\n") 

print("\n------------------------------------\n")

# [a]
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(word_tokenize(myFile))


saveFile.write("## USING TRIGRAM ##\n\n") 


for i in finder.score_ngrams(trigram_measures.pmi):
    #print (i)
    saveFile.write(str(i) + "\n") 


end = time.time()

print("Script ends after " + str(format(end - start, '.3g')) + " seconds")

# Coments/References
#[a] http://stackoverflow.com/questions/21128689/how-to-get-pmi-scores-for-trigrams-with-nltk-collocations-python