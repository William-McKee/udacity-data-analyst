# Enron Persons of Interest Identifier

This code analyzes the Enron data set and identifies persons of interest (POIs) using a machine learning algorithm.  Persons of interest in the Enron corporate fraud case are individuals who were indicted, made a plea deal or settlement, or testified in exchange for immunity from federal prosecution.

## File Contents

1. **poi_id.py**: Python code which reads data, explores the data set, selects features, splits the data, and trains the data.
2. **explore_dataset.py**: Python code which examines the data set and prints features including the number of data points, number of POIs, known feature counts, and feature splits between POIs and non-POIs.
3. **clean_dataset.py**: Python functions to clean NaNs and add features.
4. **feature_format.py**: Python code which converts data to a format useful for sklearn classifiers (provided by Udacity).
5. **evaluate_poi.py**: Python code which fits training data and makes predictions on testing data (provided by Udacity).
6. **tester.py**: Python code containing functions which reads/writes classifier, datasets, and features lists from/to output files. Code also includes a function which tests the classifier on the contents of the output files (provided by Udacity).
7. **Project Submission Answers.pdf**: Answers to project questions.

All files shall be downloaded in the same directory.

## Running the code

The source code is written in Python 3.6.  Python 3.6 is available [here](https://www.python.org/downloads/).

The code can be run in any Python source code editor.  Anaconda is available [here](https://www.continuum.io/downloads).  Install for Python 3.X series.