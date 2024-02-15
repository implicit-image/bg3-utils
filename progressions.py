#!/usr/bin/env python3


import xml.etree.ElementTree as ET
from sys import argv
from pathlib import Path
from utils import intersperse, dict_contains, dict_filter
from ls_string import LSString


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

    def get_nodes_by_class(self, class_name: str):
        return self.xml_tree_root.iterfind(f"./region/node/children//node/attribute[@value='{class_name}']/..")


    def modify_attrib_value(self, elem: ET.Element, attr_data: dict[str, str]) -> ET.Element:
        for k, v in attr_data.items():
            elem.set(k, v)
        return elem


    # self.update(string, "ActionResource(SpellSlot,4,1)", "ActioResource(SpellSlot,8,1)")
    #

    def modify_node_attribute_value(self, node: ET.Element, attr_id: str, value: str, value_name : str, OP_FLAG="update") -> ET.Element | None:
        attr_elem = node.find(f"./attribute[@id={attr_id}]")
        if attr_elem:
            if OP_FLAG == "overwrite":
                attr_elem.set("value", value)
            elif OP_FLAG == "update":
                ls_string = LSString(attr_elem.get("value"))
                if not ls_string: return None
                ls_string[value_name] = value
                attr_elem.set("value", str(ls_string))
            return node
        return None

    def get_node_lvl(self, node: ET.Element) -> int | None:
        level = node.find(f".//attribute[@id='Level']")
        if level is None: return -1
        if level is None:
            return -1
        level = level.get("value")
        return int(level)


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

    def get_attr_elem_by_attrs(self, node: ET.Element, attr_data: dict[str, str]) -> ET.Element | None:
        for child in node:
            if dict_contains(child.attrib, attr_data):
                return child
        return None

    def get_attr_elem_by_id(self, node: ET.Element, attr_id: str) -> ET.Element | None:
        return self.get_attr_elem_by_attrs(node, { "id" : attr_id })

    def make_attribute_elem(self, attr_name: str) -> ET.Element:
        return ET.Element('attribute', self.progressionAttributes[attr_name])

    def add_spell_slots(self, classes: list[str], levels: list[int], slots: int, slot_level = -1, ):
        for char_class in classes:
            class_nodes = self.get_nodes_by_class(char_class)
            for node in class_nodes:
                if self.get_node_lvl(node) not in levels:
                    continue
                boosts = self.get_attr_elem_by_id(node, "Boosts")
                if boosts is None: continue
                ls_string = LSString(boosts.get("value"))
                classSlot = "SpellSlot"
                if char_class == "Warlock":
                    classSlot = "WarlockSpellSlot"
                slot_info = ls_string['ActionResource'][classSlot][0]
                curr_slot_level = slot_info[0]
                curr_num_of_slots = slot_info[1]
                print(curr_slot_level, curr_num_of_slots)
                ls_string['ActionResource'][classSlot][0] = [[int(curr_num_of_slots) + slots]]
                boosts.set("value", str(ls_string))

    # ActionResource(SpellSlot,2,4)
    def add_boost_to_node(self, boost, node):
        boosts_node = self.get_attr_elem_by_id(node, "Boosts")
        if boosts_node is None: return -1
        ls_string = LSString(boosts_node.get("value"))
        # if node already has this boost, return -1
        if boost in list(ls_string.expressions.keys()):
            return -1
        boost_ls_string = LSString(boost)
        ls_string.append(boost_ls_string)
        boosts_node.set("value", str(ls_string))

    def make_boost(self, boost_type: str, boost_args: list[str]):
        LSString(f"{boost_type}()")



    def test(self):
        self.add_spell_slots(["Rogue"], [1, 2, 3], 4, 4)
        nodes = []
        for node in nodes:
            boosts_el = self.get_attr_elem_by_id(node, "Boosts")
            if boosts_el is None: continue
            value = boosts_el.get("value")
            ls_string = LSString(value)
            if ls_string is None: continue
            boosts_el.set("value", str(ls_string))


    def write(self):
        print(f"saving to {self.filepath}...")
        self.xml_tree.write(self.filepath)

