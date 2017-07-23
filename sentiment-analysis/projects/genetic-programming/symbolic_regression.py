# Airton Bordin Junior
# airtonbjunior@gmail.com
# Federal University of Goias (UFG)
# Computer Science Master's Degree
#
# Genetic Programming - First example using deap
# Reference: https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/symbreg.py
#            https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/spambase.py

import operator
import math
import random
import re
import numpy
import time
import string

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from twython import Twython

from stemming.porter2 import stem
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


#import nltk
#nltk.download()

# log time
start = time.time()


tweets_semeval       = []
tweets_semeval_score = []
tweet_semeval_index  = 0

dic_positive_words     = []
dic_negative_words     = []
dic_positive_hashtags  = []
dic_negative_hashtags  = []
dic_positive_emoticons = []
dic_negative_emoticons = []
dic_negation_words     = []

positive_tweets = 0
negative_tweets = 0
neutral_tweets  = 0

fitness_positive = 0
fitness_negative = 0
fitness_neutral  = 0

best_fitness = 0
best_fitness_history  = []
all_fitness_history   = []

best_accuracy = 0

best_precision_positive = 0
best_precision_negative = 0
best_precision_neutral  = 0
best_precision_avg      = 0

best_recall_positive = 0
best_recall_negative = 0
best_recall_neutral  = 0
best_recall_avg      = 0

best_f1_positive = 0
best_f1_negative = 0
best_f1_neutral  = 0
best_f1_avg      = 0
best_f1_positive_negative_avg = 0

best_precision_avg_function = ""
best_recall_avg_function    = ""
best_f1_avg_function        = ""

precision_positive_history = []
precision_negative_history = []
precision_neutral_history  = []
recall_positive_history    = []
recall_negative_history    = []
recall_neutral_history     = []
f1_positive_history        = []
f1_negative_history        = []
f1_neutral_history         = []

MAX_ANALYSIS_TWEETS = 10000

MAX_POSITIVES_TWEETS = 1400
MAX_NEGATIVES_TWEETS = 1400
MAX_NEUTRAL_TWEETS = 1400

GENERATIONS = 1000
generations_unchanged = 0
max_unchanged_generations = 450

stop_words = set(stopwords.words('english'))

uses_dummy_function = False
used_stop_words = False
used_stemming_words = False

log_all_messages = False
log_parcial_results = True

# Used only once
def saveTweetsFromIdInFile():
    print("[loading tweets to save in a file]")

    file = open("datasets/twitter-2016train-A-full-tweets2.txt","w") 
    
    tweet_parsed = []

    APP_KEY = 'fBoxg0SJUlIKRN84wOJGGCmgz'
    APP_SECRET = 'yhf4LSdSlfmj25WUzvT8YzWmFXf30SFv2w5Qqa3M6wViWZNpYA'
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()

    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

    exceptions = 0

    with open('datasets/twitter-2016train-A-part.txt', 'r') as inF:
        for line in inF:
            tweet_parsed = line.split()
            try:
                tweet = twitter.show_status(id=str(tweet_parsed[0]))
                file.write(tweet_parsed[1].strip() + "#@#" + tweet['text'].strip() + "\n") 
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                exceptions += 1
                continue

    print("[" + str(exceptions) + " exceptions]")
    print("[tweets saved on file]")

    file.close() 


