"""
Evaulate classifier
"""

import numpy as np
from sklearn.metrics import classification_report

def evaluate_classifier(clf, features_train, labels_train, features_test, labels_test):
    '''Perform training on classifier and make predictions
       clf = classifier
       features_train = features for training points
       labels_train = correct answers for training points
       features_test = features for testing points
       labels_test = correct answers for testing points
    '''
    # Fit training data
    clf = clf.fit(features_train, labels_train)

    # Accuracy
    accuracy= clf.score(features_test, labels_test)
    print("Accuracy: ", accuracy)

    # Predictions
    predict = clf.predict(features_test)

    no_cpp = np.sum([1 for j in zip(labels_test, predict) if j[0] == j[1] and j[1] == 1])
    print("Number of Correct Positive Predictions: ", no_cpp)
    print(classification_report(labels_test, predict))