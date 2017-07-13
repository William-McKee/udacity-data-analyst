Open Street Map Project README
==============================

William McKee
July 2017

The "Open Street Map" Project contains the following files:

(1)  "Open_Street_Map_Cleaning.pdf" contains the answers to the project rubric questions.
(2)  "philadelphia_pennsylvania_sample.osm" contains a sample of the Philadelphia Open Street Map OSM file.
(3)  "open_street_osm_sample.py": This is the code sample from the Open Street Map Project Details.  This code creates the sample OSM file.
(4)  "open_street_process_map.py": Most of this code was taken from the "Case Study: Quiz #11".  The process_map() function reads the OSM 
                                   file, iterates through the "nodes" and "ways" elements, cleans each element, adds to a dictionary, and
                                   writes the CSV output files.
(5)  "open_street_clean.py": This code checks the element key and cleans the element for "addr:street", "highway", "amenity", "shop",
                             "addr:postcode", "addr:city", and "addr:state".
(6)  "open_street_clean_amenities.py": This code cleans elements with the key "amenity".
(7)  "open_street_clean_cities.py": This code cleans elements with the key "addr:city".
(8)  "open_street_clean_highways.py": This code cleans elements with the key "highway".
(9)  "open_street_clean_postcodes.py": This code cleans elements with the key "addr:postcode".
(10) "open_street_clean_shops.py": This code cleans elements with the key "shop".
(11) "open_street_clean_states.py": This code cleans elements with the key "addr:state".
(12) "open_street_clean_steeets.py": This code cleans elements with the key "addr:street".
(13) "Open Street Map Queries.txt": This file contains queries I ran on the OSM sqlite3 database.

Please note that the code was written in Python 3.6.  I used Anaconda's Spyder IDE for development.

One can perform all tasks by opening open_street_process_map.py file and running the code (process_map()).

The only resource used for this project was code from the Udacity lessons, indicated in the Python source code files.

I created open_street_map.db file in sqlite3 using the schema provided in the Open Street Map Project Details. I imported the CSV files
using the commands from the course (.mode csv; .import <file>.csv <table>).