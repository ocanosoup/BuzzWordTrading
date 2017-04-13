# -*- coding: utf-8 -*-
import sys, traceback
import sys,getopt,got,datetime,codecs
import csv

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		print("""\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n

 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n""")
		return

        opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))

        tweetCriteria = got.manager.TweetCriteria()

	try:
		tweetCriteria = got.manager.TweetCriteria()

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

		with codecs.open("output_got.csv", "w+", "utf-8") as csvfile:

                        fieldnames = ['username', 'date', 'retweets','favorites','text','geo','mentions','hashtags','id','permalink']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        print('Searching...\n')

                        def receiveBuffer(tweets):
                                for t in tweets:
                                        try:
                                                data = {'username':t.username, 
                                                'date':t.date.strftime("%Y-%m-%d %H:%M"), 
                                                'retweets':t.retweets,
                                                'favorites':t.favorites,
                                                'text':t.text.encode("ascii", "ignore"),
                                                'geo':t.geo,
                                                'mentions':t.mentions,
                                                'hashtags':t.hashtags,
                                                'id':t.id,
                                                'permalink':t.permalink
                                                }
                                        
                                                writer.writerow(data)
                                        except UnicodeEncodeError as e:
                                            print e
                                csvfile.flush();
                                print('%d more saved to file...\n' % len(tweets))

                        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except Exception as e:
		print 'Arguments parser error, try -h', e
                traceback.print_exc(file=sys.stdout)
	finally:
		print('Done. Output file generated "output_got.csv".')

if __name__ == '__main__':
	main(sys.argv[1:])
