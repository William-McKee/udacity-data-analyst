#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "highways"
"""

HIGHWAY_TYPE_EXPECTED = \
    ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "service", "motorway_link", 
     "trunk_link", "primary_link", "secondary_link", "tertiary_link", "living_street", "pedestrian", "track", "bus_guideway", 
     "escape", "raceway", "road", "footway", "bridleway", "steps", "path", "cycleway", "proposed", "construction", "bus_stop", 
     "crossing", "elevator", "emergency_access_point", "give_way", "mini_roundabout", "motorway_junction", "passing_place", 
     "rest_area", "speed_camera", "street_lamp", "services", "stop", "traffic_signals", "turning_circle"]


HIGHWAY_TYPE_MAPPING = { "turning_loop": "turning_circle",
                         "yield": "give_way"
                       }


def clean_highway(in_tag_value):
    '''
    This function cleans the values within the Open Street Map highway types
    in_tag_value = Open Street Map value from the highway type key (e.g, "turning_circle")
    '''
    tag_value = in_tag_value

    # Standarize the highway type
    if (tag_value in HIGHWAY_TYPE_EXPECTED):
        # Highway type is already standarized
        pass
    elif (tag_value in HIGHWAY_TYPE_MAPPING.keys()):
        # Last word is highway type variant
        tag_value = HIGHWAY_TYPE_MAPPING[tag_value]
    
    return tag_value