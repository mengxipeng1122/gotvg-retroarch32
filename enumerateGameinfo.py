#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import argparse
import os

import xml.etree.ElementTree as ET


def runCmd(cmd, showCmd =True, mustOk=False, showResult=False):
  '''
run a shell command  on PC
and return the output result
parameter:
  cmd --- the command line
  showCmd -- whether show running command
  mustOk -- if this option is True and command run failed, then raise a exception
  showResult -- show result of command
  '''
  if showCmd:
    print (cmd)
  ## run it ''
  result = ""
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  ## But do not wait till netstat finish, start displaying output immediately ##
  while True:
    try:
        output = p.stdout.readline().decode()
    except UnicodeDecodeError as e:
        print(' UnicodeDecodeError ', e);
    if output == '' and p.poll() is not None:
      break
    if output:
      result+=str(output)
      if showResult:
        print(output.strip())
        sys.stdout.flush()
  stderr = p.communicate()[0]
  if stderr:
    print (f'STDERR:{stderr}')
  p_status = p.wait()
  if mustOk:
    if p_status is p_status !=0: raise Exception('run %s failed %d' %(cmd, p_status))
  return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--rom-dir', help="path to roms", default='/sdcard/roms/')
    parser.add_argument("-i", '--input-xml', help="path to input xml file ", default='./../com.gotvg.mobileplatform.v.1.17/assets/gameconfig/OnEntireListAck.xml')
    parser.add_argument("-t", '--tmp-file', help="path to temp playlist file", default='/tmp/gotvg.cn.lpl')
    args = parser.parse_args()
    rom_dir = args.rom_dir;
    input_xml = args.input_xml;
    dfn = args.tmp_file
    
    # Parse the XML file
    tree = ET.parse(input_xml)
    # Get the root element
    root = tree.getroot()
    

    info = {
        "version": "1.5",
        "default_core_path": "/data/user/0/com.retroarch.ra32/cores/gotvg_libretro_android.so",
        "default_core_name": "gotvg",
        "label_display_mode": 0,
        "right_thumbnail_mode": 0,
        "left_thumbnail_mode": 0,
        "sort_mode": 0,
        "items": [ ],
    }

    for machine in root.iter('machine'):
        for game in machine.iter('game'):
            for server in game.iter('server'):
                for version in server.iter('version'):
                    rom1 = version.attrib['rom1']
                    rom2 = version.attrib['rom2']
                    rom = rom2 if rom2!=None and rom2 != '0' else rom1
                    rompath = os.path.join(rom_dir, f'{rom}.zip')
                    info['items'] .append(
                    {
                        'path' : rompath, 
                        'label' : f"{game.attrib['title']}-{version.attrib['title']}",
                    },)
    json.dump(info, open(dfn, 'w'), indent=2)

    cmd = f'adb push {dfn} /sdcard/RetroArch/playlists'
    runCmd(cmd)


    

if __name__ == '__main__':
    main()

