import praw
import csv

reddit = praw.Reddit(client_id='HDUejy8lyaO-uw',
                     client_secret='dkQB2xSpT9GpqWwZcePnynZVd6g',
                     user_agent='Linux:BuzzWordTrading:0.1 (by /u/BuzzWordTrading)')

go_list = []

with open("constituents.csv","rb") as f:
    csv_file = csv.reader(f)
    for row in csv_file:
        #go_list.append(row[0])
        go_list.append(row[1].lower())

go_list = set(go_list)

for submission in reddit.subreddit('news').top(limit=999999):
    text = submission.title + ' ' + submission.selftext
    text = text.lower()
    for check in [(go_word in text, go_word) for go_word in go_list]:
        if check[0]:
            print check[1], submission.shortlink
        
