import xml.etree.ElementTree as ET
from xmlprocessing import TRACK,LIB,PLAYLIST
import pandas as pd


def parse_xml_data()-> LIB:
    tree = ET.parse('xml_here/hihi.xml')
    root = tree.getroot()
    def xml_to_dict(elem):
        node = {}
        if elem.attrib:
            node["@attributes"] = elem.attrib
        children = list(elem)
        if children:
            child_dict = {}
            for child in children:
                child_data = xml_to_dict(child)
                tag = child.tag
                if tag not in child_dict:
                    child_dict[tag] = child_data if not isinstance(child_data, list) else child_data
                else:
                    if not isinstance(child_dict[tag], list):
                        child_dict[tag] = [child_dict[tag]]
                    child_dict[tag].append(child_data)
            node.update(child_dict)
        else:
            node = elem.text.strip() if elem.text else None
            if elem.attrib:
                node = {"@attributes": elem.attrib, "#text": node}

        return node

    print("Root tag:", root.tag)

    data = {root.tag: xml_to_dict(root)}
    trackdicts = [ track['@attributes'] for track in data['DJ_PLAYLISTS']['COLLECTION']['TRACK']]
    breakpoint()
    lib=LIB(tracks=[TRACK(initdict=track) for track in trackdicts])


parse_xml_data()