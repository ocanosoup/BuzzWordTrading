import praw
import csv
import argparse
import time
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("sub")
parser.add_argument("start")
parser.add_argument("end")
args = parser.parse_args()

reddit = praw.Reddit(client_id='HDUejy8lyaO-uw',
                     client_secret='dkQB2xSpT9GpqWwZcePnynZVd6g',
                     user_agent='Linux:BuzzWordTrading:0.1 (by /u/BuzzWordTrading)')

go_list = {}

with open("constituents.csv","rb") as f:
    csv_file = csv.reader(f)
    for row in csv_file:
        #go_list.append(row[0])
        go_list[row[1].lower()]=row[0]


start = datetime.strptime(args.start, '%Y-%m-%d').total_seconds()
end = datetime.strptime(args.end, '%Y-%m-%d').total_seconds()

for submission in reddit.subreddit(args.sub).submissions(start, end):
    if submission.score < 5000:
        continue
    text = submission.title + ' ' + submission.selftext
    text = text.lower()
    for check in [(go_word in text, go_word) for go_word in go_list]:
        if check[0]:
            created = time.strftime("%Y-%m-%d", time.localtime(submission.created))
            print go_list[check[1]], submission.shortlink, created, submission.score
        
