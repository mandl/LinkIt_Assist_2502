This is a beta toolchain for LinkIt_Assist_2502 for Linux

http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/whatis_2502/index.gsp

http://www.seeed.cc/rephone/



(1) Download the arm compiler

gcc-arm-none-eabi-4_9-2014q4-20141203-linux.tar.bz2

https://launchpad.net/gcc-arm-embedded

(2) Download the Windows SDK

http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_assist_2502/sdk_intro/index.gsp

(3) Use a Windows maschine for updating the firmware

(4) Switch off the device and connect it to USB. Copy autostart.txt in the root folder


Running the sample

make all
make upload

ToDo Understand the header format
ToDo Understand the resource file format and building
ToDo Understand the monitor tool




Power off and connect USB

Ubuntu Linux found /dev/ttyUSB0 and switch after some seconds to  USB Mass Storage device (5.2 MB )

Power on and conncect to USB

Ubuntu Linux found 

/dev/ttyACM0  ( Mtk Modem Port )  used for uploading *.vxp Applications
/dev/ttyACM1  ( Mtk Debug Port )  used for debugging 



