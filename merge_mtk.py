#!/usr/bin/env python
#
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


import struct
import argparse
import os
import sys
import traceback

    

def main():
    parser = argparse.ArgumentParser(description = 'MTK merge utility', prog = 'mtktool')
    parser.add_argument('ifile', type=argparse.FileType('rb'), help='ELF File')
    parser.add_argument('bfile', type=argparse.FileType('rb'), help='mtk header')
    parser.add_argument('ofile', type=argparse.FileType('wrb'), help='vxp File')
    
    
    #print parser.parse_args()

    args = parser.parse_args()

	#seek to end
    args.ifile.seek(0,2)
	#get size of user binary file to merge
    bsize = args.ifile.tell()
    print 'Size of the ELF File:    %d' % bsize
	#seek to start
    args.ifile.seek(0,0)

    args.bfile.seek(0,2)
	#get size of user binary file to merge
    bsizeHeader = args.bfile.tell()
    print 'Size of the Header File: %d' %  bsizeHeader 
    args.bfile.seek(0,0)

    #write output file
    data = args.ifile.read(bsize)
    data += args.bfile.read(bsizeHeader)

    args.ofile.write(data)

    args.ifile.close()
    args.bfile.close()
    args.ofile.flush()

    elf_length = struct.pack('<L',bsize)

    args.ofile.seek(-12,2)

    print 'Write Header size'

    args.ofile.write(elf_length)
    args.ofile.close()


  
    print 'Done'

if __name__ == '__main__':
    try:
        main()
       
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        traceback.print_exc()
       
        
