# Dataset: Polarity dataset v2.0
# http://www.cs.cornell.edu/people/pabo/movie-review-data/
#
import sys
import os
import time

import csv
import pickle
import getopt,got,datetime,codecs
import argparse
from collections import OrderedDict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

import numpy as np
import matplotlib.pyplot as plt

import random

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get tweet sentiment for a query over a period of time')

    parser.add_argument('--since', dest='since', type=str, required=True)
    parser.add_argument('--until', dest='until', type=str, required=True)
    parser.add_argument('--user', dest='user', type=str, default=None)
    parser.add_argument('--query', dest='query', type=str, default=None)

    args = parser.parse_args()

    filename='output/output'
    for arg in args.__dict__:
        try:
            filename += '_' + args.__dict__[arg].replace(' ','')
        except:
            print "missing " + arg

    # Create feature vectors
    vectorizer = None

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []

    train_vectors = None
    test_vectors = None
    try:
        with open("pickles/train_vector.pkl","r") as f:
            print "loading vectorizer"
            train_vectors, test_vectors, train_labels, test_labels, vectorizer = pickle.load(f)

    except Exception as e:
        data_dir = sys.argv[1]

        i = 0

        fname = 'SAD.csv'

        csvreader = None
        with open(fname,'r') as csvfile:
            csvreader = csv.reader(csvfile)

            head = next(csvreader, None)
            for line in csvreader:
                if len(line) == 0:
                    continue
                if i%100000==0:
                    print i
                i+=1
                line[0] = unicode(line[0], errors='replace')
                if random.randint(1,10) == 1:
                    test_data.append(line[3])
                    test_labels.append(int(line[1]))
                else:
                    train_data.append(line[3])
                    train_labels.append(int(line[1]))

        print "creating vectorizer"
        vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.8,
                                 max_features = 70000, 
                                 sublinear_tf=True,
                                 use_idf=True)

        train_vectors = vectorizer.fit_transform(train_data)
        test_vectors = vectorizer.transform(test_data)
        with open("pickles/train_vector.pkl","w") as f:
            pickle.dump((train_vectors, test_vectors, train_labels, test_labels, vectorizer ),f)


    '''
    print "creating rbf classifier"
    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    t0 = time.time()
    classifier_rbf.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_rbf = classifier_rbf.predict(test_vectors)
    t2 = time.time()
    time_rbf_train = t1-t0
    time_rbf_predict = t2-t1

    print "creating SVC classifier"
    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1
    '''

    #with open('pickles/classifier.pkl','r') as f:

    t0 = time.time()
    classifier_liblinear = None
    try:
        with open("pickles/linearSVC.pkl","r") as f:
            print "loading vectorizer"
            classifier_liblinear = pickle.load(f)


    except Exception as e:
        print "creating linearSVC classifier"
        # Perform classification with SVM, kernel=linear
        classifier_liblinear = svm.LinearSVC()
        classifier_liblinear.fit(train_vectors, train_labels)
        with open("pickles/linearSVC.pkl","w") as f:
            pickle.dump(classifier_liblinear,f)

    if classifier_liblinear == None:
        raise Exception("Bad PKL file...")

    t1 = time.time()
    prediction_liblinear = classifier_liblinear.predict(test_vectors)
    t2 = time.time()

    ''' ********************* Get New Tweets ************************
        This is the section where we get the tweets and build the Vector
        for the input data and write to a CSV for further study.
        The CSV format should be:
            Score, Time
        And the file should be named after the tweet querysearch
        ************************************************************** '''

    hist = OrderedDict()

    print "getting tweets..."
    counter = 0

    tweetCriteria = got.manager.TweetCriteria().setMaxTweets(100000000)

    if args.user is not None:
        tweetCriteria.username = args.user
    if args.query is not None:
        tweetCriteria.querySearch = args.query
    if args.until is not None:
        tweetCriteria.until = args.until
    if args.since is not None:
        tweetCriteria.since = args.since


    def receiveBuffer(tweets):
        import time
        time.sleep(15)
        global counter
        counter += len(tweets)
        unknown_data = []
        unknown_dates = []
        for t in tweets:
            try:
                date = t.date.strftime("%Y-%m-%d %H")
                unknown_data.append(t.text.encode("ascii", "ignore"))
                unknown_dates.append(date)
                if not date in hist: hist[date] =  {'pos':0,'neg':0}

            except UnicodeEncodeError as e:
                print e

        print('%s - predicting %d more tweets...' % (unknown_dates[0], len(tweets)))
        ts = time.time()
        unknown_vectors = vectorizer.transform(unknown_data)
        unknown_liblinear = classifier_liblinear.predict(unknown_vectors)
        te = time.time()
        ptime = te - ts
        print 'Prediction Time: %fs' % ptime

        for i, sentiment in enumerate(unknown_liblinear):
            #data = {}
            if sentiment == 0:
                hist[unknown_dates[i]]['neg'] += 1
                #data['neg'] = unknown_dates[i]
            else:
                hist[unknown_dates[i]]['pos'] += 1
                #data['pos'] = unknown_dates[i]

            #writer.writerow(data)

    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
    print "{} tweets in total".format(counter)

    with open(filename+'.csv', 'w') as csvfile:

        fieldnames = ['date','pos','neg']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in hist:
            line = {}
            line['date'] = item
            line['pos'] = hist[item]['pos']
            line['neg'] = hist[item]['neg']
            writer.writerow(line)


    ''' ********************* Plot Twitter Data **********************
        In this section we plot the Twitter sentiment data. We should
        plot a plot with pos above neg, pos next to neg, the
        difference in a gains/loss format. and potentially also plot
        the stockmarket data
        ************************************************************** '''

    dates = []
    neg = []
    pos = []
    diff = []
    for date in reversed(hist):
        dates.append(date)
        neg.append(hist[date]['neg']*-1)
        pos.append(hist[date]['pos'])
        diff.append(neg[-1]+pos[-1])

    n_groups = len(dates)

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.5

    opacity = 0.4

    rects1 = plt.bar(index, pos, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Positive')

    rects2 = plt.bar(index, neg, bar_width,
                     alpha=opacity,
                     color='r',
                     label='Negative')

    plt.xlabel('Datetime (Year-Month-Day hour)')
    plt.ylabel('Number of Tweets')
    plt.title('Histogram of Positive and Negative (Above and Below) Tweets Matching the Query "{}"'.format(args.query))
    plt.xticks(index + bar_width / 2, dates, rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename+'_1.png', bbox_inches='tight')


    # New plot
    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.5

    opacity = 0.4

    rects1 = plt.bar(index, diff, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Difference')

    plt.xlabel('Datetime (Year-Month-Day hour)')
    plt.ylabel('Difference (Positives - Negatives)')
    plt.title('Histogram of the Difference of Sentiments in Tweets Matching the Query "{}"'.format(args.query))
    plt.xticks(index + bar_width / 2, dates, rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename+'_2.png', bbox_inches='tight')

    #new plot
    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4

    rects1 = plt.bar(index, pos, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Positive')

    def double(x): return x*-1
    rects2 = plt.bar(index+bar_width, list(map(double, neg)), bar_width,
                     alpha=opacity,
                     color='r',
                     label='Negative')

    plt.xlabel('Datetime (Year-Month-Day hour)')
    plt.ylabel('Number of Tweets')
    plt.title('Histogram of Positive and Negative (Side-by-Side) Tweets Matching the Query "{}"'.format(args.query))
    plt.xticks(index + bar_width / 2, dates, rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename+'_3.png', bbox_inches='tight')

    '''
    print "vectorizing input tweets..."
    with open('output_got.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)

        head = next(csvreader, None)
        for line in csvreader:
            if len(line) == 0:
                continue
            unknown_data.append(line[4])
    '''

    '''
    buy = 0
    sell = 0
    for sentiment in unknown_liblinear:
        if sentiment == 1:
            buy += 1
        if sentiment == 0:
            sell += 1

    print "Buy/Sell: {}/{}".format(buy,sell)
    '''

    time_liblinear_train = t1-t0
    time_liblinear_predict = t2-t1

    '''
    # Print results in a nice table
    print("Results for SVC(kernel=rbf)")
    print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
    print(classification_report(test_labels, prediction_rbf))
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction_linear))
    '''

    print len(test_labels),test_labels[:10]
    print len(prediction_liblinear),prediction_liblinear[:10]

    print("Results for LinearSVC()")
    print("Training time: %fs; Prediction time(Test): %fs" % (time_liblinear_train, time_liblinear_predict))
    print(classification_report(test_labels, prediction_liblinear))