# Used only to load the file (once)
def saveTestTweetsFromFilesIdLoadedSemeval2014():
    print("[loading tweets from test file Semeval 2014]")

    saveFile = open("datasets/test/SemEval2014-task9-test-B-all-tweets.txt","w") 

    tweet_text = []
    tweet_polarity = []
    tweet_base = []

    tweets_loaded = 0
    polarity_loaded = 0

    with open('d:/SemEval2014-task9-test-B-input.txt', 'r') as inF:
        for line in inF:
            tweet_parsed = line.split("\t")
            tweet_text.append(tweet_parsed[3])
            tweets_loaded += 1
            print(tweet_parsed[3])
    
    with open('d:/SemEval2014-task9-test-B-gold.txt', 'r') as inF2:
        for line2 in inF2:
            tweet_parsed = line2.split("\t")
            tweet_polarity.append(tweet_parsed[2])
            tweet_base.append(tweet_parsed[1])
            polarity_loaded += 1
            print(tweet_parsed[2])
    
    for index, item in enumerate(tweet_text):
        saveFile.write(tweet_polarity[index].strip() + "\t" + tweet_base[index] + "\t" + tweet_text[index].strip() + "\n")

    saveFile.close()


    print("Tweets loaded " + str(tweets_loaded))
    print("Polarity loaded " + str(polarity_loaded))

    print("[tweets loaded]")


# get tweets from id (SEMEVAL 2014 database)
def getTweetsFromFileIdLoadedSemeval2014():
    print("[loading tweets from train file Semeval 2014]")

    global MAX_ANALYSIS_TWEETS

    global tweets_semeval
    global tweets_semeval_score

    global positive_tweets
    global negative_tweets
    global neutral_tweets

    tweets_loaded = 0

    with open('datasets/twitter-train-cleansed-B.txt', 'r') as inF:
        for line in inF:
            if tweets_loaded < MAX_ANALYSIS_TWEETS:
                tweet_parsed = line.split("\t")
                try:
                    # i'm ignoring the neutral tweets
                    if(tweet_parsed[2] != "neutral"):
                        if(tweet_parsed[2] == "positive"):
                            if(positive_tweets < MAX_POSITIVES_TWEETS):
                                positive_tweets += 1
                                tweets_semeval.append(tweet_parsed[3])
                                tweets_semeval_score.append(1)
                                tweets_loaded += 1
                        else:
                            if(negative_tweets < MAX_NEGATIVES_TWEETS):
                                negative_tweets += 1
                                tweets_semeval.append(tweet_parsed[3])
                                tweets_semeval_score.append(-1)
                                tweets_loaded += 1
                    else:
                        if(neutral_tweets < MAX_NEUTRAL_TWEETS):
                            tweets_semeval.append(tweet_parsed[3])
                            tweets_semeval_score.append(0)
                            neutral_tweets += 1
                            tweets_loaded += 1
                # treat 403 exception mainly
                except:
                    #print("exception")
                    continue
    
    print("[tweets loaded]")


# get tweets from id (SEMEVAL database)
def getTweetsFromFileIdLoaded():
    print("[loading tweets from file]")

    global MAX_ANALYSIS_TWEETS

    global tweets_semeval
    global tweets_semeval_score

    global positive_tweets
    global negative_tweets

    tweets_loaded = 0

    with open('datasets/twitter-2016train-A-full-tweets.txt', 'r') as inF:
        for line in inF:
            if tweets_loaded < MAX_ANALYSIS_TWEETS:
                tweet_parsed = line.split("#@#")
                try:
                    # i'm ignoring the neutral tweets
                    if(tweet_parsed[0] != "neutral"):
                        tweets_semeval.append(tweet_parsed[1])
                        if(tweet_parsed[0] == "positive"):
                            positive_tweets += 1
                            tweets_semeval_score.append(1)
                        else:
                            negative_tweets += 1
                            tweets_semeval_score.append(-1)

                        tweets_loaded += 1
                # treat 403 exception mainly
                except:
                    #print("exception")
                    continue
    
    print("[tweets loaded]")


