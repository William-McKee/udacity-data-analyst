#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Note: This code was provided by Udacity during Quiz #11 of the "Case Study"
in the "Data Wrangling" course, expect for calls to clean the data

The code reads the Open Street Map data file nodes, ways, and relations and
is transformed into a dictionary of dictionary.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files


We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the
cerberus library we can validate the output against this schema to ensure it is correct.

### If the element top level tag is "node":

The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset

All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:

- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
          'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
          'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":

The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
- user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

import csv
import codecs
import re
import xml.etree.cElementTree as ET

from open_street_clean import clean_tags

# Regular expressions
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_node(element, node_attr_fields=NODE_FIELDS, problem_chars=PROBLEMCHARS,
               default_tag_type ='regular'):
    """
    Clean and shape node elements
        element = OSM XML element
        node_attr_fields = list of expected node attributes
        problem_chars = regular expression for keys we should ignore
        default_tag_type = indicate the type for a default key
    """
    node_attribs = {}
    node_tags = []
   
    # Save attributes
    for field in node_attr_fields:
        node_attribs[field] = element.attrib[field]

    # Go through the element and save tags
    for node in element:
        # Clean the tags for this node
        cleaned_tag_key, cleaned_tag_value = clean_tags(node.attrib['k'], node.attrib['v'])
    
        if PROBLEMCHARS.match(cleaned_tag_key):
            continue

        tag_dict = {}
        tag_dict['id'] = element.attrib['id']
        tag_dict['value'] = cleaned_tag_value

        # Keys could contain a key and type
        if ':' in node.attrib['k']:
            tag_dict['key'] = cleaned_tag_key.split(':', 1)[-1]
            tag_dict['type'] = cleaned_tag_key.split(':', 1)[0]
        else:
            tag_dict['key'] = cleaned_tag_key
            tag_dict['type'] = default_tag_type
        node_tags.append(tag_dict)

    return {'node': node_attribs, 'node_tags': node_tags}


def shape_way(element, way_attr_fields=WAY_FIELDS, problem_chars=PROBLEMCHARS,
              default_tag_type='regular'):
    """
    Clean and shape way elements
        element = OSM XML element
        way_attr_fields = list of expected way attributes
        problem_chars = regular expression for keys we should ignore
        default_tag_type = indicate the type for a default key
    """
    way_attribs = {}
    way_nodes = []
    way_tags = []

    # Save attributes    
    for field in way_attr_fields:
        way_attribs[field] = element.attrib[field]

    # Go through the element and save tags
    n = 0
    for node in element:      
        # node links
        if node.tag == "nd":
            way_node = {}
            way_node['id'] = element.attrib['id']
            way_node['node_id'] = node.attrib['ref']
            way_node['position'] = n
            way_nodes.append(way_node)
            n += 1
        # tags
        elif node.tag == "tag":
            # Clean the tags for this node
            cleaned_tag_key, cleaned_tag_value = clean_tags(node.attrib['k'], node.attrib['v'])
        
            if PROBLEMCHARS.match(cleaned_tag_key):
                continue

            tag_dict = {}
            tag_dict['id'] = element.attrib['id']
            tag_dict['value'] = cleaned_tag_value

            if ':' in node.attrib['k']:
                tag_dict['key'] = cleaned_tag_key.split(':', 1)[-1]
                tag_dict['type'] = cleaned_tag_key.split(':', 1)[0]
            else:
                tag_dict['key'] = cleaned_tag_key
                tag_dict['type'] = default_tag_type
            way_tags.append(tag_dict)    
    
    return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': way_tags}


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):

    """Clean and shape node or way XML element to Python dict"""
    return_dict = {}

    # Process nodes
    if element.tag == 'node':
        return_dict = shape_node(element)
    # Process way
    elif element.tag == 'way':
        return_dict = shape_way(element)

    return return_dict

# ================================================== #

#               Helper Functions                     #

# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """
    Yield element if it is the right type of tag
        osm_file = path to the OSM XML file
        tags = list of tags whose elements this shall yield
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            #k:str(v).encode('utf-8') for k, v in row.items()
            k:v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# ================================================== #

#               Main Function                        #

# ================================================== #

def process_map(file_in, nodes_path, nodes_tags_path, ways_path, way_nodes_path, way_tags_path):
    """
    Iteratively process each XML element and write to csv(s)
        file_in = XML OSM File
    """
    
    # Operate on all output files (use codecs.open or regular open?)
    with codecs.open(nodes_path, 'w', encoding='utf-8') as nodes_file, \
         codecs.open(nodes_tags_path, 'w', encoding='utf-8') as nodes_tags_file, \
         codecs.open(ways_path, 'w', encoding='utf-8') as ways_file, \
         codecs.open(way_nodes_path, 'w', encoding='utf-8') as way_nodes_file, \
         codecs.open(way_tags_path, 'w', encoding='utf-8') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS, lineterminator = '\n')
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS, lineterminator = '\n')
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS, lineterminator = '\n')
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS, lineterminator = '\n')
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS, lineterminator = '\n')
        
        # nodes_writer.writeheader() Skip headers due to sqlite3 insertion error on primary key
        node_tags_writer.writeheader()
        # ways_writer.writeheader() Skip headers due to sqlite3 insertion error on primary key
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        # Loop through the node and way elements
        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    
    # CSV Sample Output File Names
    NODES_PATH_SAMPLE = "nodes_sample.csv"
    NODES_TAGS_PATH_SAMPLE = "nodes_tags_sample.csv"
    WAYS_PATH_SAMPLE = "ways_sample.csv"
    WAY_NODES_PATH_SAMPLE = "ways_nodes_sample.csv"
    WAY_TAGS_PATH_SAMPLE = "ways_tags_sample.csv"

    # Process sample data set
    process_map('philadelphia_pennsylvania_sample.osm',
                NODES_PATH_SAMPLE, NODES_TAGS_PATH_SAMPLE,
                WAYS_PATH_SAMPLE, WAY_NODES_PATH_SAMPLE, WAY_TAGS_PATH_SAMPLE)
    
    # CSV Full Output File Names
    NODES_PATH_FULL = "nodes.csv"
    NODES_TAGS_PATH_FULL = "nodes_tags.csv"
    WAYS_PATH_FULL = "ways.csv"
    WAY_NODES_PATH_FULL = "ways_nodes.csv"
    WAY_TAGS_PATH_FULL = "ways_tags.csv"
    
    # Process full data set
    process_map('philadelphia_pennsylvania.osm',
                 NODES_PATH_FULL, NODES_TAGS_PATH_FULL,
                 WAYS_PATH_FULL, WAY_NODES_PATH_FULL, WAY_TAGS_PATH_FULL)