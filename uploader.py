#!/usr/bin/env python3
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

import argparse
import os
import re
import serial
import sys
import time
import traceback
import binascii



class MTKModem(object):

    WRITE_SIZE = 400

    def __init__(self, port):
        self.open(port)

    def open(self, port):
        self.ser = serial.Serial(port, 115200, timeout=5, dsrdtr=True, rtscts=True)
        
        

    def SendCommand(self, command, getline=True, ignoreError=False):
        print ('send: %s' % (command))
        self.ser.write((command + '\r').encode())
        data = ''
        if getline:
            data = self.ReadLine(ignoreError)
        return data 

    def SendCommandResult(self, command,ignoreError=False):
        out = []    
        print ('send: %s' % (command))
        self.ser.write((command + '\r').encode())
        while 1:
            data = self.ser.readline().decode().rstrip("\n\r")
            if data == 'OK':
                return out
                break
            if data == 'ERROR':
                if ignoreError:
                    return out
                raise Exception('Comm Error')
            if data != '':
                out.append(data)    
            

    def ReadLine(self, ignoreError):
        while 1:
            data = self.ser.readline().decode().rstrip("\n\r")
            if data == 'OK':
                break
            if data == 'ERROR':
                if ignoreError:
                    break
                raise Exception('Comm Error')
                
            if data != '':
                print (data)

    def ListFiles(self, path):
        
        filenamePath = binascii.hexlify(path.encode("utf-16-be")).decode()
        fileList = self.SendCommandResult('AT+EFSL="' + filenamePath + '"',True)
        print ("List path: %s" % path)
        for item in fileList:
            diritem = item.split(",")
            # get file size
            filesize = diritem[1]
            # attribute of file
            attrib = diritem[2]
            quoted = re.compile('"[^"]*"')
            for value in quoted.findall(item):
                # find filename
                value = value.replace('"', "")               
                myname = binascii.unhexlify(value)
                print("{0:30s} {1:10s} {2:5s}".format( myname.decode('utf-16-be'),filesize,attrib))
        print("")
            

    def DeleteFile(self, pathFilename):
        # Folder operation Back to root folder
        print ("Delete File {0:s}".format(pathFilename))
        self.SendCommand('AT+EFSF=3')
        
        folder = binascii.hexlify(pathFilename.encode("utf-16-be")).decode()
        # send command ignore error if file does not exits
        
        self.SendCommand('AT+EFSD="' + folder + '"', True, True)
    
    def createFolder(self,folderName):
        
        print ("Create folder: %s" % folderName)
        self.SendCommand('AT+EFSF=3')
        #ignore error
        folder = binascii.hexlify(folderName.encode("utf-16-be")).decode()
        self.SendCommand('AT+EFSF=0,"'+ folder +'"',True,True)    
    

    def sendFile(self, destpath,filename):
        if not os.path.isfile(filename):
            raise Exception('Can not open file: %s') % (filename)
        
        # open file        
        f = open(filename, 'rb')
        st = os.stat(filename)
        
        size = st.st_size
        print ('Bytes to send %d' % (size))
        if size == 0:
            raise Exception('File is empty')
        
        path = destpath + filename
       
        filenamePath = binascii.hexlify(path.encode("utf-16-be")).decode()
        print ('Filename Path %s' % path)

        # open file for write
        self.SendCommand('AT+EFSW=0,"' + filenamePath + '"')
               
        # send data to open file
        for i in range(st.st_size // self.WRITE_SIZE):
            var = f.read(self.WRITE_SIZE)
            data = binascii.hexlify(var).decode()
            #data = var.encode("hex")
            if size == 400:
                # last paket send eof
                 self.SendCommand('AT+EFSW=2,1,400,"' + data + '"')
            else:
                # send paket
                self.SendCommand('AT+EFSW=2,0,400,"' + data + '"')
            size = size - 400
    
        if size > 0:
            # send last data to open file
            var = f.read(size)
            data = binascii.hexlify(var).decode()
            #data = var.encode("hex")
            # send lastpaket
            self.SendCommand('AT+EFSW=2,1,' + str(size) + ',"' + data + '"')
    
        # close file
        self.SendCommand('AT+EFSW=1,"' + filenamePath + '"') 



    def flushCom(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        
    def close(self):
        self.ser.close()


def main():


    parser = argparse.ArgumentParser(description='Push Application Utility', prog='uploader')

    parser.add_argument('--port', '-p', help='Serial port device', default='/dev/ttyACM0')
    # parser.add_argument('uploadfile', type=argparse.FileType('rb'), help='File for uploading')

    args = parser.parse_args()
    if os.path.isfile('main.vxp') == False:
        print ('Can not open main.vxp')
        return
    args = parser.parse_args()
    if os.path.isfile('autostart.txt') == False:
        print ('Can not open autostart.txt')
        return
    
    h = MTKModem(args.port)
    time.sleep(0.5)
    
    h.SendCommand("AT")
       
    # exit all running process
    h.SendCommand("AT+[666]EXIT_ALL", False)
    time.sleep(2)
    h.flushCom()
     
    # Change operation mode to obtain access to filesystem    
    h.SendCommand("AT+ESUO=3")
        
    # AT+EFSR FileRead
    # h.SendCommand('AT+EFSR\r')

    # File System Size  67 = C:\
    # h.SendCommand('AT+EFS=67\r)

    # Folder operation Back to root folder
    h.SendCommand("AT+EFSF=3")
    
    h.createFolder("C:\MRE")
    
    h.DeleteFile("D:\autostart.txt")
    h.DeleteFile("C:\autostart.txt")

    h.DeleteFile("C:\MRE\main.vxp")
    
    h.sendFile("C:\MRE\\","main.vxp")
    h.sendFile("C:\\","autostart.txt")

    h.ListFiles("C:\MRE")
    #h.ListFiles("D:\MRE")
    # C: can also mount as disk ( power off the device )
    h.ListFiles("C:")
    # D: is a hidden volume
    h.ListFiles("D:")
            
    # Change operation mode to compatible
    h.SendCommand("AT+ESUO=4")

    h.SendCommand("AT+[666]REBOOT", False) 
    
    h.close()
    
  


if __name__ == '__main__':
    try:
        main()
       
    except Exception:
        
        traceback.print_exc()