# get tweets from id (SEMEVAL database)
def getTweetsFromIds():
    print("[loading tweets]")

    global tweets_semeval
    global tweets_semeval_score

    global positive_tweets
    global negative_tweets

    tweet_parsed = []

    APP_KEY = 'fBoxg0SJUlIKRN84wOJGGCmgz'
    APP_SECRET = 'yhf4LSdSlfmj25WUzvT8YzWmFXf30SFv2w5Qqa3M6wViWZNpYA'
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()

    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

    with open('twitter-2016train-A-part.txt', 'r') as inF:
        for line in inF:
            tweet_parsed = line.split()
            try:
                # i'm ignoring the neutral tweets
                if(tweet_parsed[1] != "neutral"):
                    tweet = twitter.show_status(id=str(tweet_parsed[0]))
                    tweets_semeval.append(tweet['text'])
                    if(tweet_parsed[1] == "positive"):
                        positive_tweets += 1
                        tweets_semeval_score.append(1)
                    else:
                        negative_tweets += 1
                        tweets_semeval_score.append(-1)
            # treat 403 exception mainly
            except:
                #print("exception")
                continue
    
    print("[tweets loaded]")


def getDictionary():
    print("[loading dictionary]")

    global dic_positive_words
    global dic_negative_words

    global dic_positive_hashtags
    global dic_negative_hashtags

    global dic_positive_emoticons
    global dic_negative_emoticons

    global dic_negation_words

    with open('dictionaries/positive-words.txt', 'r') as inF:
        for line in inF:
            dic_positive_words.append(line.lower().strip())

    with open('dictionaries/negative-words.txt', 'r') as inF2:
        for line2 in inF2:
            dic_negative_words.append(line2.lower().strip())

    with open('dictionaries/positive-hashtags.txt', 'r') as inF3:
        for line3 in inF3:
            dic_positive_hashtags.append(line3.lower().strip())

    with open('dictionaries/negative-hashtags.txt', 'r') as inF4:
        for line4 in inF4:
            dic_negative_hashtags.append(line4.lower().strip())            

    with open('dictionaries/positive-emoticons.txt', 'r') as inF5:
        for line5 in inF5:
            dic_positive_emoticons.append(line5.strip()) 

    with open('dictionaries/negative-emoticons.txt', 'r') as inF6:
        for line6 in inF6:
            dic_negative_emoticons.append(line6.strip())             

    with open('dictionaries/negating-word-list.txt', 'r') as inF7:
        for line7 in inF7:
            dic_negation_words.append(line7.strip()) 

    with open('dictionaries/goldStandard.tff', 'r') as inF8:
        for line8 in inF8:
            if (line8.split()[1] == "+Effect"):
                for word in line8.split()[2].split(","):
                    dic_positive_words.append(word)
                    #print("[positive word]: " + word)
            
            elif (line8.split()[1] == "-Effect"):
                for word in line8.split()[2].split(","):
                    dic_negative_words.append(word)
                    #print("[negative word]: " + word)


#    with open('dictionaries/SemEval2015-English-Twitter-Lexicon.txt', 'r') as inF7:
#        for line7 in inF7:
#            #removing composite words for while 
#            if float(line7.split("\t")[0]) > 0 and not ' ' in line7.split("\t")[1].strip():
#                if "#" in line7.split("\t")[1].strip():
#                    dic_positive_hashtags.append(line7.split("\t")[1].strip()[1:])
#                else:
#                    dic_positive_words.append(line7.split("\t")[1].strip())
#            elif float(line7.split("\t")[0]) < 0 and not ' ' in line7.split("\t")[1].strip():
#                if "#" in line7.split("\t")[1].strip():
#                    dic_negative_hashtags.append(line7.split("\t")[1].strip()[1:])
#                else:
#                    dic_negative_words.append(line7.split("\t")[1].strip())

    print("[dictionary loaded] [words, hashtags and emoticons]")


# Define new functions
# Protected Div (check division by zero)
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


# Log
def protectedLog(value):
    try:
        return math.log10(value)
    except:
        return 1    


# Sqrt
def protectedSqrt(value):
    try:
        return math.sqrt(value)
    except:
        return 1  


def invertSignal(val):
    return -val


def negativeWordsQuantity(phrase):
    global dic_negative_words
    negative_words = 0
    words = phrase.split()
    
    for word in words:
        if word in dic_negative_words:
            negative_words += 1

    return negative_words


