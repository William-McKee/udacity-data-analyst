#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "addr:street"
"""

import re

DIRECTIONALS = { "E": "East",
                 "E.": "East",
                 "N": "North",
                 "N.": "North",
                 "S": "South",
                 "S.": "South",
                 "W": "West",
                 "W.": "West"}

STREET_TYPE_RE = re.compile(r'\b\S+\.?$', re.IGNORECASE)

STREET_TYPE_EXPECTED = ["Avenue", "Boulevard", "Circle", "Commons", "Court", "Drive", "Highway", "Lane", "Parkway", 
                        "Pike", "Place", "Road", "Square", "Street", "Terrace", "Trail", "Turnpike", "Way"]


STREET_TYPE_MAPPING = { "Ave": "Avenue",
                        "Ave.": "Avenue",
                        "AVE": "Avenue",
                        "Blvd": "Boulevard",
                        "Blvd.": "Boulevard",
                        "Cir": "Circle",
                        "Ct": "Court",
                        "Dr": "Drive",
                        "Hwy": "Highway",
                        "Ln": "Lane",
                        "PIke": "Pike",
                        "Rd": "Road",
                        "Rd.": "Road",
                        "RD": "Road",
                        "ROAD": "Road",
                        "St": "Street",
                        "St.": "Street",
                        "ST": "Street",
                        "Sstreet": "Street",
                        "Steet": "Street",
                        "Ter": "Terrace"
                      }

ROUTE_INDICATORS = ["Rt", "Rte", "Route", "PA", "NJ", "US", "I", "Interstate"]

KNOWN_STREETS = ["Market", "Chestnut", "Spruce", "Spring Garden"]


def audit_street_type(street_types, street_name):
    '''
    This function was used to determine which street types do not fit in an expected list
    of street types.  This function is part of the Udacity Data Analyst Nanodegree Course
    '''
    
    # Search for street type
    m = STREET_TYPE_RE.search(street_name)

    # Group streets by type
    if m:
        street_type = m.group()
        if street_type not in STREET_TYPE_EXPECTED:
            street_types[street_type].add(street_name)
            
            
def check_for_numbered_street(words):
    '''
    This function checks for numbered street values
    words = list of words forming the street value (e.g., "23rd")
    '''
    return_value = False

    if (len(words) > 1):
        return False
    
    suffixes = ["th", "st", "nd", "rd"]
    word_num = words[0][:-2]
    word_suffix = words[0][-2:]
        
    # Is first part a number
    try:
        num = int(word_num)
    except ValueError:
        return_value = False    
    else:
        # Is second part a suffix
        if (word_suffix.lower() in suffixes):
            return_value = True
    
    return return_value


def check_for_short_entry(words):
    '''
    This function checks the Open Street Map value when the street type may be missing
    words = list of words forming the street value (e.g., "North 23rd")
    '''
    new_words = words
    
    # If first word is a directional, exclude from the check
    words_to_check = words
    if (words_to_check[0] in DIRECTIONALS.values()):
        words_to_check = words_to_check[1:]
    
    # Check for known street ('Chestnut' without 'Street'; '25th' without 'Street')
    if (" ".join(words_to_check) in KNOWN_STREETS or check_for_numbered_street(words_to_check)):
        new_words = []
        for i in range(len(words)):
            new_words.append(words[i])
        new_words.append("Street")
        
    return new_words


def clean_unusual_street_type(words):
    '''
    This function cleans the Open Street Map value when the street type does not match an item in
    an expected list of street types (.e.g., not a street, avenue, road, boulevard, court, etc.)
    words = list of words forming the street value (e.g., "West Route 73")
    '''
    
    new_words = words
    
    # Is the last item a number as part of a route (Example: 'PA Route 73'?)
    last_number = 'NaN'
    try:
        last_number = int(words[-1])
    except ValueError:
        # Last item is not a number - move onto next section
        pass
    else:
        # If we don't have a route, we need to modify
        if (len(words) == 1 or words[-2] not in ROUTE_INDICATORS):
            last_number = 'NaN'
        
    # Find last instance of street type or variant and drop off the excess (Example: 'Street Road #115' becomes 'Street Road')
    if (last_number == 'NaN'):
        last_index = -1
        for i in range(len(words) - 1, 0, -1):
            if words[i] in STREET_TYPE_EXPECTED or words[i] in STREET_TYPE_MAPPING.keys():
                last_index = i
                break
            
        # If street type or variant is found
        if (last_index >= 0):
            # Yes, we found street type or variant
            new_words = []
            for i in range(last_index + 1):
                new_words.append(words[i])
        else:
            # No, check for short entry (e.g., "Chestnut" or "33rd")?
            new_words = check_for_short_entry(words)

    return new_words


def clean_street(in_tag_value):
    '''
    This function cleans the values within the Open Street Map street types
    in_tag_value = Open Street Map value from the street type key (e.g, "Front Street")
    '''
    tag_value = in_tag_value
    
    # Capitalize each word
    words = [word[0].upper() + word[1:] for word in tag_value.split()]
    tag_value = " ".join(words)

    # Standardize directional streets
    words = tag_value.split()
    if (words[0] in DIRECTIONALS.keys()):
        words[0] = DIRECTIONALS[words[0]]
        
    # Is last word a street type or variant?
    if (words[-1] not in STREET_TYPE_EXPECTED and words[-1] not in STREET_TYPE_MAPPING.keys()):
        words = clean_unusual_street_type(words)

    # Street type is last word
    # Standarize the street type
    if (words[-1] in STREET_TYPE_EXPECTED):
        # Street type is already standarized
        pass
    elif (words[-1] in STREET_TYPE_MAPPING.keys()):
        # Last word is street type variant
        words[-1] = STREET_TYPE_MAPPING[words[-1]]
        
    # Reconstruct street name with corrected words
    tag_value = " ".join(words)
    
    return tag_value