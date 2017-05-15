# -*- coding: utf-8 -*-
import praw
import io
import time
from praw.models import MoreComments


start = time.time()

# User/Pass optional if access only public content 
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/sentiment_analysis)',
                     client_id='404ucZurD8NCyg', 
                     client_secret="HUNj14gPjK7Ua5rzDBqUIV5-CVo") 

# Enconding problem solved on [1]
file = io.open("D:/redditdata-cancer.txt", "w", encoding='utf-8') 

for submissions in reddit.subreddit('cancer').hot(limit=100000000):
    # submissions parameter has the id of the topic
    for comment in reddit.submission(id=submissions).comments.list():
    	# [2] to solve MoreComents problem
    	if isinstance(comment, MoreComments):
        	continue
    	file.write(comment.body) 

end = time.time()

print("Script ends after " + str(format(end - start, '.3g')) + " seconds")


# Coments/References
#[1] https://www.reddit.com/r/redditdev/comments/4vsksc/prawtheard_scraper_stops_iterating_midway/
#[2] http://praw.readthedocs.io/en/latest/tutorials/comments.html?highlight=has%20no%20attribute%20body