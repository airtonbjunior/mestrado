# -*- coding: utf-8 -*-
import io
import sys
import time
import string
import re
import math
import nltk
from nltk.tokenize import TweetTokenizer
#nltk.download()
from nltk.collocations import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Start count the process time
start = time.time()


# [A]
frequency = 1

def do_bigrams(words):
	bigrams = nltk.collocations.BigramCollocationFinder.from_words(words)
	#bigrams.apply_freq_filter(frequency)
	return {bigram: freq for bigram, freq in bigrams.ngram_fd.items()}



def do_unigrams(words):
	unigrams = nltk.FreqDist(words)
	return {unigram: freq for unigram, freq in unigrams.items()}


def calc_pmi(word1, word2, unigram_freq, bigram_freq):
	prob_word1 = unigram_freq[word1] / sum(unigram_freq.values())
	prob_word2 = unigram_freq[word2] / sum(unigram_freq.values())
	try:
		prob_word1_word2 = bigram_freq[(word1, word2)] / sum(bigram_freq.values())
	except KeyError:
		#print ("Error")
		return 0
	a = prob_word1_word2 / prob_word1 * prob_word2
	return round(math.log(a, 2), 2);



# filesystem
myFile = io.open("D:/redditdata-cancer.txt", "r", encoding='utf-8').read()
saveFile = io.open("D:/redditdata-cancer-pmi.txt", "w", encoding='utf-8')
myDataTestTokens = io.open("D:/redditdata-test-tokens.txt", "w", encoding='utf-8')
myDataTestUnigrams = io.open("D:/redditdata-test-unigrams.txt", "w", encoding='utf-8')
myDataTestBigrams = io.open("D:/redditdata-test-bigrams.txt", "w", encoding='utf-8')
myDataTestPMIPositive = io.open("D:/redditdata-test-pmi-positive-smile.txt", "w", encoding='utf-8')
myDataTestPMINegative = io.open("D:/redditdata-test-pmi-negative-smile.txt", "w", encoding='utf-8')


punctuations = list(string.punctuation)
punctuations.append("--")

# [b]
my_stop_words = ['i', 'you', 'he', 'she', 'it', 'they', 'am', 'are', 'is', 'was', 'would', "a", "about", "above", "above", "across", "after", 
				"afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", 
				"amoungst", "amount", "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as", "at", 
				"back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", 
				"besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", 
				"cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", 
				"empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", 
				"find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", 
				"go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", 
				"himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", 
				"last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", 
				"most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", 
				"none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", 
				"otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", 
				"seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", 
				"someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", 
				"themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", 
				"this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", 
				"two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", 
				"where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", 
				"whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", 
				"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "it's", "..."]



#print(stopwords.words('english'))

#myList = myFile.split()
#myCorpus = nltk.Text(myList)

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
result_words = tknzr.tokenize(myFile.encode("utf8"))

# Remove the punctuactions
result_words = [i for i in result_words if i not in punctuations]
# Remove stopwords
result_words = [i for i in result_words if i.lower() not in my_stop_words]

# Remove the urls 
#result_words = re.sub(r"http\S+", "", str(result_words))
#result_words = re.sub(r"www\S+", "", str(result_words))
# Remove mentions @
#result_words = re.sub(r"@\S+", "", str(result_words))
# Remove --
#result_words = re.sub(r"--\S+", "", str(result_words))


# Save the tokenize text
#tokenizeTextFile.write(str(result_words))


#bigram_measures = nltk.collocations.BigramAssocMeasures()
#finder = BigramCollocationFinder.from_words(word_tokenize(str(result_words)))

#myDataTestTokens.write(str(result_words))

unigrams = do_unigrams(result_words)
#myDataTestUnigrams.write(str(unigrams))

bigrams = do_bigrams(result_words)
#myDataTestBigrams.write(str(bigrams))

pmi_values = []

for i in result_words:
	#print(calc_pmi("couple", "days", unigrams, bigrams))
	#pmi_values.append(i + " and good: " + str(calc_pmi("good", str(i), unigrams, bigrams)))

	pmiPositive = calc_pmi(":)", str(i), unigrams, bigrams)
	myDataTestPMIPositive.write(i + " and smile :) -> " + str(pmiPositive) + "\n")
	
	pmiNegative = calc_pmi(":(", str(i), unigrams, bigrams)
	myDataTestPMINegative.write(i + " and smile :( -> " + str(pmiNegative) + "\n")

#myDataTestPMI.write(str(pmi_values))

end = time.time()

print("Script ends after " + str(format(end - start, '.3g')) + " seconds")

# Coments/References
# [A] https://www.slideshare.net/FrancescoBruni1/basic-nlp-with-python-and-nltk