def positiveWordsQuantity(phrase):
    global dic_positive_words
    positive_words = 0
    words = phrase.split()
    
    for word in words:
        if word in dic_positive_words:
            positive_words += 1

    return positive_words    


# Return the sum of the word polarities (positive[+1], negative[-1])
def polaritySum(phrase):
    global dic_positive_words
    global dic_negative_words
    
    total_sum = 0
    index = 0

    words = phrase.split()
    
    for word in words:
        if word.lower().strip() in dic_positive_words:
            if index > 0 and words[index-1] == "insidenoteinverterword":
                #print("[has inversion word]: " + words[index-1])
                total_sum -=1
            else:
                #print("[positive Word]: " + word)
                total_sum += 1 

        if word.lower().strip() in dic_negative_words:
            if index > 0 and words[index-1] == "insidenoteinverterword":
                #print("[has inversion word]: " + words[index-1])
                total_sum +=1
            else:
                #print("[negative Word]: " + word)
                total_sum -= 1

        index += 1    

    return total_sum  


def replaceNegatingWords(phrase):
    global dic_negation_words

    phrase = phrase.lower()
    phrase_list = []

    if phrase.split()[0] in dic_negation_words:
        phrase_list = phrase.split()
        phrase_list[0] = "insidenoteinverterword"
        phrase = ' '.join(phrase_list)

    for negation_word in dic_negation_words:
        negation_word = " " + negation_word + " "
        if phrase.lower().find(negation_word.lower()) > -1:
            phrase = phrase.replace(negation_word, " insidenoteinverterword ")


    return phrase 


# sum of the hashtag polarities only
def hashtagPolaritySum(phrase):
    return positiveHashtags(phrase) - negativeHashtags(phrase)


# sum of the emoticons polarities only
def emoticonsPolaritySum(phrase):
    return positiveEmoticons(phrase) - negativeEmoticons(phrase)


def positiveEmoticons(phrase):
    global dic_positive_emoticons
    words = phrase.split()

    total_sum = 0

    for word in words:
        if word.strip() in dic_positive_emoticons:
            total_sum += 1               

    return total_sum


def negativeEmoticons(phrase):
    global dic_negative_emoticons
    words = phrase.split()

    total_sum = 0

    for word in words:
        if word.strip() in dic_negative_emoticons:
            total_sum += 1               

    return total_sum


# Positive Hashtags
def positiveHashtags(phrase):
    global dic_positive_words
    global dic_positive_hashtags
    total = 0
    if "#" in phrase:
        #print("has hashtag")
        hashtags = re.findall(r"#(\w+)", phrase)

        for hashtag in hashtags:
            if hashtag.lower().strip() in dic_positive_hashtags:
                total += 1 
            else:
                if hashtag.lower().strip() in dic_positive_words:
                    total += 1 

    return total


# Negative Hashtags
def negativeHashtags(phrase):
    global dic_negative_words
    global dic_negative_hashtags
    total = 0
    if "#" in phrase:
        #print("has hashtag")
        hashtags = re.findall(r"#(\w+)", phrase)

        for hashtag in hashtags:
            if hashtag.lower().strip() in dic_negative_hashtags:
                total += 1 
            else:
                if hashtag.lower().strip() in dic_negative_words:
                    total += 1 

    return total


# Check if has hashtags on phrase
def hasHashtag(phrase):
    return True if "#" in phrase else False


# Check if has emoticons on phrase
def hasEmoticons(phrase):
    global dic_negative_emoticons
    global dic_positive_emoticons
    
    words = phrase.split()

    for word in words:
        if (word in dic_negative_emoticons) or (word in dic_positive_emoticons):
            return True

    return False


# logic operators
# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2


def removeStopWords(phrase):
    global stop_words
    global used_stop_words

    #if used_stop_words:
        #return phrase

    words = phrase.split()
    return_phrase = ""

    for word in words:
        if word not in stop_words:
            return_phrase += word + " "               

    used_stop_words = True
    return return_phrase


