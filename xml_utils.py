import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def addObject(maintag,label,x1,y1,x2,y2):
    """This will create the subtree same as prescribed by Pascal VOC"""
    object=SubElement(maintag,"object")
    name=SubElement(object,'name')
    name.text=f'{label}'
    bndbox=SubElement(object,'bndbox')

    xmin=SubElement(bndbox,'xmin')
    xmin.text=f"{x1}"
    ymin=SubElement(bndbox,'ymin')
    ymin.text=f"{y1}"

    xmax=SubElement(bndbox,'xmax')
    xmax.text=f"{x2}"
    ymax=SubElement(bndbox,'ymax')
    ymax.text=f"{y2}"


    return maintag

def write_as_file(filename,tree):
    """Saves the tree as a xml file"""
    with open(f'{filename}.xml','w') as outfile:
        outfile.write(prettify(tree))
