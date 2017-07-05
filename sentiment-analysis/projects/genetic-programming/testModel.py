import time 

# log time
start = time.time()

MAX_ANALYSIS_TWEETS = 10000

dic_positive_words     = []
dic_negative_words     = []
dic_positive_hashtags  = []
dic_negative_hashtags  = []
dic_positive_emoticons = []
dic_negative_emoticons = []

tweets_liveJournal2014       = []
tweets_liveJournal2014_score = []

tweets_2013       = []
tweets_2013_score = []

tweets_2014       = []
tweets_2014_score = []

sms_2013       = []
sms_2013_score = []



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


# sum of the emoticons polarities only
def emoticonsPolaritySum(phrase):
    return positiveEmoticons(phrase) - negativeEmoticons(phrase)


# get the test tweets from Semeval 2014 task 9
def getTestTweetsFromSemeval2014():
    print("[loading tweets from train file Semeval 2014]")

    global MAX_ANALYSIS_TWEETS

    global tweets_liveJournal2014
    global tweets_liveJournal2014_score
    global tweets_2013
    global tweets_2013_score
    global tweets_2014
    global tweets_2014_score
    global sms_2013
    global sms_2013_score

    tweets_loaded = 0

    with open('datasets/test/SemEval2014-task9-test-B-all-tweets.txt', 'r') as inF:
        for line in inF:
            if tweets_loaded < MAX_ANALYSIS_TWEETS:
                tweet_parsed = line.split("\t")
                try:
                    # i'm ignoring the neutral tweets
                    if(tweet_parsed[0] != "neutral"):
                        if tweet_parsed[1] == "Twitter2013":
                            tweets_2013.append(tweet_parsed[2])
                            if tweet_parsed[0] == "positive":
                                tweets_2013_score.append(1)
                            else:
                                tweets_2013_score.append(-1)

                        elif tweet_parsed[1] == "Twitter2014":
                            tweets_2014.append(tweet_parsed[2])
                            if tweet_parsed[0] == "positive":
                                tweets_2014_score.append(1)
                            else:
                                tweets_2014_score.append(-1)

                        elif tweet_parsed[1] == "SMS2013":
                            sms_2013.append(tweet_parsed[2])
                            if tweet_parsed[0] == "positive":
                                sms_2013_score.append(1)
                            else:
                                sms_2013_score.append(-1)

                        elif tweet_parsed[1] == "LiveJournal2014":
                            tweets_liveJournal2014.append(tweet_parsed[2])
                            if tweet_parsed[0] == "positive":
                                tweets_liveJournal2014_score.append(1)
                            else:
                                tweets_liveJournal2014_score.append(-1)                            

                        tweets_loaded += 1
                # treat 403 exception mainly
                except:
                    #print("exception")
                    continue
    
    print("[tweets loaded]")