def stemmingText(phrase):
    #global used_stemming_words
    words = phrase.split()
    
    #if used_stemming_words:
        #return phrase

    stemmed_phrase = ""

    for word in words:
        stemmed_phrase += stem(word) + " "               

    used_stemming_words = True
    return stemmed_phrase.strip()


def lemmingText(phrase):
    lemmatizer = WordNetLemmatizer()
    words = phrase.split()

    lemmed_phrase = ""

    for word in words:
        # I'm always considering that the word is a verb
        lemmed_phrase += lemmatizer.lemmatize(word, 'v') + " "               

    return lemmed_phrase.strip()


def removeLinks(phrase):
    return re.sub(r'http\S+', '', phrase, flags=re.MULTILINE)


def removeEllipsis(phrase):
    return re.sub('\.{3}', ' ', phrase)


def removeDots(phrase):
    return re.sub('\.', ' ', phrase)


def removeAllPonctuation(phrase):
    return phrase.translate(str.maketrans('','',string.punctuation))


pset = gp.PrimitiveSetTyped("MAIN", [str], float)
pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)

#pset.addPrimitive(math.pow, [float, float], float)

pset.addPrimitive(math.exp, [float], float)
pset.addPrimitive(math.cos, [float], float)
pset.addPrimitive(math.sin, [float], float)
pset.addPrimitive(protectedSqrt, [float], float)

pset.addPrimitive(protectedLog, [float], float)
pset.addPrimitive(invertSignal, [float], float) # invert

pset.addPrimitive(positiveHashtags, [str], float)
pset.addPrimitive(negativeHashtags, [str], float)

pset.addPrimitive(positiveEmoticons, [str], float)
pset.addPrimitive(negativeEmoticons, [str], float)

pset.addPrimitive(polaritySum, [str], float)
pset.addPrimitive(hashtagPolaritySum, [str], float)
pset.addPrimitive(emoticonsPolaritySum, [str], float)

pset.addPrimitive(positiveWordsQuantity, [str], float)
pset.addPrimitive(negativeWordsQuantity, [str], float)

pset.addPrimitive(hasHashtag, [str], bool)
pset.addPrimitive(hasEmoticons, [str], bool)

pset.addPrimitive(if_then_else, [bool, float, float], float)

pset.addPrimitive(stemmingText, [str], str)
pset.addPrimitive(removeStopWords, [str], str)
pset.addPrimitive(removeLinks, [str], str)
pset.addPrimitive(removeEllipsis, [str], str)
pset.addPrimitive(removeAllPonctuation, [str], str)
pset.addPrimitive(replaceNegatingWords, [str], str)

pset.addTerminal(True, bool)
pset.addTerminal(False, bool)

#pset.addTerminal(polaritySumTerminal(tweets_semeval[tweet_semeval_index]), float)
pset.addEphemeralConstant("rand", lambda: random.uniform(-2, 2), float)


pset.renameArguments(ARG0='x')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


