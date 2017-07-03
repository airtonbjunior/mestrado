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
import csv

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from twython import Twython

# log time
start = time.time()


tweets_semeval = []
tweets_semeval_score = []
tweet_semeval_index = 0

dic_positive_words     = []
dic_negative_words     = []
dic_positive_hashtags  = []
dic_negative_hashtags  = []
dic_positive_emoticons = []
dic_negative_emoticons = []

positive_tweets = 0
negative_tweets = 0

fitness_positive = 0
fitness_negative = 0
fitness_neutral = 0

MAX_ANALYSIS_TWEETS = 70
GENERATIONS = 40

best_fitness = 0
best_fitness_history = []

uses_dummy_function = False


# Used only one time
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


# get tweets of tweets.txt
def getTweets():
    global tweets
    global tweets_score

    f = open("tweets.txt", 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            if int(row[1]) > 0:
                tweets_score.append(row[1])
            else:
                tweets_score.append(-1)

            tweets.append(row[3].strip())
    finally:
        f.close()



def getDictionary():
    print("[loading dictionary]")

    global dic_positive_words
    global dic_negative_words

    global dic_positive_hashtags
    global dic_negative_hashtags

    global dic_positive_emoticons
    global dic_negative_emoticons

    with open('dictionaries/positive-words.txt', 'r') as inF:
        for line in inF:
            dic_positive_words.append(line.strip())

    with open('dictionaries/negative-words.txt', 'r') as inF2:
        for line2 in inF2:
            dic_negative_words.append(line2.strip())

    with open('dictionaries/positive-hashtags.txt', 'r') as inF3:
        for line3 in inF3:
            dic_positive_hashtags.append(line3.strip())

    with open('dictionaries/negative-hashtags.txt', 'r') as inF4:
        for line4 in inF4:
            dic_negative_hashtags.append(line4.strip())            

    with open('dictionaries/positive-emoticons.txt', 'r') as inF5:
        for line5 in inF5:
            dic_positive_emoticons.append(line5.strip()) 

    with open('dictionaries/negative-emoticons.txt', 'r') as inF6:
        for line6 in inF6:
            dic_negative_emoticons.append(line6.strip())             

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
# Liu's dicionary of positive and negative words
def polaritySum(phrase):
    global dic_positive_words
    global dic_negative_words

    words = phrase.split()

    total_sum = 0

    for word in words:
        if word in dic_positive_words:
            total_sum += 1 

        if word in dic_negative_words:
            total_sum -= 1

    return total_sum


# sum of the hashtag polarities only
def hashtagPolaritySum(phrase):
    return positiveHashtags(phrase) - negativeHashtags(phrase)


# sum of the emoticons polarities only
def emoticonsPolaritySum(phrase):
    return positiveEmoticons(phrase) - negativeEmoticons(phrase)

    
def polaritySumTerminal():
    global dic_positive_words
    global dic_negative_words

    words = phrase.split()

    total_sum = 0

    for word in words:
        if word in dic_positive_words:
            total_sum += 1 

        if word in dic_negative_words:
            total_sum -= 1

    return total_sum


def positiveEmoticons(phrase):
    global dic_positive_emoticons
    words = phrase.split()

    total_sum = 0

    for word in words:
        if word in dic_positive_emoticons:
            total_sum += 1               

    return total_sum


def negativeEmoticons(phrase):
    global dic_negative_emoticons
    words = phrase.split()

    total_sum = 0

    for word in words:
        if word in dic_negative_emoticons:
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
            if hashtag in dic_positive_hashtags:
                total += 1 
            else:
                if hashtag in dic_positive_words:
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
            if hashtag in dic_negative_hashtags:
                total += 1 
            else:
                if hashtag in dic_negative_words:
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


def onlyTestFuncion(string1, string2):
    global uses_dummy_function
    uses_dummy_function = True
    return 1


def onlyTestFuncion2(float1, float2):
    global uses_dummy_function
    uses_dummy_function = True
    return ""


def repeatInputString(phrase):
    return phrase


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

pset.addPrimitive(repeatInputString, [str], str)

# dummy functions
#pset.addPrimitive(onlyTestFuncion, [str, str], float)
#pset.addPrimitive(onlyTestFuncion2, [float, float], str)

pset.addTerminal(False, bool)

#pset.addTerminal(polaritySumTerminal(tweets_semeval[tweet_semeval_index]), float)
pset.addEphemeralConstant("rand", lambda: random.uniform(-2, 2), float)


pset.renameArguments(ARG0='x')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=7)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


# evaluation function 
def evalSymbRegTweetsFromSemeval(individual):
    global tweets_semeval
    global tweets_semeval_score

    global positive_tweets
    global negative_tweets

    global fitness_positive
    global fitness_negative

    global best_fitness
    global best_fitness_history
    global uses_dummy_function
    
    fitnessReturn = 0

    is_positive = 0
    is_negative = 0

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    #logs
    print("\n[New cicle]: " + str(len(tweets_semeval)) + " phrases to evaluate [" + str(positive_tweets) + " positives and " + str(negative_tweets) + " negatives]")
    #logs
    
    for index, item in enumerate(tweets_semeval):        

        try:
            if (round(func(tweets_semeval[index]), 2) > 0 and float(tweets_semeval_score[index]) > 0):
                fitnessReturn += 1 
                is_positive += 1

            if (round(func(tweets_semeval[index]), 2) < 0 and float(tweets_semeval_score[index]) < 0):
                fitnessReturn += 1 
                is_negative += 1

        except:
            continue

        #logs
        #print(index, item)
        print("[phrase]: " + tweets_semeval[index])
        print("[value]: " + str(tweets_semeval_score[index]))
        print("[calculated]:" + str(func(tweets_semeval[index])))
        #logs
    
    if uses_dummy_function:
        fitnessReturn = 0
        uses_dummy_function = False


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
        is_positive = 0
        is_negative = 0


    #logs    
    print("[function]: " + str(individual))
    print("[fitness]: " + str(fitnessReturn))
    print("\n\n")   
    #logs

    return fitnessReturn,



toolbox.register("evaluate", evalSymbRegTweetsFromSemeval) # , points=[x for x in reviews])

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=18))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=18))


# Work on memory to improve performance
# load the dictionary 
getDictionary()

# Load the tweets
getTweetsFromFileIdLoaded()


def main():

    global best_fitness
    global best_fitness_history

    global positive_tweets
    global negative_tweets

    global fitness_positive
    global fitness_negative

    global GENERATIONS

    random.seed()

    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    
    
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
    pop, log = algorithms.eaSimple(pop, toolbox, 2.5, 1.0, GENERATIONS, stats=False,
                                   halloffame=hof, verbose=False)#True)


    #logs
    print("\n")
    print("## Results ##\n")
    print("[total tweets]: " + str(positive_tweets + negative_tweets) + " [" + str(positive_tweets) + " positives and " + str(negative_tweets) + " negatives]\n")
    print("[best fitness]: " + str(best_fitness) + " [" + str(fitness_positive) + " positives and " + str(fitness_negative) + " negatives]\n")
    print("[function]: " + str(hof[0]) + "\n")
    print(best_fitness_history)
    print("\n")
    #logs 

    return pop, log, hof


if __name__ == "__main__":
    main()
    #saveTweetsFromIdInFile()

end = time.time()
print("Script ends after " + str(format(end - start, '.3g')) + " seconds")


# TO-DO: uppercasepositive uppercasenegative 
# repeated vowel
# see n-gram dictionary