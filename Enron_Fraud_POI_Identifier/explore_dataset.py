"""
Explore basic information about the data set
"""

import numpy as np

def explore_basics(dataset):
    '''Print basic statistics about dataset'''
    print("Data Set Basics")
    print("Number of employees/vendors? ", len(dataset))
    print("Number of persons of interest (POIs)? ", get_feature_valid_points_count(dataset, 'poi', 0))
    print("How many features?", get_feature_count(dataset))
    
    
def get_feature_count(dataset):
    '''How many features?'''
    dataset_keys = dataset.keys()
    #dataset_values = dataset.values()
    any_key = next(iter(dataset_keys))
    return len(dataset[any_key])
    
    
def get_feature_valid_points_count(dataset, feature, bad_value):
    '''
    How many points in data set?
    dataset: dictionary containing list of people, where each person is represented by dictionary
    feature: feature for which to find valis data points
    bad_value: for valid point, feature != this value
    '''
    count=0
    dataset_keys = dataset.keys()
    for item in dataset_keys:
        if dataset[item][feature] != bad_value:
            count += 1
    return count


def get_bad_value(feature):
    '''Return bad value for feature'''
    if feature == 'poi':
        return 0
    else:
        return 'NaN'
    

def explore_features(dataset):
    '''Get and print count of all features of dataset'''
    # Get the list of features
    dataset_keys = dataset.keys()
    any_key = next(iter(dataset_keys))
    features = dataset[any_key].keys()
    
    # Loop through features
    for feature in features:
        bad_value = get_bad_value(feature)
        count = get_feature_valid_points_count(dataset, feature, bad_value)
        print(str(feature) + ": " + str(count))
            
            
def explore_metrics(dataset):
    '''Get and print metrics of all features of dataset'''
    # Get the list of features
    dataset_keys = dataset.keys()
    any_key = next(iter(dataset_keys))
    features = dataset[any_key].keys()
    
    # Loop through features
    for feature in features:
        feature_list = []
        bad_value = get_bad_value(feature)
        for item in dataset:
            if dataset[item][feature] != bad_value:
                feature_list.append(dataset[item][feature])
        np_feature = np.array(feature_list)
        if (feature != 'email_address' and np_feature.size > 0):
            print(feature + ": " + str(np_feature.size) + " / " + str(np_feature.min()) + " / " + str(np_feature.mean()) +  " / " + str(np_feature.max()))
        else:
            print(feature + ": 0 / 0.000 / 0.000 / 0.000")
            
def dataset_basics(dataset):
    '''Explore top level information about the dataset,
       including POI and non-POI'''
       # Print dataset information
    print("\n")
    explore_basics(dataset)

    print("\n")
    print("How many known values for each feature?")
    explore_features(dataset)

    # Split data set into POI and non-POI
    poi_dataset = {}
    nonpoi_dataset = {}
    for item in dataset:
        if dataset[item]['poi'] == 1:
            poi_dataset[item] = dataset[item]
        else:
            nonpoi_dataset[item] = dataset[item]

    print("\n")
    print("How many known values for each feature for POIs?")
    explore_features(poi_dataset)

    print("\n")
    print("How many known values for each feature for non-POIs?")
    explore_features(nonpoi_dataset)
        
    print("\n")
    print("### METRICS ###")
    print("Field: Min / Mean / Max")
    explore_metrics(dataset)

    print("\n")
    print("### POI METRICS ###")
    print("Field: Min / Mean / Max")
    explore_metrics(poi_dataset)

    print("\n")
    print("### NON-POI METRICS ###")
    print("Field: Min / Mean / Max")
    explore_metrics(nonpoi_dataset)
    print("\n")