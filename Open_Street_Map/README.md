# Open Street Map Philadelphia

This project cleans the Open Street Map data for Philadelphia, Pennsylvania, USA.

## Open Street Map Data

Download the Open Street Map data for Philadelphia from the [Open Street Map Metro Extracts](https://mapzen.com/data/metro-extracts/).  Search for "Philadelphia" and select the first entry.  Download the OSM XML file from "Raw OpenStreetMap datasets".

## Running the code

The code was written in Python version 3.6.  I used Anaconda's Spyder IDE for development but any Python editor should suffice.

Python 3.X is located [here](https://www.python.org/downloads/) for installation.  Install the latest 3.X version.

Anaconda is [here](https://www.continuum.io/downloads).  Download Anaconda for the latest 3.X version.

Be sure all source code files and the Open Street Map OSM file are located in the same working directory.

Run the code by opening `open_street_process_map.py` and executing `process_map()`.  This function invokes all of the cleaning code.  The cleaned data is written to five CSV files - `nodes.csv`, `nodes_tags.csv`, `ways.csv`, `ways_nodes.csv`, and `ways_tags.csv`.

## Data Querying

sqlite3 is located [here](http://www.sqlite.org/download.html) for installation.

Create `open_street_map.db` file in sqlite3 using the schema provided in **data_wrangling_schema.sql**. In sqlite3, type `.mode csv` then import each table using the command `.import <file>.csv <table>` for each table in the schema.

Example: `.import nodes_tags.csv nodes_tags`

## File Contents

The "Open Street Map" Project contains the following files:

1.  **"Open_Street_Map_Cleaning.pdf"**: contains the answers to the project rubric questions.
2.  **"philadelphia_pennsylvania_sample.osm"**: contains a sample of the Philadelphia Open Street Map OSM file.
3.  **"open_street_osm_sample.py"**: This is the code sample from the Open Street Map Project Details.  This code creates the sample OSM file.
4.  **"open_street_process_map.py"**: Most of this code was taken from the "Case Study: Quiz #11" taken during the Udacity Nanodegree Course Data Wrangling section. The process_map() function reads the OSM file, iterates through the "nodes" and "ways" elements, cleans each element, adds to a dictionary, and writes the CSV output files.
5.  **"open_street_clean.py"**: This code checks the element key and cleans the element for "addr:street", "highway", "amenity", "shop", "addr:postcode", "addr:city", and "addr:state".
6.  **"open_street_clean_amenities.py"**: This code cleans elements with the key "amenity".
7.  **"open_street_clean_cities.py"**: This code cleans elements with the key "addr:city".
8.  **"open_street_clean_highways.py"**: This code cleans elements with the key "highway".
9.  **"open_street_clean_postcodes.py"**: This code cleans elements with the key "addr:postcode".
10. **"open_street_clean_shops.py"**: This code cleans elements with the key "shop".
11. **"open_street_clean_states.py"**: This code cleans elements with the key "addr:state".
12. **"open_street_clean_steeets.py"**: This code cleans elements with the key "addr:street".
13. **"Open Street Map Queries.txt"**: This file contains queries I ran on the OSM sqlite3 database.
14. **"data_wrangling_schema.sql"**: This file includes the database schema for cleaned Open Street Map database.