# evaluation function 
def evalSymbRegTweetsFromSemeval(individual):
    global tweets_semeval
    global tweets_semeval_score

    global positive_tweets
    global negative_tweets
    global neutral_tweets

    global fitness_positive
    global fitness_negative
    global fitness_neutral

    global best_fitness
    global best_fitness_history
    global all_fitness_history

    global best_accuracy
    # Precision
    global best_precision_positive
    global best_precision_negative
    global best_precision_neutral
    global best_precision_avg
    global best_precision_avg_function
    # Recall
    global best_recall_positive
    global best_recall_negative
    global best_recall_neutral
    global best_recall_avg
    global best_recall_avg_function
    # F1
    global best_f1_positive
    global best_f1_negative
    global best_f1_neutral
    global best_f1_avg
    global best_f1_positive_negative_avg
    global best_f1_avg_function
    # Precision, Recall and F1 history
    global precision_positive_history
    global precision_negative_history
    global precision_neutral_history
    global recall_positive_history
    global recall_negative_history
    global f1_positive_history
    global f1_negative_history

    global uses_dummy_function
    global used_stop_words
    global used_stemming_words

    global log_all_messages
    global log_parcial_results

    global generations_unchanged
    global max_unchanged_generations

    correct_evaluations = 0

    fitnessReturn = 0

    is_positive = 0
    is_negative = 0
    is_neutral  = 0
    
    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    true_neutral  = 0
    false_positive = 0
    false_negative = 0
    false_neutral  = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral  = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral  = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral  = 0
    f1_avg = 0
    f1_positive_negative_avg = 0

    breaked = False

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    used_stop_words = False
    used_stemming_words = False

    for index, item in enumerate(tweets_semeval):        

        if generations_unchanged >= max_unchanged_generations:
            breaked = True
            break

        if index == 0:
            print("\n[New cicle]: " + str(len(tweets_semeval)) + " phrases to evaluate [" + str(positive_tweets) + " positives, " + str(negative_tweets) + " negatives and " + str(neutral_tweets) + " neutrals]")

        try:
            if float(tweets_semeval_score[index]) > 0:
                if float(func(tweets_semeval[index])) > 0:
                    correct_evaluations += 1 
                    is_positive   += 1
                    true_positive += 1
                else:
                    if float(func(tweets_semeval[index])) == 0:
                        false_neutral += 1
                    else:
                        false_negative += 1

            elif float(tweets_semeval_score[index]) < 0:
                if float(func(tweets_semeval[index])) < 0:
                    correct_evaluations += 1 
                    is_negative   += 1
                    true_negative += 1
                else:
                    if float(func(tweets_semeval[index])) == 0:
                        false_neutral += 1
                    else:
                        false_positive += 1

            elif float(tweets_semeval_score[index]) == 0:
                if float(func(tweets_semeval[index])) == 0:
                    correct_evaluations += 1 
                    is_neutral   += 1
                    true_neutral += 1
                else:
                    if float(func(tweets_semeval[index])) < 0:
                        false_negative += 1
                    else:
                        false_positive += 1


        except:
            print("exception")
            continue

        #logs
        #print(index, item)
        if log_all_messages:
            print("[phrase]: " + tweets_semeval[index])
            print("[value]: " + str(tweets_semeval_score[index]))
            print("[calculated]:" + str(func(tweets_semeval[index])))
        #logs


    if uses_dummy_function:
        fitnessReturn = 0
        uses_dummy_function = False


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    if accuracy > best_accuracy:
        best_accuracy = accuracy 

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)
        if precision_positive > best_precision_positive:
            best_precision_positive = precision_positive


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
        if precision_negative > best_precision_negative:
            best_precision_negative = precision_negative
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
        if precision_neutral > best_precision_neutral:
            best_precision_neutral = precision_neutral
    # End PRECISION

    # Begin RECALL
    if positive_tweets > 0:
        recall_positive = true_positive / positive_tweets
        if recall_positive > best_recall_positive:
            best_recall_positive = recall_positive


    if negative_tweets > 0:
        recall_negative = true_negative / negative_tweets
        if recall_negative > best_recall_negative:
            best_recall_negative = recall_negative

    if neutral_tweets > 0:
        recall_neutral = true_neutral / neutral_tweets
        if recall_neutral > best_recall_neutral:
            best_recall_neutral = recall_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)
        if f1_positive > best_f1_positive:
            best_f1_positive = f1_positive


    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        
        if f1_negative > best_f1_negative:
            best_f1_negative = f1_negative

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)        
        if f1_neutral > best_f1_neutral:
            best_f1_neutral = f1_neutral            
    # End F1

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    if precision_avg > best_precision_avg:
        best_precision_avg = precision_avg
        best_precision_avg_function = str(individual)

    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3
    if recall_avg > best_recall_avg:
        best_recall_avg = recall_avg
        best_recall_avg_function = str(individual)

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3
    if f1_avg > best_f1_avg:
        best_f1_avg = f1_avg
        best_f1_avg_function = str(individual)

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2
    if f1_positive_negative_avg > best_f1_positive_negative_avg:
        best_f1_positive_negative_avg = f1_positive_negative_avg

    # The metric that represent the fitness
    # fitnessReturn = accuracy
    fitnessReturn = f1_positive_negative_avg


    # test: i'm forcing don't model only the positive or negative tweets
    # there are a lot more positive than negative on dataset
    if (fitnessReturn == positive_tweets) or (fitnessReturn == negative_tweets):
        fitnessReturn = 0


    if best_fitness < fitnessReturn:
        if best_fitness != 0:
            best_fitness_history.append(best_fitness)
        best_fitness = fitnessReturn
        fitness_positive = is_positive
        fitness_negative = is_negative
        fitness_neutral  = is_neutral
        is_positive = 0
        is_negative = 0
        is_neutral  = 0
        generations_unchanged = 0
    else:
        generations_unchanged += 1


    all_fitness_history.append(fitnessReturn)

    #logs   
    if log_parcial_results and not breaked: 
        print("[function]: " + str(individual))
        print("[accuracy]: " + str(round(accuracy, 3)))
        print("[precision positive]: " + str(round(precision_positive, 3)))
        print("[precision negative]: " + str(round(precision_negative, 3)))
        print("[precision neutral]: " + str(round(precision_neutral, 3)))
        print("[precision avg]: " + str(round(precision_avg, 3)))
        print("[recall positive]: " + str(round(recall_positive, 3)))
        print("[recall negative]: " + str(round(recall_negative, 3)))
        print("[recall neutral]: " + str(round(recall_neutral, 3)))
        print("[recall avg]: " + str(round(recall_avg, 3)))
        print("[f1 positive]: " + str(round(f1_positive, 3)))
        print("[f1 negative]: " + str(round(f1_negative, 3)))
        print("[f1 neutral]: " + str(round(f1_neutral, 3)))        
        print("[f1 avg]: " + str(round(f1_avg, 3)))
        print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 3)))
        print("[fitness (F1 +/-)]: " + str(round(fitnessReturn, 3)))
        print("[best fitness]: " + str(round(best_fitness, 3)))
        print("[generations unmodified]: " + str(generations_unchanged))
        print("[true_positive]: " + str(true_positive))
        print("[false_positive]: " + str(false_positive))
        print("[true_negative]: " + str(true_negative))
        print("[false_negative]: " + str(false_negative))
        print("[true_neutral]: " + str(true_neutral))
        print("[false_neutral]: " + str(false_neutral))        
        print("\n")   
    #logs

    return fitnessReturn,



