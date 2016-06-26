#This is a toolchain for LinkIt_Assist_2502 for Linux



http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/whatis_2502/index.gsp

http://www.seeed.cc/rephone/


##Setup 

1. Download the arm compiler [gcc-arm-none-eabi-4_9-2014q4-20141203-linux.tar.bz2](https://launchpad.net/gcc-arm-embedded)

2. Download the [Windows SDK](http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/sdk_intro/index.gsp)

3. Install [pyserial](https://github.com/pyserial/pyserial).

4. Switch off the device and connect it to USB. Copy autostart.txt in the root folder

5. Open the Makefile and set your **TOOLCHAIN** Path and your **LINKIT_ASSIST_SDK_PATH**

##Running the sample


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


Ubuntu Linux found **/dev/ttyUSB0** and switch after some seconds to  USB Mass Storage device (5.2 MB ). This is partions C:

### Power on and conncect to USB

Ubuntu Linux found 




**/dev/ttyACM0**  ( Mtk Modem Port )  used for uploading *.vxp Applications


**/dev/ttyACM1**  ( Mtk Debug Port )  used for debugging 


The device as 2 partions C: and D:. 

Partions D: can only accessed via AT commands from the modem port. see *uploader.py*


Firmware Version **W15.19.p2-uart** 


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
	 

## Mac OS

1. Install [python](https://www.python.org/downloads/mac-osx/)

2. Use [fernvale-osx-codeless](https://github.com/jacobrosenthal/fernvale-osx-codeless) to get a com port.

3. Install the [gcc-arm](https://launchpad.net/gcc-arm-embedded/4.9/4.9-2014-q4-major) for Mac.



