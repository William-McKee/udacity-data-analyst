#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "addr:state"
"""

STATES_EXPECTED = ["PA", "NJ", "DE"]

STATES_MAPPING = { "18914": "PA",
                   "NEW JERSEY": "NJ",
                   "PA`": "PA",
                   "PHILADELPHIA": "PA"
                 }

def clean_state(in_tag_value):
    '''
    This function cleans the values within the Open Street Map state types
    in_tag_value = Open Street Map value from the state type key (e.g, "PA")
    '''
    tag_value = in_tag_value

    # Capitalize each letter
    tag_value = tag_value[:].upper()
    
    if (tag_value in STATES_EXPECTED):
        # State already standarized
        pass
    elif (tag_value in STATES_MAPPING.keys()):
        # Correct variants!
        tag_value = STATES_MAPPING[tag_value]
    
    return tag_value