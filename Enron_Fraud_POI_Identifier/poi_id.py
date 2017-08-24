#!/usr/bin/python

import sys
import pickle
import numpy as np
sys.path.append("../tools/")

from explore_dataset import dataset_basics
from clean_dataset import replace_nans_with_zeroes
from clean_dataset import add_features
from evaluate_poi import evaluate_classifier
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Load the dictionary containing the dataset
data_dict = {}
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)
    
# Clean the data set
del data_dict['TOTAL']
del data_dict['THE TRAVEL AGENCY IN THE PARK']
del data_dict['LOCKHART EUGENE E'] # No financial data for this employee

# Basic exploration
dataset_basics(data_dict)
    
# Handle NaNs
replace_nans_with_zeroes(data_dict)
    
# Add features
add_features(data_dict)

### Feature selection (first must be 'poi')
# All of these feature combinations were tested
#features_list = ['poi', 'salary', 'bonus', 'long_term_incentive', 'deferred_income', 'deferral_payments', 'loan_advances', 'other', 'expenses', 'director_fees']
#features_list = ['poi', 'salary', 'bonus', 'deferred_income', 'other', 'expenses']
#features_list = ['poi', 'salary', 'bonus', 'other', 'expenses']
#features_list = ['poi', 'exercised_stock_options', 'restricted_stock', 'restricted_stock_deferred']
#features_list = ['poi', 'exercised_stock_options', restricted_stock']
#features_list = ['poi', 'to_messages', 'from_messages', 'from_poi_to_this_person', 'from_this_person_to_poi', 'shared_receipt_with_poi']
#features_list = ['poi', 'total_money', 'total_poi_emails']

# Final features selected based on best model performance using Decision Tree Classifier with no parameters
# Precision and recall scores were between 0.35 and 0.37 for each run
features_list = ['poi', 'salary', 'bonus', 'expenses']

data = featureFormat(data_dict, features_list)
poi, finance_features = targetFeatureSplit(data)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Create classifier
#from sklearn.naive_bayes import GaussianNB
from sklearn import tree

#clf = GaussianNB() used to test final features_list compared to DecisionTreeClassifier() below
#clf = tree.DecisionTreeClassifier() used to test features initially

# Parameters tuned in attempt to improve Precision and Recall scores for final features_list
#clf = tree.DecisionTreeClassifier(min_samples_split=3)
#clf = tree.DecisionTreeClassifier(min_samples_split=4)
#clf = tree.DecisionTreeClassifier(min_samples_split=5)
#clf = tree.DecisionTreeClassifier(min_samples_split=10)

#clf = tree.DecisionTreeClassifier(max_leaf_nodes=500)
#clf = tree.DecisionTreeClassifier(max_leaf_nodes=100)
#clf = tree.DecisionTreeClassifier(max_leaf_nodes=50)
#clf = tree.DecisionTreeClassifier(max_leaf_nodes=10)
#clf = tree.DecisionTreeClassifier(max_leaf_nodes=5)

#clf = tree.DecisionTreeClassifier(min_samples_split=3, max_leaf_nodes=10)
#clf = tree.DecisionTreeClassifier(min_samples_split=5, max_leaf_nodes=10)

# Final parameters chosen due to better Precision and Recall scores
clf = tree.DecisionTreeClassifier(min_samples_split=4, max_leaf_nodes=10)

# Evaluation
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

evaluate_classifier(clf, features_train, labels_train, features_test, labels_test)

# Note feature importance (comment out when using the GaussianNB classifier)
print("\n")
print("Feature Importance:", clf.feature_importances_)
print("\n")
    
# Dump your classifier, dataset, and features_list
dump_classifier_and_data(clf, my_dataset, features_list)