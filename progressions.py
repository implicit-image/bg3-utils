#!/usr/bin/env python3


import zipfile, rarfile, os
from sys import argv
import xml.etree.ElementTree as ET
from pathlib import Path


def dict_filter(f, d)-> dict: return { k : v for k, v in d.items() if f(k, v)}

def dict_contains(d1, d2):
    count = len(d2)
    for k, v in d1.items():
        if count <= 0: return True
        if (k, v) in d2.items():
            count -= 1
    return False

    

class Progressions:


    def __init__(self, path):
        with open(path, "rb") as progressions_file:
            self.filepath = path
            self.xml_tree = ET.parse(progressions_file)
            self.xml_tree_root = self.xml_tree.getroot()
            self.progression_nodes = filter(lambda result: result.tag != "attribute" , self.xml_tree_root.iterfind(f"./region/node[@id='root']/children//"))
            self.progressionAttributes = {
                "FeatProgression" : { "id": "AllowImprovement", "type": "bool", "value": "true"},
                "NormalSpellSlot" : { "id": "Boosts", "type": "LSString", "value": "ActionResource(SpellSlot,{0},{1})"},
                "WarlockSpellSlot": { "id": "Boosts", "type": "LSString", "value": "ActionResource(WarlockSpellSlot,{0},{1})"},
                "Name"            : {"id": "Name", "type": "LSString", "value": "{0}" }
            }

    # TODO: load existing progression from game files instead of relying on predefined list
    #value="SelectSpells(f5c4af9c-5d8d-4526-9057-94a4b243cd40,1,0,,,,AlwaysPrepared);SelectPassives(a2d72748-0792-4f1e-a798-713a66d648eb,1,WarlockInvocations)"
    def __split_LSS_string(self, lss_string: str) -> list[str] | None:
        return lss_string.split(";")


    def __add_attribute_elem(self, elem, parent = None):
        parent = self.xml_tree_root if not parent else parent
        # find target node
        parent.append(elem)


    # def __comp_with_attr_data(self, attr_data: dict[str, str], element: ET.Element) -> bool:
    #     return element.attrib == attr_data

    def get_nodes_by_class(self, class_name):
        return self.xml_tree_root.iterfind(f"./region/node/children//node/attribute[@value='{class_name}']/..")

    def get_nodes_by_level(self, level):
        all_nodes = list(self.xml_tree_root.iterfind(f"./region/node/children//node"))[:100]
        nodes_by_level = []
        for node in all_nodes:
            node_level = node.find(f".//attribute[@id='Level']")
            if node_level is None:
                continue
            node_level = node_level.get('value', "-1")
            print(node_level)
            if int(node_level) == level:
                nodes_by_level.append(node)
        return nodes_by_level



    # TODO: implement removing elements
    # def __remove_attribute_elem(self, attr_data, parent = None):
    #     parent = self.xml_tree_root if not parent else parent
    #     attr = ET.Element('attribute', attr_data)
    #     parent.append(attr)


    def make_attribute_elem(self, attr_name: str) -> ET.Element:
        return ET.Element('attribute', self.progressionAttributes[attr_name])

    def write(self):
        print(f"saving to {self.filepath}...")
        self.xml_tree.write(self.filepath)

class ClassInfo:

    def __init__(self): pass


    def show_progression(self): pass


##################
path = Path("/home/b/Games/modding/bg3/progressions.lsx")
##################
# path = Path(argv[1])

if not path.exists():
    print(f"File {path.resolve()} does not exist")
    exit()

progs = Progressions(path)
# get all nodes that have feat progression
nodes = progs.get_nodes_by_level(4)
for node in nodes:
    ET.dump(node)
