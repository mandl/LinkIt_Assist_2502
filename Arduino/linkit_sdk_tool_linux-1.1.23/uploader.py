#!/usr/bin/env python3
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


import time
import sys
import re
import argparse
import traceback
import os
import logging
import serial
import binascii
import logging

class MTKModem(object):

    WRITE_SIZE = 400

    def __init__(self, port):
        self.open(port)

    def open(self, port):
        self.ser = serial.Serial(port, 115200, timeout=5, dsrdtr=True, rtscts=True)
        
        

    def SendCommand(self, command, getline=True, ignoreError=False):
        logging.debug ('send: ' +command)
        self.ser.write((command + '\r').encode())
        data = ''
        if getline:
            data = self.ReadLine(ignoreError)
        return data 

    def SendCommandResult(self, command,ignoreError=False):
        out = []    
        logging.debug('send: ' + command )
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
                logging.debug("Read: " + data)

    def ListFiles(self, path):
        
        filenamePath = binascii.hexlify(path.encode("utf-16-be")).decode()
        fileList = self.SendCommandResult('AT+EFSL="' + filenamePath + '"',True)
        logging.debug("List path: " + path)
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
                logging.debug("{0:30s} {1:10s} {2:5s}".format( myname.decode('utf-16-be'),filesize,attrib))
        logging.debug("")
            

    def DeleteFile(self, pathFilename):
        # Folder operation Back to root folder
        logging.debug ("Delete File {0:s}".format(pathFilename))
        self.SendCommand('AT+EFSF=3')
        
        folder = binascii.hexlify(pathFilename.encode("utf-16-be")).decode()
        # send command ignore error if file does not exits
        
        self.SendCommand('AT+EFSD="' + folder + '"', True, True)
    
    def createFolder(self,folderName):
        
        logging.debug("Create folder:" + folderName)
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
        logging.debug("Bytes to send:{0:d}".format(size))
        if size == 0:
            raise Exception('File is empty')
        
        path = destpath + os.path.basename(filename)
       
        filenamePath = binascii.hexlify(path.encode("utf-16-be")).decode()
        logging.debug('Filename Path ' + path)

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

    def sendAutostart(self,name):
    
        path = "C:\\autostart.txt"
        filenamePath = binascii.hexlify(path.encode("utf-16-be")).decode()
        
        # open file for write
        self.SendCommand('AT+EFSW=0,"' + filenamePath + '"')
        
        # send last data to open file
        var = "[autostart]\nApp=C:\\MRE\\"+ name +"\n"
        data = binascii.hexlify(var.encode("utf-8")).decode()
        
        # send paket
        self.SendCommand('AT+EFSW=2,1,' + str(len(var)) + ',"' + data + '"')
        
        # close file
        self.SendCommand('AT+EFSW=1,"' + filenamePath + '"')
   
    def clearSketches(self, path):

        fileList = self.SendCommandResult('AT+EFSL="'+ binascii.hexlify(path.encode("utf-16-be")).decode() +'"',True)
        if len(fileList) == 0:
            return
        for item in fileList:
            diritem  = item.split(",")
            quoted = re.compile('"[^"]*"')
            for value in quoted.findall(item):
                value = value.replace('"', "")
                filename = binascii.unhexlify(value).decode("utf-16-be")
                logging.debug("File found: " + filename)
                if filename.endswith('.ino.vxp'):
                    logging.debug("Delete file:" + filename)
                    self.DeleteFile("C:\\MRE\\" + filename)

    def flushCom(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        
    def close(self):
        self.ser.close()


def main():
    parser = argparse.ArgumentParser(description = 'Push Application Utility', prog = 'uploader')
    parser.add_argument('-port', '-p', help = 'Serial port device', default = 'ttyACM1')
    parser.add_argument('-app', help='File for uploading', default='demo.ino')
    parser.add_argument('-clear', help='Clear old sketches in MRE folder', action='store_true')
    parser.add_argument('-verbose', '-v', help = 'Verbose output', action='count')

    args = parser.parse_args()

    myports= {"ttyACM0" : "ttyACM1", "ttyACM1" : "ttyACM2","ttyACM3" : "ttyACM4","ttyACM5" : "ttyACM6","ttyACM7" : "ttyACM8","ttyACM9" : "ttyACM10"}
    
    if os.path.isfile(args.app) == False:
        print ('Can not open file "' + args.app + '" for upload. Aborted')
        return

    print("Starting upload",file=sys.stdout, flush=True)

    rephonePort = '/dev/' + myports[args.port]
    # The modem port is the one not used for debugging, so always choose the "other" port
    h = MTKModem(rephonePort)
    #port = args.port[:-1] + '3'
    #h = MTKModem('/dev/%s' % (port))
    time.sleep(0.5)
    
    if args.verbose >3 :
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Opening communication..."+ rephonePort)

    h.SendCommand('AT')
    logging.debug("File for uploading:" + args.app)
    # exit all running process
    logging.debug("Stopping all processes...")
    h.SendCommand('AT+[666]EXIT_ALL', False)
    h.flushCom()
    time.sleep(1)

    logging.debug("Changing operation mode to obtain access to filesystem...")
    h.SendCommand('AT+ESUO=3',True,True)
        
    logging.debug("Folder operation back to root folder...")
    h.SendCommand('AT+EFSF=3',True,True)
    
    logging.debug("Create MRE folder...")
    
    # after a firmware upload C: is empty   
    h.createFolder('C:\MRE')

    logging.debug("Delete D:\\autoload.txt...")
    # delete autoload.txt on D:
    # the windows uploader tool writes here 
    h.DeleteFile('D:\\autoload.txt')
    
    
    logging.debug("Clearing old sketches from MRE folder...")
    if args.clear:
        h.clearSketches('C:\MRE')

    logging.debug("Sending new sketch: " + args.app)
    h.sendFile('C:\MRE\\', args.app)
    h.ListFiles('C:\MRE')

    logging.debug("Sending new 'autoload.txt'...")
    h.sendAutostart(os.path.basename(args.app))
    h.ListFiles('C:')
        
    logging.debug("Change operation mode to compatible...")
    h.SendCommand('AT+ESUO=4')

    logging.debug("Rebooting...")
    h.SendCommand('AT+[666]REBOOT', False) 
    print("Upload done", flush=True)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        #sys.stderr.write('ERROR: %s\n' % str(err))
        traceback.print_exc()