toolbox.register("evaluate", evalSymbRegTweetsFromSemeval) # , points=[x for x in reviews])

toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=10)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=16))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=16))


# Work on memory to improve performance
# load the dictionary 
getDictionary()

# Load the tweets
getTweetsFromFileIdLoadedSemeval2014()


def main():

    global best_fitness
    global best_fitness_history
    global all_fitness_history

    global best_accuracy
    global best_precision_positive
    global best_precision_negative
    global best_precision_avg
    global best_recall_positive
    global best_recall_negative
    global best_recall_avg
    global best_f1_positive
    global best_f1_negative
    global best_f1_avg
    global best_f1_positive_negative_avg

    global best_precision_avg_function
    global best_recall_avg_function
    global best_f1_avg_function

    global positive_tweets
    global negative_tweets
    global neutral_tweets

    global fitness_positive
    global fitness_negative

    global GENERATIONS

    random.seed()

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(3)
    
    
    #stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    #stats_size = tools.Statistics(len)
    #mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    #mstats.register("avg", numpy.mean)
    #mstats.register("std", numpy.std)
    #mstats.register("min", numpy.min)
    #mstats.register("max", numpy.max)


    # Parameters
        # population (list of individuals)
        # toolbox (that contains the evolution operators)
        # Mating probability (two individuals)
        # Mutation probability
        # Number of generations
        # Statistics objetc (updated inplace)
        # HallOfFame object that contain the best individuals
        # Whether or not to log the statistics
    pop, log = algorithms.eaSimple(pop, toolbox, 9.5, 4.5, GENERATIONS, stats=False,
                                   halloffame=hof, verbose=False)#True)


    #logs
    print("\n")
    print("## Results ##\n")
    print("[total tweets]: " + str(positive_tweets + negative_tweets + neutral_tweets) + " [" + str(positive_tweets) + " positives, " + str(negative_tweets) + " negatives and " + str(neutral_tweets) + " neutrals]\n")
    print("[best fitness (F1 avg (+/-)]: " + str(best_fitness) + " [" + str(fitness_positive + fitness_negative + fitness_neutral) + " correct evaluations] ["+ str(fitness_positive) + " positives, " + str(fitness_negative) + " negatives and " + str(fitness_neutral) + " neutrals]\n")
    print("[function]: " + str(hof[0]) + "\n")
    print("[best accuracy]: " + str(best_accuracy) + "\n")
    print("[best precision positive]: " + str(best_precision_positive))
    print("[best precision negative]: " + str(best_precision_negative))
    print("[best precision neutral]: "  + str(best_precision_neutral))    
    print("[best precision avg]: " + str(best_precision_avg))
    print("[best precision avg function]: " + best_precision_avg_function + "\n")    
    print("[best recall positive]: " + str(best_recall_positive))    
    print("[best recall negative]: " + str(best_recall_negative))
    print("[best recall avg]: " + str(best_recall_avg))
    print("[best recall avg function]: " + best_recall_avg_function + "\n")
    print("[best f1 positive]: " + str(best_f1_positive))    
    print("[best f1 negative]: " + str(best_f1_negative))
    print("[best f1 avg]: " + str(best_f1_avg))
    print("[best f1 avg (+/-)]: " + str(best_f1_positive_negative_avg))
    print("[best f1 avg function]: " + best_f1_avg_function + "\n")       
    #print(json.dumps(all_fitness_history))
    print("\n")
    #print(set(all_fitness_history))
    #logs 

    # Plot the data contained on all_fitness_history

    return pop, log, hof


