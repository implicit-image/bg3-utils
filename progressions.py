#!/usr/bin/env python3


import xml.etree.ElementTree as ET
from sys import argv
from pathlib import Path
from utils import intersperse, dict_contains, dict_filter


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

    def get_nodes_by_class(self, class_name):
        return self.xml_tree_root.iterfind(f"./region/node/children//node/attribute[@value='{class_name}']/..")


    def modify_attrib_value(self, elem: ET.Element, attr_data: dict[str, str]) -> ET.Element:
        for k, v in attr_data.items():
            elem.set(k, v)
        return elem


    # self.update(string, "ActionResource(SpellSlot,4,1)", "ActioResource(SpellSlot,8,1)")
    #

    def modify_node_attribute_value(self, node: ET.Element, attr_id: str, value: str, OP_FLAG="update") -> ET.Element | None:
        attr_elem = node.find(f"./attribute[@id={attr_id}]")
        if attr_elem:
            if OP_FLAG == "overwrite":
                attr_elem.set("value", value)
            elif OP_FLAG == "update":
                lss_string = attr_elem.get("value")
                updated_lss_string = self.update_lss_string(lss_string, value_name, value)
            attr_elem.set("value", updated_lss_string)
            return node
        return None


    def get_nodes_by_level(self, level):
        level_nodes = list(self.xml_tree_root.iterfind(f"./region/node/children//node/attribute[@id='Level']/.."))
        nodes_by_level = []
        for node in level_nodes:
            node_level = node.find(f".//attribute[@id='Level']")
            if node_level is None:
                continue
            node_level = node_level.get('value', "-1")
            if int(node_level) == level:
                nodes_by_level.append(node)
        return nodes_by_level

    def get_attr_elem(self, node: ET.Element, attr_data: dict[str, str]) -> ET.Element | None:
        for child in node:
            if dict_contains(child.attrib, attr_data):
                return child
        return None

    def make_attribute_elem(self, attr_name: str) -> ET.Element:
        return ET.Element('attribute', self.progressionAttributes[attr_name])

    def add_spell_slots(self, classes: list[str], level: int, slot_level: int, slots: int):
        cls = {}
        for char_class in classes:
            cls[char_class] = []


    
    def test(self):
        bard_node = list(self.get_nodes_by_class('Bard'))[0]
        lss_string = self.get_attr_elem(bard_node, { "id" : "Boosts" })
        lss_string = lss_string.get('value')
        if not lss_string: return 0
        lss_string = self.update_lss_string(lss_string, "ActionResource(SpellSlot,4,1)", "ActionResource(SpellSlot,8,1)")


    def write(self):
        print(f"saving to {self.filepath}...")
        self.xml_tree.write(self.filepath)

