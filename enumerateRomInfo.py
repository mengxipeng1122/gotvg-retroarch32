#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import xml.etree.ElementTree as ET

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input-file', help="path to input xml file ", default='./../bins/com.gotvg.mobileplatform.v.1.17/assets/gameconfig/rom_md5.xml')
    parser.add_argument("-o", '--output-json', help="path to output json file ", default='/tmp/roms.list.json')

    args = parser.parse_args()

    input_file = args.input_file
    output_json = args.output_json

    tree = ET.parse(input_file)
    root = tree.getroot()
    info =  []
    for item in root.iter('item'):
        rom_name =  item.attrib['name']
        rom_value = item.attrib['value']
        rom = rom_name[:-4] if rom_name.endswith('.zip') else rom_name
        info.append({
            'name' : item.attrib['name'],   
            'url' : f"http://download.gotvg.cn/roms2/{rom}_{rom_value}.zip",
        })
        print(item)
    json.dump(info, open(output_json, 'w'), indent=2)
        
    


if __name__ == '__main__':
    main()

