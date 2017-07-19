import string
import operator
import math
import re
import time

from stemming.porter2 import stem
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# log time
start = time.time()

MAX_ANALYSIS_TWEETS = 10000

false_neutral_log = 0
false_negative_log = 0
false_positive_log = 0

dic_positive_words     = []
dic_negative_words     = []
dic_positive_hashtags  = []
dic_negative_hashtags  = []
dic_positive_emoticons = []
dic_negative_emoticons = []
dic_negation_words     = []

tweets_liveJournal2014       = []
tweets_liveJournal2014_score = []
tweets_liveJournal2014_positive = 0
tweets_liveJournal2014_negative = 0
tweets_liveJournal2014_neutral  = 0

tweets_2013       = []
tweets_2013_score = []
tweets_2013_positive = 0
tweets_2013_negative = 0
tweets_2013_neutral  = 0

tweets_2014       = []
tweets_2014_score = []
tweets_2014_positive = 0
tweets_2014_negative = 0
tweets_2014_neutral  = 0

tweets_2014_sarcasm       = []
tweets_2014_sarcasm_score = []
tweets_2014_sarcasm_positive = 0
tweets_2014_sarcasm_negative = 0
tweets_2014_sarcasm_neutral  = 0

sms_2013       = []
sms_2013_score = []
sms_2013_positive = 0
sms_2013_negative = 0
sms_2013_neutral  = 0

stop_words = set(stopwords.words('english'))


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


# get the test tweets from Semeval 2014 task 9
def getTestTweetsFromSemeval2014():
    print("[loading tweets from test file Semeval 2014]")

    global MAX_ANALYSIS_TWEETS

    global tweets_liveJournal2014
    global tweets_liveJournal2014_score
    global tweets_liveJournal2014_positive
    global tweets_liveJournal2014_negative
    global tweets_liveJournal2014_neutral
    
    global tweets_2013
    global tweets_2013_score
    global tweets_2013_positive
    global tweets_2013_negative
    global tweets_2013_neutral
    
    global tweets_2014
    global tweets_2014_score
    global tweets_2014_positive
    global tweets_2014_negative
    global tweets_2014_neutral
    
    global sms_2013
    global sms_2013_score
    global sms_2013_positive
    global sms_2013_negative
    global sms_2013_neutral

    global tweets_2014_sarcasm
    global tweets_2014_sarcasm_score
    global tweets_2014_sarcasm_positive
    global tweets_2014_sarcasm_negative
    global tweets_2014_sarcasm_neutral

    tweets_loaded = 0

    with open('datasets/test/SemEval2014-task9-test-B-all-tweets.txt', 'r') as inF:
        for line in inF:
            if tweets_loaded < MAX_ANALYSIS_TWEETS:
                tweet_parsed = line.split("\t")
                try:
                    if tweet_parsed[1] == "Twitter2013":
                        tweets_2013.append(tweet_parsed[2])
                        
                        if tweet_parsed[0] == "positive":
                            tweets_2013_score.append(1)
                            tweets_2013_positive += 1
                        
                        elif tweet_parsed[0] == "negative":
                            tweets_2013_score.append(-1)
                            tweets_2013_negative += 1
                        
                        elif tweet_parsed[0] == "neutral":
                            tweets_2013_score.append(0)
                            tweets_2013_neutral += 1

                    elif tweet_parsed[1] == "Twitter2014":
                        tweets_2014.append(tweet_parsed[2])
                        
                        if tweet_parsed[0] == "positive":
                            tweets_2014_score.append(1)
                            tweets_2014_positive += 1
                        
                        elif tweet_parsed[0] == "negative":
                            tweets_2014_score.append(-1)
                            tweets_2014_negative += 1
                        
                        elif tweet_parsed[0] == "neutral":
                            tweets_2014_score.append(0)
                            tweets_2014_neutral += 1

                    elif tweet_parsed[1] == "SMS2013":
                        sms_2013.append(tweet_parsed[2])
                        
                        if tweet_parsed[0] == "positive":
                            sms_2013_score.append(1)
                            sms_2013_positive += 1
                        
                        elif tweet_parsed[0] == "negative":
                            sms_2013_score.append(-1)
                            sms_2013_negative += 1
                        
                        elif tweet_parsed[0] == "neutral":
                            sms_2013_score.append(0)
                            sms_2013_neutral += 1

                    elif tweet_parsed[1] == "LiveJournal2014":
                        tweets_liveJournal2014.append(tweet_parsed[2])
                        
                        if tweet_parsed[0] == "positive":
                            tweets_liveJournal2014_score.append(1)
                            tweets_liveJournal2014_positive += 1
                        
                        elif tweet_parsed[0] == "negative":
                            tweets_liveJournal2014_score.append(-1)
                            tweets_liveJournal2014_negative += 1
                        
                        elif tweet_parsed[0] == "neutral":
                            tweets_liveJournal2014_score.append(0)
                            tweets_liveJournal2014_neutral += 1

                    elif tweet_parsed[1] == "Twitter2014Sarcasm":
                        tweets_2014_sarcasm.append(tweet_parsed[2])
                        
                        if tweet_parsed[0] == "positive":
                            tweets_2014_sarcasm_score.append(1)
                            tweets_2014_sarcasm_positive += 1
                        
                        elif tweet_parsed[0] == "negative":
                            tweets_2014_sarcasm_score.append(-1)
                            tweets_2014_sarcasm_negative += 1
                        
                        elif tweet_parsed[0] == "neutral":
                            tweets_2014_sarcasm_score.append(0)                                                           
                            tweets_2014_sarcasm_neutral += 1

                    tweets_loaded += 1
                # treat 403 exception mainly
                except:
                    #print("exception")
                    continue
    
    print("[tweets loaded]")


