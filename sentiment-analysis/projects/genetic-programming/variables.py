# Airton Bordin Junior
# airtonbjunior@gmail.com
# Federal University of Goias (UFG)
# Computer Science Master's Degree

from nltk.corpus import stopwords

SEMEVAL_TRAIN_FILE = 'datasets/twitter-train-cleansed-B.txt'
SEMEVAL_TEST_FILE  = 'datasets/test/SemEval2014-task9-test-B-all-tweets.txt'
DICTIONARY_POSITIVE_WORDS = 'dictionaries/positive-words.txt'
DICTIONARY_NEGATIVE_WORDS = 'dictionaries/negative-words.txt'
DICTIONARY_POSITIVE_HASHTAGS  = 'dictionaries/positive-hashtags.txt'
DICTIONARY_NEGATIVE_HASHTAGS  = 'dictionaries/negative-hashtags.txt'
DICTIONARY_POSITIVE_EMOTICONS = 'dictionaries/positive-emoticons.txt'
DICTIONARY_NEGATIVE_EMOTICONS = 'dictionaries/negative-emoticons.txt'
DICTIONARY_NEGATING_WORDS = 'dictionaries/negating-word-list.txt'

MAX_POSITIVES_TWEETS = 1400
MAX_NEGATIVES_TWEETS = 1400
MAX_NEUTRAL_TWEETS   = 1400

GENERATIONS = 60
POPULATION  = 10
generations_unchanged = 0
max_unchanged_generations = 10000

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

tweets_liveJournal2014       = []
tweets_liveJournal2014_score = []
tweets_liveJournal2014_positive = 0
tweets_liveJournal2014_negative = 0
tweets_liveJournal2014_neutral  = 0

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

stop_words_function_used = False
stem_function_used = False
remove_dots_function_used = False
remove_links_function_used = False
remove_ellipsis_function_used = False
remove_all_ponctuaction_function_used = False

negative_words_quantity_cache = -1
positive_words_quantity_cache = -1

log_all_messages = False
MAX_ANALYSIS_TWEETS = 10000

false_neutral_log  = 0
false_negative_log = 0
false_positive_log = 0

log_parcial_results = True

stop_words = set(stopwords.words('english'))