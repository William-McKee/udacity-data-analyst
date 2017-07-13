"""
Udacity "Open Street Map" Project Details code sample reduces file size.
This function creates the sample file by taking every k-th element and
writing those elements only to the sample file.
"""

import xml.etree.cElementTree as ET

def get_element(osm_file, tags=('node', 'way', 'relation')):
    '''
    Yield element if it is the right kind of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    '''
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def create_sample_file(osm_file, sample_osm_file, k):
    '''
    Create sample file
    osm_file: Full OSM file
    osm_sample_file: Sample OSM file containing the output
    k: Copy every k-th element to the sample OSM file
    '''
    
    # Convert lines to bytes
    START_LINE_STRING = '<?xml version="1.0" encoding="UTF-8"?>\n'
    START_LINE_BYTES = START_LINE_STRING.encode('utf-8')
    OSM_START_TAG_STRING = '<osm>\n  '
    OSM_START_TAG_BYTES = OSM_START_TAG_STRING.encode('utf-8')
    OSM_END_TAG_STRING = '</osm>'
    OSM_END_TAG_BYTES = OSM_END_TAG_STRING.encode('utf-8')

    # Loop through file
    with open(sample_osm_file, 'wb') as output:
        output.write(START_LINE_BYTES)
        output.write(OSM_START_TAG_BYTES)

        # Write every kth top level element
        for i, element in enumerate(get_element(osm_file)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write(OSM_END_TAG_BYTES)
        
if __name__ == '__main__':
    create_sample_file('philadelphia_pennsylvania.osm', 'philadelphia_pennsylvania_sample.osm', 100)