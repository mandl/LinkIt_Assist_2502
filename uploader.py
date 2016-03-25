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

import argparse
import os
import re
import serial
import sys
import time
import traceback


class MTKModem(object):

	WRITE_SIZE = 400

	def __init__(self, port):
		self.open(port)

	def open(self, port):
		self.ser = serial.Serial(port, 115200, timeout=5)
		self.ser.flushInput()
		self.ser.flushOutput()
        

	def SendCommand(self, command, getline=True, ignoreError=False):
		print 'send: %s' % (command)
		self.ser.write(command + '\r')
		data = ''
		if getline:
			data = self.ReadLine(ignoreError)
		return data 

	def SendCommandResult(self, command):
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
			if data != '':
				out.append(data)	
			



	def ReadLine(self, ignoreError):
		while 1:
			data = self.ser.readline().rstrip("\n\r")
			if data == 'OK':
				break
			if data == 'ERROR':
				if ignoreError:
					break
				raise Exception('Comm Error')
				
			if data != '':
				print data

	def ListFiles(self, path):
		
		fileList = self.SendCommandResult('AT+EFSL="' + path.encode("utf-16-be").encode("hex") + '"')
		print "List path: %s" % path
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
				print (value.decode("hex").strip() + "\t\t" + str(filesize) + "\t" + str(attrib))
		print ' '
			


	def DeleteFile(self, pathFilename):
		# Folder operation Back to root folder
		print 'Delete File %s' % pathFilename
		self.SendCommand('AT+EFSF=3')
		# send command ignore error if file does not exits
		self.SendCommand('AT+EFSD="' + pathFilename.encode("utf-16-be").encode("hex") + '"', True, True)
		

	def sendFile(self, filename):
   		if not os.path.isfile(filename):
			raise Exception('Can not open file: %s') % (filename)
        
		# open file		
		f = file(filename, 'rb')
 		st = os.stat(filename)
		
		size = st.st_size
		print 'Bytes to send %d' % (size)
		if size == 0:
			raise Exception('File is empty')
		
		path = 'c:\MRE\\' + filename
		filenamePath = path.encode("utf-16-be")

		print 'Filename Path %s' % filenamePath

		# open file for write
		self.SendCommand('AT+EFSW=0,"' + filenamePath.encode("hex") + '"')
		
		
		# send data to open file
		for i in range(st.st_size / self.WRITE_SIZE):
			var = f.read(self.WRITE_SIZE)
			data = var.encode("hex")
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
			data = var.encode("hex")
			# send lastpaket
			self.SendCommand('AT+EFSW=2,1,' + str(size) + ',"' + data + '"')
	
		# close file
		self.SendCommand('AT+EFSW=1,"' + filenamePath.encode("hex") + '"') 



	def flushCom(self):
		self.ser.flushInput()
		self.ser.flushOutput()


def main():


	parser = argparse.ArgumentParser(description='Push Application Utility', prog='uploader')

	parser.add_argument('--port', '-p', help='Serial port device', default='/dev/ttyACM0')
	# parser.add_argument('uploadfile', type=argparse.FileType('rb'), help='File for uploading')

	args = parser.parse_args()
	if os.path.isfile('main.vxp') == False:
		print 'Can not open main.vxp'
		return
	h = MTKModem(args.port)
	time.sleep(0.5)

	
	h.SendCommand('AT')
   	h.SendCommand('AT')

	# exit all running process
	h.SendCommand('AT+[666]EXIT_ALL', False)
	time.sleep(8)
	h.flushCom()
 	

	# Change operation mode to obtain access to filesystem	
	h.SendCommand('AT+ESUO=3')
		
	# AT+EFSR FileRead
	# h.SendCommand('AT+EFSR\r')

	# File System Size  67 = C:\
	# h.SendCommand('AT+EFS=67\r)

	# Folder operation Back to root folder
	h.SendCommand('AT+EFSF=3')
	
	# h.DeleteFile('D:\\autostart.txt')

	h.DeleteFile('C:\MRE\main.vxp')
	
	h.sendFile('main.vxp')

	h.ListFiles('C:\MRE')
	h.ListFiles('D:\MRE')
    # C: can also mount as disk ( power off the device )
	h.ListFiles('C:')
	# D: is a hidden volume
	h.ListFiles('D:')
	
		
	# Change operation mode to compatible
	h.SendCommand('AT+ESUO=4')

	h.SendCommand('AT+[666]REBOOT', False) 
	
 	
	# AT+EFSD Delete File


if __name__ == '__main__':
    try:
        main()
       
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        traceback.print_exc()


