# -*- coding: utf-8 -*-
import praw
import io
from praw.models import MoreComments


# User/Pass optional if access only public content 
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/sentiment_analysis)',
                     client_id='404ucZurD8NCyg', 
                     client_secret="HUNj14gPjK7Ua5rzDBqUIV5-CVo") 

# Enconding problem solved on [1]
file = io.open("D:/redditdata-cancer.txt", "w", encoding='utf-8') 

for submissions in reddit.subreddit('cancer').top('all'):
    # submissions parameter has the id of the topic
    for comment in reddit.submission(id=submissions).comments.list():
    	#print(comment.body.encode('utf-8'))
    	file.write(comment.body) 




# Coments/References
#[1] https://www.reddit.com/r/redditdev/comments/4vsksc/prawtheard_scraper_stops_iterating_midway/