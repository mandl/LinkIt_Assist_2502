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

import serial
import time
import sys
import re
import argparse
import traceback
import os



class MTKModem(object):

	WRITE_SIZE = 400

	def __init__(self,port):
		self.open(port)

	def open(self,port):
		self.ser = serial.Serial(port, 115200, timeout=5)
		self.ser.flushInput()
		self.ser.flushOutput()
        

	def SendCommand(self,command, getline=True):
		print 'send: %s' % (command)
		self.ser.write(command + '\r')
		data = ''
		if getline:
			data=self.ReadLine()
		return data 

	def SendCommandResult(self,command):
		out = []	
		print 'send: %s' % (command)
		self.ser.write(command + '\r')
		while 1:
			data = self.ser.readline().rstrip("\n\r")
			if data == 'OK':
				return out
				break
			if data == 'ERROR':
				raise Exception('Comm Error')
			if data !='':
				out.append(data)	
			



	def ReadLine(self):
		while 1:
			data = self.ser.readline().rstrip("\n\r")
			if data == 'OK':
				break
			if data == 'ERROR':
				raise Exception('Comm Error')
			if data !='':
				print data

	def ListFiles(self,path):
		
		fileList = self.SendCommandResult('AT+EFSL="'+path.encode("utf-16-be").encode("hex") +'"')
		print "List path: %s" % path
		for item in fileList:
			#print item
			diritem  = item.split(",")
			filesize = diritem[1]
			attrib   = diritem[2]
			quoted = re.compile('"[^"]*"')
			for value in quoted.findall(item):
				value = value.replace('"', "")
				print (value.decode("hex").strip() + "\t\t" + str(filesize) + "\t" + str(attrib))
			


	def DeleteFile(self,pathFilename):
		# Folder operation Back to root folder
		self.SendCommand('AT+EFSF=3')
		self.SendCommand('AT+EFSD="'+pathFilename.encode("utf-16-be").encode("hex") +'"')
		

	def sendFile(self,filename):
   		if not os.path.isfile(filename):
			raise Exception('Can not open file: %s') % (filename)
        
		# open file		
		f = file(filename, 'rb')
 		st = os.stat(filename)
		
        
		print 'Bytes to send %d' % (st.st_size)
		if st.st_size == 0:
			raise Exception('File is empty')
		
		path = 'c:\MRE\\' + filename
		filenamePath = path.encode("utf-16-be")

		print 'Filename Path %s' % filenamePath

		# open fiel for write
		self.SendCommand('AT+EFSW=0,"'+ filenamePath.encode("hex") +'"')
		#time.sleep(0.5)

		# send data to open file
		for i in range(st.st_size / self.WRITE_SIZE):
			var = f.read(self.WRITE_SIZE)
			data = var.encode("hex")
			self.SendCommand('AT+EFSW=2,0,400,"' +data + '"')
			#time.sleep(0.5)
			#print 'Send data %s' % data

		lastsize = st.st_size % self.WRITE_SIZE
		# send last data to open file
		if st.st_size % self.WRITE_SIZE:
            
			var = f.read()
			data = var.encode("hex")
			self.SendCommand('AT+EFSW=2,1,'+ str(lastsize) +',"' +data + '"')
			#time.sleep(0.5)
			#print 'Send last data %s' % data

		# close file
		self.SendCommand('AT+EFSW=1,"' +filenamePath.encode("hex") +'"') 



	def flushCom(self):
		self.ser.flushInput()
		self.ser.flushOutput()


def main():


	parser = argparse.ArgumentParser(description = 'Push Application Utility', prog = 'uploader')

	parser.add_argument('--port', '-p',help = 'Serial port device',default = '/dev/ttyACM0')
	args = parser.parse_args()

	h = MTKModem(args.port)
	time.sleep(0.5)

	
	h.SendCommand('AT')
   	h.SendCommand('AT')

	# exit all running process
	h.SendCommand('AT+[666]EXIT_ALL',False)
	time.sleep(8)
	h.flushCom()

	# Change operation mode to obtain access to filesystem	
	h.SendCommand('AT+ESUO=3')
		
	# AT+EFSR FileRead
	#h.SendCommand('AT+EFSR\r')

	

	# File System Size  67 = C:\
	#h.SendCommand('AT+EFS=67\r)

	# Folder operation Back to root folder
	h.SendCommand('AT+EFSF=3')

	h.ListFiles('C:\MRE')
	h.ListFiles('D:\MRE')
	h.ListFiles('C:')
	h.ListFiles('D:')
	#h.DeleteFile('D:\\autostart.txt')
	
	h.sendFile('main.vxp')
	
		
	# Change operation mode to compatible
	h.SendCommand('AT+ESUO=4')

	h.SendCommand('AT+[666]REBOOT',False) 
	
 	
	# AT+EFSD Delete File


if __name__ == '__main__':
    try:
        main()
       
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        traceback.print_exc()