# Evaluate only the Tweets2013
def evaluateTweets2013Messages(model):
    global tweets_2013
    global tweets_2013_score

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_avg = 0

    # only 2013 for while
    for index, item in enumerate(tweets_2013): 
        message = str(tweets_2013[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("x", message)
        #print(model_analysis)
        #print(str(eval(model_analysis)))
        result = eval(model_analysis)

        if result > 0:
            if tweets_2013_score[index] > 0:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if tweets_2013_score[index] < 0:
                true_negative += 1
            else:
                false_negative += 1

    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)

    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)

    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)

    if true_positive + false_negative > 0:
        recall_positive = true_positive / (true_positive + false_negative)

    if true_negative + false_positive > 0:
        recall_negative = true_negative / (true_negative + false_positive)

    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative) / 2
    
    recall_avg = (recall_positive + recall_negative) / 2

    f1_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[Tweets2013 messages]")
    print("[messages evaluated]: " + str(len(tweets_2013)))
    print("[correct evaluations]: " + str(true_positive + true_negative) + " (" + str(true_positive) + " positives and " + str(true_negative) + " negatives)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(accuracy))
    print("[precision_avg]: " + str(precision_avg))
    print("[recall avg]: " + str(recall_avg))
    print("[f1 avg]: " + str(f1_avg))


# Evaluate only the Tweets2014
def evaluateTweets2014Messages(model):
    global tweets_2014
    global tweets_2014_score

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_avg = 0

    # only 2013 for while
    for index, item in enumerate(tweets_2014): 
        message = str(tweets_2014[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("x", message)
        #print(model_analysis)
        #print(str(eval(model_analysis)))
        result = eval(model_analysis)

        if result > 0:
            if tweets_2014_score[index] > 0:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if tweets_2014_score[index] < 0:
                true_negative += 1
            else:
                false_negative += 1

    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)

    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)

    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)

    if true_positive + false_negative > 0:
        recall_positive = true_positive / (true_positive + false_negative)

    if true_negative + false_positive > 0:
        recall_negative = true_negative / (true_negative + false_positive)

    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative) / 2
    
    recall_avg = (recall_positive + recall_negative) / 2

    f1_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[Tweets2014 messages]")
    print("[messages evaluated]: " + str(len(tweets_2014)))
    print("[correct evaluations]: " + str(true_positive + true_negative) + " (" + str(true_positive) + " positives and " + str(true_negative) + " negatives)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(accuracy))
    print("[precision_avg]: " + str(precision_avg))
    print("[recall avg]: " + str(recall_avg))
    print("[f1 avg]: " + str(f1_avg))


# Evaluate only the SMS2013
def evaluateSMS2013(model):
    global sms_2013
    global sms_2013_score

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_avg = 0

    # only 2013 for while
    for index, item in enumerate(sms_2013): 
        message = str(sms_2013[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("x", message)
        #print(model_analysis)
        #print(str(eval(model_analysis)))
        result = eval(model_analysis)

        if result > 0:
            if sms_2013_score[index] > 0:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if sms_2013_score[index] < 0:
                true_negative += 1
            else:
                false_negative += 1

    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)

    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)

    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)

    if true_positive + false_negative > 0:
        recall_positive = true_positive / (true_positive + false_negative)

    if true_negative + false_positive > 0:
        recall_negative = true_negative / (true_negative + false_positive)

    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative) / 2
    
    recall_avg = (recall_positive + recall_negative) / 2

    f1_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[SMS2013 messages]")
    print("[messages evaluated]: " + str(len(sms_2013)))
    print("[correct evaluations]: " + str(true_positive + true_negative) + " (" + str(true_positive) + " positives and " + str(true_negative) + " negatives)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(accuracy))
    print("[precision_avg]: " + str(precision_avg))
    print("[recall avg]: " + str(recall_avg))
    print("[f1 avg]: " + str(f1_avg))



# Evaluate only the Tweets2014
def evaluateTweetsLiveJournal2014(model):
    global tweets_liveJournal2014
    global tweets_liveJournal2014_score

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_avg = 0

    # only 2013 for while
    for index, item in enumerate(tweets_liveJournal2014): 
        message = str(tweets_liveJournal2014[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("x", message)
        #print(model_analysis)
        #print(str(eval(model_analysis)))
        result = eval(model_analysis)

        if result > 0:
            if tweets_liveJournal2014_score[index] > 0:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if tweets_liveJournal2014_score[index] < 0:
                true_negative += 1
            else:
                false_negative += 1

    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)

    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)

    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)

    if true_positive + false_negative > 0:
        recall_positive = true_positive / (true_positive + false_negative)

    if true_negative + false_positive > 0:
        recall_negative = true_negative / (true_negative + false_positive)

    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative) / 2
    
    recall_avg = (recall_positive + recall_negative) / 2

    f1_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("[LiveJournal2014 messages]")
    print("[messages evaluated]: " + str(len(tweets_liveJournal2014)))
    print("[correct evaluations]: " + str(true_positive + true_negative) + " (" + str(true_positive) + " positives and " + str(true_negative) + " negatives)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(accuracy))
    print("[precision_avg]: " + str(round(precision_avg, 2)))
    print("[recall avg]: " + str(round(recall_avg, 2)))
    print("[f1 avg]: " + str(round(f1_avg, 2)))



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

    message = ""
    model_analysis = ""
    result = 0

    # parameters to calc the metrics
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    accuracy = 0
    
    precision_positive = 0
    precision_negative = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_avg = 0

    allMessages = tweets_2013 + tweets_2014 + tweets_liveJournal2014 + sms_2013
    allScores   = tweets_2013_score + tweets_2014_score + tweets_liveJournal2014_score + sms_2013_score

    # only 2013 for while
    for index, item in enumerate(allMessages): 
        message = str(allMessages[index]).strip().replace("'", "")
        message = "'" + message + "'"

        model_analysis = model.replace("x", message)
        #print(model_analysis)
        #print(str(eval(model_analysis)))
        result = eval(model_analysis)

        if result > 0:
            if allScores[index] > 0:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if allScores[index] < 0:
                true_negative += 1
            else:
                false_negative += 1
    
    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)

    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)

    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)

    if true_positive + false_negative > 0:
        recall_positive = true_positive / (true_positive + false_negative)

    if true_negative + false_positive > 0:
        recall_negative = true_negative / (true_negative + false_positive)

    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)

    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative) / 2
    
    recall_avg = (recall_positive + recall_negative) / 2

    f1_avg = (f1_positive + f1_negative) / 2         

    print("\n")
    print("Evaluate all messages")
    print("[messages evaluated]: " + str(len(allMessages)))
    print("[correct evaluations]: " + str(true_positive + true_negative) + " (" + str(true_positive) + " positives and " + str(true_negative) + " negatives)")
    print("[model]: " + str(model))
    print("[accuracy]: " + str(round(accuracy, 2)))
    print("[precision_avg]: " + str(round(precision_avg, 2)))
    print("[recall avg]: " + str(round(recall_avg, 2)))
    print("[f1 avg]: " + str(round(f1_avg, 2)))


if __name__ == "__main__":
    getDictionary()
    getTestTweetsFromSemeval2014()

    evaluateTweets2013Messages("polaritySum(x)")
    evaluateTweets2014Messages("polaritySum(x)")
    evaluateSMS2013("polaritySum(x)")
    evaluateTweetsLiveJournal2014("polaritySum(x)")
    evaluateAllMessages("polaritySum(x)")


end = time.time()
print("\n\nScript ends after " + str(format(end - start, '.3g')) + " seconds")