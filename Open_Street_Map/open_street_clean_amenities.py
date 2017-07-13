#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "amenities"
"""

AMENITY_TYPE_EXPECTED = \
    ["bar", "bbq", "biergarten", "cafe", "drinking_water", "fast_food", "food_court", "ice_cream", "pub", "restaurant", 
     "college", "kindergarten", "library", "public_bookcase", "school", "music_school", "driving_school", "language_school",
     "university", "bicycle_parking", "bicycle_repair_station", "bicycle_rental", "boat_rental", "boat_sharing", "bus_station", 
     "car_rental", "car_sharing", "car_wash", "charging_station", "ferry_terminal", "fuel", "grit_bin", "motorcycle_parking", 
     "parking", "parking_entrance", "parking_space", "taxi", "atm", "bank", "bureau_de_change", "baby_hatch", "clinic", "dentist", 
     "hospital", "nursing_home", "pharmacy", "social_facility", "veterinary", "blood_donation", "arts_centre", "brothel", 
     "casino", "cinema", "community_centre", "fountain", "gambling", "nightclub", "planetarium", "social_centre", "stripclub", 
     "studio", "swingerclub", "theatre", "animal_boarding", "animal_shelter", "baking_oven", "bench", "clock", "courthouse", 
     "coworking_space", "creamtorium", "crypt", "dive_center", "dojo", "embassy", "fire_station", "game_feeding", "grave_yard", 
     "hunting_stand", "internet_cafe", "kneipp_water_cure", "marketplace", "photo_booth", "place_of_worship", "police", 
     "post_box", "post_office", "prison", "ranger_station", "recycling", "rescue_station", "sanitary_dump_station", "shelter", 
     "shower", "table", "telephone", "toilets", "townhall", "vending_machine", "waste_basket", "waste_disposal", 
     "waste_transfer_station", "watering_place", "water_point"]


AMENITY_TYPE_MAPPING = { "childcare": "kindergarten",
                         "preschool": "kindergarten",
                         "fraternity": "dormitory",
                         "Bank Branch": "bank",
                         "animal_animal_boarding": "animal_boarding",
                         "crematorium": "creamtorium"
                       }

AMENITY_KEYS_CHANGEOVER = {"swimming_pool": "leisure:swimming_area", 
                           "public_building": "office:government", 
                           "gym": "leisure:fitness_centre"}


def clean_amenity(in_tag_key, in_tag_value):
    '''
    This function cleans the keys and values within the Open Street Map amenities types
    in_tag_value = Open Street Map value from the amenity type key (e.g, "university")
    '''
    tag_key = in_tag_key
    tag_value = in_tag_value

    # Standarize the amenity type
    if (tag_value in AMENITY_TYPE_EXPECTED):
        # Amenity type is already standarized
        pass
    elif (tag_value in AMENITY_TYPE_MAPPING.keys()):
        # Last word is amenity type variant
        tag_value = AMENITY_TYPE_MAPPING[tag_value]
    elif (tag_value in AMENITY_KEYS_CHANGEOVER.keys()):
        # Replace key:value pair
        value_parts = AMENITY_KEYS_CHANGEOVER[tag_value].split(":")
        tag_key = value_parts[0]
        tag_value = value_parts[1]
    
    return tag_key, tag_value