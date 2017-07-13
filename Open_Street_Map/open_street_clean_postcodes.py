#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "addr:postcode"
"""

POSTCODE_STARTS = ["08", "18", "19"]

def clean_postcode(in_tag_value):
    '''
    This function cleans the values within the Open Street Map postcode types
    in_tag_value = Open Street Map value from the postcode type key (e.g, "19104")
    '''
    tag_value = in_tag_value

    # Standarize the postcode type
    start_digits = in_tag_value[:2]
    if (start_digits in POSTCODE_STARTS):
        if (len(in_tag_value) == 5):
            # Five digit zip code ("19104")
            pass
        elif (len(in_tag_value) > 5 and in_tag_value[5] == '-'):
            # Zip code plus 4; we only need first five digits ("19154-3907")
            tag_value = tag_value[:5]
        # else: how to clean typo like "080033"?  Is it "08003" or "08033"?
    else:
        # Value like ("Philadelphia, PA 19146")
        parts = tag_value.split()
        for part in parts:
            start_digits = part[:2]
            if (start_digits in POSTCODE_STARTS):
                tag_value = part
                break
    
    return tag_value