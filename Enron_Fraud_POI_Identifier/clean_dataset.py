"""
Clean dataset and add new features
"""

def replace_nans_with_zeroes(dataset):
    '''Replace 'NaN' with zeroes for each field in dataset'''
    dataset_keys = dataset.keys()
    any_key = next(iter(dataset_keys))
    features = dataset[any_key].keys()
    
    # Loop through features
    for feature in features:
        for item in dataset:
            if dataset[item][feature] == 'NaN':
                dataset[item][feature] = 0
                
def add_features(dataset):
    '''Add features to dataset'''
    for item in dataset:
        dataset[item]['total_money'] = \
            dataset[item]['total_payments'] + \
            dataset[item]['total_stock_value']
        dataset[item]['total_poi_emails'] = \
            dataset[item]['from_poi_to_this_person'] + \
            dataset[item]['from_this_person_to_poi'] + \
            dataset[item]['shared_receipt_with_poi']