### Begin functions (improve this - import the functions of the other file)
def add(left, right):
    return left + right

def sub(left, right):
    return left - right

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
                total_sum -=1
            else:
                #print("[positive Word]: " + word)
                total_sum += 1 

        if word.lower().strip() in dic_negative_words:
            if index > 0 and words[index-1] == "insidenoteinverterword":
                total_sum +=1
            else:
                #print("[negative Word]: " + word)
                total_sum -= 1

        index += 1    

    return total_sum  


def replaceNegatingWords(phrase):
    global dic_negation_words

    phrase = phrase.lower()
    
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
    global used_stemming_words
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
### End functions (improve this - import the functions of the other file)



# Evaluate only the Tweets2013
def evaluateTweets2013Messages(model):
    global tweets_2013
    global tweets_2013_score

    global tweets_2013_positive
    global tweets_2013_negative
    global tweets_2013_neutral

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0


    for index, item in enumerate(tweets_2013): 
        message = str(tweets_2013[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if tweets_2013_score[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif tweets_2013_score[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1

                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result)) 

        elif tweets_2013_score[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if tweets_2013_positive > 0:
        recall_positive = true_positive / tweets_2013_positive


    if tweets_2013_negative > 0:
        recall_negative = true_negative / tweets_2013_negative

    if tweets_2013_neutral > 0:
        recall_neutral = true_neutral / tweets_2013_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[Twitter2013 messages]")
    print("[messages evaluated]: " + str(len(tweets_2013)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")


# Evaluate only the Tweets2014
def evaluateTweets2014Messages(model):
    global tweets_2014
    global tweets_2014_score

    global tweets_2014_positive
    global tweets_2014_negative
    global tweets_2014_neutral

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0


    for index, item in enumerate(tweets_2014): 
        message = str(tweets_2014[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if tweets_2014_score[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif tweets_2014_score[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1

                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result)) 

        elif tweets_2014_score[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if tweets_2014_positive > 0:
        recall_positive = true_positive / tweets_2014_positive


    if tweets_2014_negative > 0:
        recall_negative = true_negative / tweets_2014_negative

    if tweets_2014_neutral > 0:
        recall_neutral = true_neutral / tweets_2014_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[Twitter2014 messages]")
    print("[messages evaluated]: " + str(len(tweets_2014)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")


# Evaluate only the Tweets2014 Sarcasm
def evaluateTweets2014SarcasmMessages(model):
    global tweets_2014_sarcasm
    global tweets_2014_sarcasm_score

    global tweets_2014_sarcasm_positive
    global tweets_2014_sarcasm_negative
    global tweets_2014_sarcasm_neutral

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0


    for index, item in enumerate(tweets_2014_sarcasm): 
        message = str(tweets_2014_sarcasm[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if tweets_2014_sarcasm_score[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif tweets_2014_sarcasm_score[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1

                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result))    

        elif tweets_2014_sarcasm_score[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if tweets_2014_sarcasm_positive > 0:
        recall_positive = true_positive / tweets_2014_sarcasm_positive


    if tweets_2014_sarcasm_negative > 0:
        recall_negative = true_negative / tweets_2014_sarcasm_negative

    if tweets_2014_sarcasm_neutral > 0:
        recall_neutral = true_neutral / tweets_2014_sarcasm_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[Twitter2014Sarcasm messages]")
    print("[messages evaluated]: " + str(len(tweets_2014_sarcasm)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")


# Evaluate only the SMS2013
def evaluateSMS2013(model):
    global sms_2013
    global sms_2013_score

    global sms_2013_positive
    global sms_2013_negative
    global sms_2013_negative

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0


    for index, item in enumerate(sms_2013): 
        message = str(sms_2013[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if sms_2013_score[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif sms_2013_score[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1

                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result))

        elif sms_2013_score[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if sms_2013_positive > 0:
        recall_positive = true_positive / sms_2013_positive


    if sms_2013_negative > 0:
        recall_negative = true_negative / sms_2013_negative

    if sms_2013_neutral > 0:
        recall_neutral = true_neutral / sms_2013_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2   
   

    print("\n")
    print("[SMS2013 messages]")
    print("[messages evaluated]: " + str(len(sms_2013)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")


# Evaluate only the Tweets2014
def evaluateTweetsLiveJournal2014(model):
    global tweets_liveJournal2014
    global tweets_liveJournal2014_score

    global tweets_liveJournal2014_positive
    global tweets_liveJournal2014_negative
    global tweets_liveJournal2014_neutral

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0

    for index, item in enumerate(tweets_liveJournal2014): 
        message = str(tweets_liveJournal2014[index]).strip().replace("'", "")
        message = message.replace("\\u2018", "").replace("\\u2019", "").replace("\\u002c", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if tweets_liveJournal2014_score[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif tweets_liveJournal2014_score[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1

                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result))

        elif tweets_liveJournal2014_score[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if tweets_liveJournal2014_positive > 0:
        recall_positive = true_positive / tweets_liveJournal2014_positive


    if tweets_liveJournal2014_negative > 0:
        recall_negative = true_negative / tweets_liveJournal2014_negative

    if tweets_liveJournal2014_neutral > 0:
        recall_neutral = true_neutral / tweets_liveJournal2014_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[LiveJournal2014 messages]")
    print("[messages evaluated]: " + str(len(tweets_liveJournal2014)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")


# Evaluate all messages
def evaluateAllMessages(model):
    global tweets_liveJournal2014
    global tweets_liveJournal2014_score
    global tweets_2013
    global tweets_2013_score
    global tweets_2014
    global tweets_2014_score
    global sms_2013
    global sms_2013_score
    global tweets_2014_sarcasm
    global tweets_2014_sarcasm_score

    global tweets_liveJournal2014_positive
    global tweets_liveJournal2014_negative
    global tweets_liveJournal2014_neutral

    global tweets_2013_positive
    global tweets_2013_negative
    global tweets_2013_neutral

    global tweets_2014_positive
    global tweets_2014_negative
    global tweets_2014_neutral

    global sms_2013_positive
    global sms_2013_negative
    global sms_2013_neutral

    global tweets_2014_sarcasm_positive
    global tweets_2014_sarcasm_negative
    global tweets_2014_sarcasm_neutral

    false_neutral_log = 0
    false_negative_log = 0

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_neutral  = 0
    false_neutral = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral = 0
    f1_avg = 0
    f1_positive_negative_avg = 0

    allMessages = tweets_2013 + tweets_2014 + tweets_liveJournal2014 + sms_2013 + tweets_2014_sarcasm
    allScores   = tweets_2013_score + tweets_2014_score + tweets_liveJournal2014_score + sms_2013_score + tweets_2014_sarcasm_score

    
    for index, item in enumerate(allMessages): 
        message = str(allMessages[index]).strip().replace("'", "")
        message = message.replace("\\u2018", "").replace("\\u2019", "").replace("\\u002c", "")
        message = "'" + message + "'"

        model_analysis = model.replace("(x)", "(" + message + ")")
        result = eval(model_analysis)

        if allScores[index] > 0:
            if result > 0:
                true_positive += 1
            else:
                if result == 0:
                    false_neutral += 1
                else:
                    false_negative += 1
                
        elif allScores[index] < 0:
            if result < 0:
                true_negative += 1
            else:
                false_negative_log += 1
                if result == 0:
                    false_neutral += 1
                else:
                    false_positive += 1
            
                if false_negative_log <= 15:
                    print("[Negative phrase evaluation error]: " + message)
                    print("[Polarity calculated]: " + str(result))

        elif allScores[index] == 0:
            if result == 0:
                true_neutral += 1
            else:
                if result < 0:
                    false_negative += 1
                else:
                    false_positive += 1    

    
    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
    # End PRECISION

    # Begin RECALL
    if tweets_2014_sarcasm_positive + tweets_2013_positive + tweets_2014_positive + sms_2013_positive + tweets_liveJournal2014_positive > 0:
        recall_positive = true_positive / (tweets_2014_sarcasm_positive + tweets_2013_positive + tweets_2014_positive + sms_2013_positive + tweets_liveJournal2014_positive)


    if tweets_2014_sarcasm_negative + tweets_2013_negative + tweets_2014_negative + sms_2013_negative + tweets_liveJournal2014_negative > 0:
        recall_negative = true_negative / (tweets_2014_sarcasm_negative + tweets_2013_negative + tweets_2014_negative + sms_2013_negative + tweets_liveJournal2014_negative)

    if tweets_2014_sarcasm_neutral + tweets_2013_neutral + tweets_2014_neutral + sms_2013_neutral + tweets_liveJournal2014_neutral > 0:
        recall_neutral = true_neutral / (tweets_2014_sarcasm_neutral + tweets_2013_neutral + tweets_2014_neutral + sms_2013_neutral + tweets_liveJournal2014_neutral)
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)                  
    # End F1        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    
    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[All messages]")
    print("[messages evaluated]: " + str(len(allMessages)))
    print("[correct evaluations]: " + str(true_positive + true_negative + true_neutral) + " (" + str(true_positive) + " positives, " + str(true_negative) + " negatives and " + str(true_neutral) + " neutrals)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 4)))
    print("[precision_positive]: " + str(round(precision_positive, 4)))
    print("[precision_negative]: " + str(round(precision_negative, 4)))
    print("[precision_neutral]: " + str(round(precision_neutral, 4)))    
    print("[precision_avg]: " + str(round(precision_avg, 4)))
    print("[recall_positive]: " + str(round(recall_positive, 4)))
    print("[recall_negative]: " + str(round(recall_negative, 4)))
    print("[recall_neutral]: " + str(round(recall_neutral, 4)))
    print("[recall avg]: " + str(round(recall_avg, 4)))
    print("[f1_positive]: " + str(round(f1_positive, 4)))
    print("[f1_negative]: " + str(round(f1_negative, 4)))
    print("[f1_neutral]: " + str(round(f1_neutral, 4)))
    print("[f1 avg]: " + str(round(f1_avg, 4)))
    print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 4)))    
    print("[true_positive]: " + str(true_positive))
    print("[false_positive]: " + str(false_positive))
    print("[true_negative]: " + str(true_negative))
    print("[false_negative]: " + str(false_negative))
    print("[true_neutral]: " + str(true_neutral))
    print("[false_neutral]: " + str(false_neutral))
    print("\n")

if __name__ == "__main__":
    getDictionary()
    getTestTweetsFromSemeval2014()


    #function_to_evaluate = "add(invertSignal(negativeWordsQuantity(x)), sin(polaritySum(x)))"
    #function_to_evaluate = "sub(mul(sub(polaritySum(removeStopWords(stemmingText(x))), sin(-0.3012931295024437)), protectedLog(-0.21199248533470838)), protectedLog(protectedLog(sub(polaritySum(stemmingText(stemmingText(stemmingText(removeStopWords(removeStopWords(removeStopWords(stemmingText(removeStopWords(stemmingText(removeStopWords(x))))))))))), sub(hashtagPolaritySum(removeStopWords(removeStopWords(removeStopWords(x)))), cos(protectedLog(polaritySum(stemmingText(removeStopWords(removeStopWords(x)))))))))))"
    #function_to_evaluate = "mul(add(add(polaritySum(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x)))))))))))), positiveEmoticons(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x)))))))), mul(sub(sin(-0.7500287440821918), protectedDiv(negativeEmoticons(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x))))))), protectedSqrt(protectedDiv(protectedLog(0.30225574066002103), cos(0.3289974105155071))))), protectedDiv(sin(negativeWordsQuantity(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x)))))), add(protectedSqrt(cos(mul(hashtagPolaritySum(x), -1.1631941015415768))), -0.27062630818833844)))), mul(protectedDiv(protectedLog(-0.9481590665673725), negativeEmoticons(x)), exp(add(-0.28621032356521914, -0.21595094634073808))))"
    #function_to_evaluate = "add(emoticonsPolaritySum(repeatInputString(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x)))))), polaritySum(repeatInputString(repeatInputString(repeatInputString(repeatInputString(x))))))"
    
    function_to_evaluate = "if_then_else(hasEmoticons(x), emoticonsPolaritySum(removeLinks(x)), polaritySum(removeEllipsis(removeLinks(lemmingText(removeAllPonctuation(replaceNegatingWords(x)))))))"
    
    #function_to_evaluate = "add(if_then_else(hasEmoticons(removeEllipsis(removeEllipsis(x))), sub(emoticonsPolaritySum(x), polaritySum(removeAllPonctuation(removeStopWords(replaceNegatingWords(x))))), polaritySum(stemmingText(removeEllipsis(removeStopWords(x))))), polaritySum(removeAllPonctuation(removeLinks(replaceNegatingWords(x)))))"

    evaluateTweets2013Messages(function_to_evaluate)
    evaluateTweets2014Messages(function_to_evaluate)
    evaluateSMS2013(function_to_evaluate)
    evaluateTweetsLiveJournal2014(function_to_evaluate)
    evaluateTweets2014SarcasmMessages(function_to_evaluate)
    evaluateAllMessages(function_to_evaluate)


end = time.time()
print("\n\n[Script ends after " + str(format(end - start, '.3g')) + " seconds]")