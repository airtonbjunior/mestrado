import praw
from praw.models import MoreComments


# User/Pass optional if access only public content 
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/sentiment_analysis)',
                     client_id='404ucZurD8NCyg', 
                     client_secret="HUNj14gPjK7Ua5rzDBqUIV5-CVo") 

#testing some post of r/cancer/ subreddit
submission = reddit.submission(url='https://www.reddit.com/r/cancer/comments/5bjnpi/best_chemo_buddy/')

submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
    print(comment.body)