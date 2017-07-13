#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the following tags:
addr:street, highway, amenity, shop, addr:postcode, addr:city, addr:state
"""

"""
I used the following code in order to audit all types other than street types.
After auditing the code for unexpected types, I came up with cleaning rules which
are implemented in the open_street_clean_<field> py files.

KEY_TYPE = '<key_type>'

EXPECTED = ['<List of expected values from Map_Features page in Open Street Wiki>']\

def audit_type(types, key, value):
    types = list containing values not in expected list
    key = current element tag "k" field
    value = current element tag "v" field
    
    # Check the key type
    if key == KEY_TYPE:
        # Add unexpected values
        if value not in EXPECTED:
            types.add(value)
"""

import xml.etree.cElementTree as ET

from open_street_clean_streets import clean_street
from open_street_clean_highways import clean_highway
from open_street_clean_amenities import clean_amenity
from open_street_clean_shops import clean_shop
from open_street_clean_postcodes import clean_postcode
from open_street_clean_cities import clean_city
from open_street_clean_states import clean_state

# Tags to be cleaned
TAGS_TO_CLEAN = ["addr:street", "highway", "amenity", "shop", "addr:postcode", "addr:city", "addr:state"]

       
def clean_tags(in_tag_key, in_tag_value):
    '''
    This function cleans Open Street Map data for various tags
    in_tag_key = Open Street Map <tag k='...'> key (e.g. "addr:street")
    in_tag_value = Open Street Map <tag v='...'> value (e.g. "Front Street")
    Returns updated tag key and tag value
    
    '''
    tag_key = in_tag_key
    tag_value = in_tag_value
    if (in_tag_key == TAGS_TO_CLEAN[0]):
        tag_value = clean_street(in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[1]):
        tag_value = clean_highway(in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[2]):
        tag_key, tag_value = clean_amenity(in_tag_key, in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[3]):
        tag_value = clean_shop(in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[4]):
        tag_value = clean_postcode(in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[5]):
        tag_value = clean_city(in_tag_value)
    elif (in_tag_key == TAGS_TO_CLEAN[6]):
        tag_value = clean_state(in_tag_value)
    return tag_key, tag_value
           
     
def clean_elements(osm_file_name):
    '''
    This function cleans the elements from the Open Street Map data set in the specified file
    osm_file_name = path to the OSM data file
    '''
    
    # OSM File open
    osm_file = open(osm_file_name, "r", encoding="utf-8")

    # Comment out auditing code
    #our_types = set()
    
    # Loop through OSM file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Process nodes and ways
        if elem.tag == "node" or elem.tag == "way":
            # Process tags
            for tag in elem.iter("tag"):
                # Check tag type
                tag_key = tag.attrib['k']
                tag_value = tag.attrib['v']
                #audit_type(our_types, tag_key, tag_value) Comment out auditing code
                new_tag_key, new_tag_value = clean_tags(tag_key, tag_value)

    # Comment out auditing code
    #print(our_types)
    
    osm_file.close()

if __name__ == '__main__':
    #clean_elements('philadelphia_pennsylvania_sample.osm')
    clean_elements('philadelphia_pennsylvania.osm')