# Dataset: Polarity dataset v2.0
# http://www.cs.cornell.edu/people/pabo/movie-review-data/
#
import sys
import os
import time

import csv
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

def usage():
    print("Usage:")
    print("python %s <data_dir>" % sys.argv[0])

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

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
            train_vectors, test_vectors, train_labels, test_labels = pickle.load(f)

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
                print i
                i+=1
                import random
                line[0] = unicode(line[0], errors='replace')
                if random.randint(1,10) == 1:
                    test_data.append(line[3])
                    test_labels.append(int(line[1]))
                else:
                    train_data.append(line[3])
                    train_labels.append(int(line[1]))



        print "creating vectorizer"
        # Create feature vectors
        vectorizer = TfidfVectorizer(min_df=5,
                                     max_df = 0.8,
                                     sublinear_tf=True,
                                     use_idf=True)

        train_vectors = vectorizer.fit_transform(train_data)
        test_vectors = vectorizer.transform(test_data)
        with open("pickles/train_vector.pkl","w") as f:
            pickle.dump((train_vectors, test_vectors, train_labels, test_labels ),f)


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

    print "vectorizing input tweets..."
    

    print "predicting input tweets..."
    unknown_liblinear = classifier_liblinear.predict(test_vectors)
    t3 = time.time()


    time_liblinear_train = t1-t0
    time_liblinear_predict = t2-t1
    time_liblinear_guess = t3-t2



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
    print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    print(classification_report(test_labels, prediction_liblinear))
