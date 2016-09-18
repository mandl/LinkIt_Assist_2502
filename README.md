#This is a toolchain for LinkIt_Assist_2502 for Linux



http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/whatis_2502/index.gsp

http://www.seeed.cc/rephone/


##Setup 

1. Download the arm compiler [gcc-arm-none-eabi-4_9-2014q4-20141203-linux.tar.bz2](https://launchpad.net/gcc-arm-embedded)

2. Download the [Windows SDK](http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/sdk_intro/index.gsp)

3. Install [pyserial](https://github.com/pyserial/pyserial).

4. Add your user to dailout group.

	sudo adduser $USER dialout

5. Open the Makefile and set your **TOOLCHAIN** Path and your **LINKIT_ASSIST_SDK_PATH**

7. Install [Python 3.5.x](https://www.python.org/)

8. Install  udev rule under **/etc/udev/rules.d/** called **71-rephone.rules**. The magic job is here setting ID_MM_DEVICE_IGNORE environment value to inform ModemManager to skip device.

	ATTRS{idVendor}=="0e8d" ATTRS{idProduct}=="0003", ENV{ID_MM_DEVICE_IGNORE}="1"
	ATTRS{idVendor}=="0e8d" ATTRS{idProduct}=="0023", ENV{ID_MM_DEVICE_IGNORE}="1"
	


##Running the sample

1. Switch your device on

	make all

	make upload

##Tools


**merge_mtk.py**	adds a header and the size of the elf file for loading


**uploader.py**	stops the running process and uploads the main.vxp to the device and restarts the application.

**mon.py**	a simple debug monitor. Shows vm_log* messages from the device. 
Only works with Firmware Version **W15.19.p2** 

	ToDo Understand the header format

	ToDo Understand the resource file format and building

	ToDo Understand the monitor tool

*FirmwareUploader*/**firmwareUploader.py**  a firmware upload tool for linux.


## The Device

Firmware Version **W15.19.p2** 

LINKIT_ASSIST_SDK/tools/FirmwareUpdater/firmware/LinkIt_Device/LinkIt_Assist_2502

from the MediaTek_LinkIt_Assist_2502_SDK_2_0_46.zip


### Power off and connect USB


Ubuntu Linux found (idVendor=0e8d  idProduct=0003) **/dev/ttyUSB0** and switch after some seconds to  USB Mass Storage device  (idVendor=0e8d  idProduct=0002)(5.2 MB ). This is partions C:

### Power on and connect to USB

Ubuntu Linux found  ( idVendor=0e8d  idProduct=0023 )


**/dev/ttyACM0**  ( Mtk Modem Port )  used for uploading *.vxp Applications

**/dev/ttyACM1**  ( Mtk Debug Port )  used for debugging 


The device as 2 partions C: and D:. 

Partions D: can only accessed via AT commands from the modem port. see *uploader.py*


Firmware Version **W15.19.p2-uart** 

### Connect to USB without battery

Ubuntu Linux found (idVendor=0e8d  idProduct=0003) **/dev/ttyUSB0**. 
The device resets and connects again.

## Links

There is also a **Arduino IDE for RePhone for GNU/Linux users**

[Arduino IDE for RePhone on GNU/Linux](https://github.com/robarago/ArduinoGNULinux4RePhone)

or with **Eclipse**

[RePhone development on Linux](https://github.com/loboris/RePhone_on_Linux)


## Hacking

There is no memory protection unit in place. So we can direct access SOC hardware regs.

This is great for hacking ...
Sample

	static VMUINT32* HARDWARE_CODE = (VMUINT32*)0x80000008;
	
	vm_log_debug("%x",*HARDWARE_CODE);
	 

## Mac OS (El Capitan) 10.11.5

1. Install [Python 3.5.x](https://www.python.org/downloads/mac-osx/)

2. Install the [GCC ARM Embedded 4.9-2014-q4-major](https://launchpad.net/gcc-arm-embedded/4.9/4.9-2014-q4-major) for Mac.

### Test the USB port

Power on the device an connect it to the USB port.

Open the terminal.

	ioreg -p IOUSB -l
		
	+-o Product@14100000  <class AppleUSBDevice, id 0x1000007b1, registered, ma$
        {
           ...
          "Bus Power Available" = 500
          "USB Address" = 14
          "bMaxPacketSize0" = 8
          "iProduct" = 6
          "iSerialNumber" = 0
          ...
          "USB Vendor Name" = "MediaTek Inc"
          "idVendor" = 3725
           ...
        }

	ls /dev/cu* 
	
	/dev/cu.usbmodem1411             /dev/cu.usbmodem1413

Test the interface
	
	screen /dev/cu.usbmodem1411
type 

	AT
	
	OK

Run the uploader tool

	./uploader.py --port /dev/cu.usbmodem1411
	
Monitor tool

	./mon.py -p /dev/cu.usbmodem1413 --osx