if __name__ == "__main__":
    #main()

    print("oi")

    #message = "Tracy McGrady signed with a team in China today.  Clearly that team does not have aspirations of reaching the 2nd round"


    #print(message)
    #print(str(replaceNegatingWords(message)))

    #print(str(polaritySum(message)))
    #print(str(polaritySum(replaceNegatingWords(message))))

    #print(str(message.find("DO NOT")))

    #print(str(spellCheck("im doingg some worng text here to corect")))
    #print(str(polaritySumWithNegationWords("I don't love you")))

    #print(removeAllPonctuation("hi,, hey! i'm only testing!!?:??: das adna i hope it's ok!!??."))

    #print(polaritySum(removeAllPonctuation("@CarlJWood I teach my class to count in pennies at first. I may be part of the problem.")))
    #print(lemmingText(removeEllipsis(removeAllPonctuation("@CarlJWood I teach my class to count in pennies at first. I may be part of the problem."))))
    #print(stemmingText(removeEllipsis(removeAllPonctuation("@CarlJWood I teach my class to count in pennies at first. I may be part of the problem."))))

    #print(removeEllipsis(removeLinks("1st debate showed emperor has no clothes...Wonder how the court jester\u002c shoeless Joe will do against Ryan? #gop")))
    #saveTestTweetsFromFilesIdLoadedSemeval2014()
    #saveTweetsFromIdInFile()

end = time.time()
print("Script ends after " + str(format(end - start, '.3g')) + " seconds")


# TO-DO: uppercasepositive uppercasenegative 
# repeated vowel
# see n-gram dictionary