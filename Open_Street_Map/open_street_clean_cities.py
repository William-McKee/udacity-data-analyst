#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "addr:city"
"""

TOWNSHIP_VARIANTS = ["Twp", "twp"]

def clean_city(in_tag_value):
    '''
    This function cleans the values within the Open Street Map city types
    in_tag_value = Open Street Map value from the city type key (e.g, "Philadelphia")
    '''
    tag_value = in_tag_value

    # Capitalize each word
    words = [word[0].upper() + word[1:] for word in tag_value.split()]
    tag_value = " ".join(words)
    
    if (tag_value.startswith("Phi")):
        # Correct variants of "Philadelphia"
        tag_value = "Philadelphia"
    else:
        # Correct all variants of "Township"
        words = tag_value.split()
        if (len(words) > 1):
            new_words = []
            for word in words:
                if word in TOWNSHIP_VARIANTS:
                    new_words.append("Township")
                else:
                    new_words.append(word)
                
            # Reconstruct
            tag_value = " ".join(new_words)
    
    return tag_value