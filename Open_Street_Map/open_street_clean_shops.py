#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code cleans the Open Street Map tag values for the tag key "shops"
"""

SHOP_TYPE_EXPECTED = \
    ["alcohol", "bakery", "beverages", "brewing_supplies", "butcher", "cheese", "chocolate", "coffee", "confectionary", 
     "convenience", "deli", "dairy", "farm", "greengrocer", "ice_cream", "pasta", "pastry", "seafood", "spices", "tea",
     "department_store", "general", "kiosk", "mall", "supermarket", "baby_goods", "bag", "boutique", "clothes", "fabric", 
     "fashion", "jewelry", "leather", "sewing", "shoes", "tailor", "watches", "charity", "second_hand", "variety_store",
     "beauty", "chemist", "cosmetics", "erotic", "hairdresser", "hairdresser_supply", "hearing_aids", "herbalist", "massage", 
     "medical_supply", "nutrition_supplements", "optician", "perfumery", "tattoo", "agarian", "bathroom_furnishing", 
     "doityourself", "electrical", "energy", "fireplace", "florist", "garden_centre", "garden_furinture", "gas", "glaziery", 
     "hardware", "houseware", "locksmith", "paint", "security", "trade", "antiques", "bed", "candles", "carpet", "curtain", 
     "furniture", "interior_decoration", "kitchen", "lamps", "tiles", "window_blind", "computer", "electronics", "hifi", 
     "mobile_phone", "radiotechnics", "vacuum_cleaner", "atv", "bicycle", "boat", "car", "car_repair", "car_parts", "fuel", 
     "fishing", "free_flying", "hunting", "jetski", "motorcycle", "outdoor", "scuba_diving", "ski", "snowmobile", "sports", 
     "swimming_pool", "tyres", "art", "collector", "craft", "frame", "games", "model", "music", "musical_instrument", 
     "photo", "camera", "trophy", "video", "video_games", "anime", "books", "gift", "lottery", "newsagent", "stationery", 
     "ticket", "bookmaker", "copyshop", "dry_cleaning", "e-cigarette", "funeral_directors", "laundry", "money_lender", 
     "party", "pawnbroker", "pet", "pyrotechnics", "religion", "tobacco", "toys", "travel_agency", "vacant", "weapons"]


SHOP_TYPE_MAPPING = { "confectionery": "confectionary",
                      "closed": "vacant",
                      "dry_cleaners": "dry_cleaning",
                      "dry_clearner": "dry_cleaning",
                      "fishmonger": "fishing",
                      "offfice_supplies": "office_supplies",
                      "pool": "swimming_pool",
                      "printing": "copyshop",
                      "variety": "variety_store"
                     }


def clean_shop(in_tag_value):
    '''
    This function cleans the values within the Open Street Map shop types
    in_tag_value = Open Street Map value from the shop type key (e.g, "convenience")
    '''
    tag_value = in_tag_value

    # Standarize the shop type
    if (tag_value in SHOP_TYPE_EXPECTED):
        # Shop type is already standarized
        pass
    elif (tag_value in SHOP_TYPE_MAPPING.keys()):
        # Last word is shop type variant
        tag_value = SHOP_TYPE_MAPPING[tag_value]
    elif (tag_value.startswith("convenience")):
        # Value like ("Convenience food")
        tag_value = "convenience"
    
    return tag_value