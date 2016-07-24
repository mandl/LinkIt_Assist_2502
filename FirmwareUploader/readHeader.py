#!/usr/bin/env python3
#
# Pares the MTK fileinfo header
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.



import argparse
import os
import struct
import sys
from time import sleep
import time
import traceback


def parseHeader(f):
    
    
    # 'MMM', highest byte - version 
    magic_ver, = struct.unpack('<I', f.read(4)) 
  
    if (magic_ver & 0x00FFFFFF) != 0x004D4D4D:
        raise Exception('Did not found magic 4D4D4D')
    print ('magic_ver 0x%x' % magic_ver)
    
    # Total header size, incl. struct gfh_header 
    size, = struct.unpack('<H', f.read(2))
    print ('header_size 0x%x' % size)
    header_type, = struct.unpack('<H', f.read(2))
    print ('header_type 0x%x' % header_type)
    
    print ('FILE_INFO')
    
    # /* 0 - gfh_file_info */
     # "FILE_INFO", zero-padded 
    f.read(12)
    
    file_ver, = struct.unpack('<I', f.read(4)) 
    print ('file_ver 0x%x' % file_ver)
    file_type, = struct.unpack('<H', f.read(2))
    print ('file_type 0x%x' % file_type)
    flash_dev, = struct.unpack('B', f.read(1))
    print ('flash_dev 0x%x' % flash_dev)
    sig_type = struct.unpack('B', f.read(1))
    print ('sig_type 0x%x' % sig_type )
    load_addr, = struct.unpack('<I', f.read(4)) 
    print ('load_addr 0x%x' % load_addr)
    file_len, = struct.unpack('<I', f.read(4))
    print ('file_len 0x%x' % file_len)
    max_size, = struct.unpack('<I', f.read(4)) 
    print ('max_size 0x%x' % max_size)
    content_offset = struct.unpack('<I', f.read(4))
    print ('content_offset 0x%x' % content_offset)
    sig_len, = struct.unpack('<I', f.read(4)) 
    print ('sig_len 0x%x' % sig_len)
    sig_type, = struct.unpack('<I', f.read(4)) 
    print ('sig_type 0x%x' % sig_type)
    attr, = struct.unpack('<I', f.read(4))
    print ('attr 0x%x' % attr) 
    print ('')
    
    

def main():
    
    
     # This is the Bootloader
     
    Folder =  "W15.19.p2-uart/"
    FilenameBootloader = Folder + "SEEED02A_DEMO_BOOTLOADER_V005_MT2502_MAUI_11CW1418SP5_W15_19.bin"
    FilenameBootloaderExt = Folder + "EXT_BOOTLOADER"
    
    # this is the Firmware
    FilenameROM1 = Folder + "ROM"
    FilenameROM2 = Folder + "VIVA"
    
   
    f = open(FilenameBootloader, 'rb')
  
    f2 = open(FilenameBootloaderExt, 'rb')
   
    f3 = open(FilenameROM1, 'rb')
  
    f4 = open(FilenameROM2, 'rb')
   
    
    
    print ( FilenameBootloader)
    parseHeader(f)
    print (FilenameBootloaderExt)
    parseHeader(f2)
    print (FilenameROM1)
    parseHeader(f3)
    print (FilenameROM2)
    parseHeader(f4)
    
  
    
if __name__ == '__main__':
    try:
        main()
       
    except Exception:
        #sys.stderr.write('ERROR: %s\n' % str(err))
        traceback.print_exc()
