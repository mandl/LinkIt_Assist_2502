
# The beta version for a linux firmware upload


## Some research:

The windows tools writes a log file. A good source of information

Steps

1. Connect to the bootloader inside the chip.
2. Disable the watchdog
3. Calibrate the internal PSRAM
4. Power up the baseband
4. Doing EMI remap
5. Upload **INT_SYSRAM** of the download agent to 0x70007000
6. Upload **EXT_RAM** of the download agent  to 0x10020000
7. Start download agent. Jump to address 0x70007000
8. Connect to the download agent . Now the download agent  takes over the communication.
9. Download agent starts to detect NOR/SF flash. Using the file **NOR_FLASH_TABLE**
12. Upload **SEEED02A_DEMO_BOOTLOADER_V005_MT2502_MAUI_11CW1418SP5_W15_19.bin**
13. Upload **EXT_BOOTLOADER**
15. Upload **ROM**
16. Upload **VIVA**
20. Create FAT Partition  Start address = 0x00500000 Length 0x00afe000
21. Disconnect

Useful links

<http://www.bunniestudios.com/blog/?p=4297>

<https://github.com/xobs/fernly>

<https://github.com/mtek-hack-hack/docs/wiki/FirmwareImageFormats>

## udev rule

Since Rephone is based on a Mediatek chip, ModemManager will, by default,
try to treat it as a modem and make it available for network connections.
This is undesirable.

To work around this problem, create a udev rule under /etc/udev/rules.d/
called 71-rephone.rules with the following contents:

    SUBSYSTEM=="tty", ATTRS{idVendor}=="0e8d",\
        ATTRS{idProduct}=="0003",\
        MODE="0660", SYMLINK+="rephone"

    ACTION=="add|change", SUBSYSTEM=="usb",\
        ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="0e8d",\
        ATTRS{idProduct}=="0003",\
        ENV{ID_MM_DEVICE_IGNORE}="1"

## Upload process

1. Install the udev rule *71-rephone.rules*

We need in the same folder

1. **/Download_Agent/6261/NOR_FLASH_TABLE**
2. **/Download_Agent/6261/EXT_RAM**
3. **/Download_Agent/6261/INT_SYSRAM**
4. **/W15.19.p2-uart/EX_BOOTLOADER**
5. **/W15.19.p2-uart/SEEED02A_DEMO_BOOTLOADER_V005_MT2502_MAUI_11CW1418SP5_W15_19.bin**
6. **/W15.19.p2-uart/ROM**    this is the  *W15.19.p2-uart* version
7. **/W15.19.p2-uart/VIVA**   this is the  *W15.19.p2-uart* version

Doing the upload

1. Start the *firmwareUploader.py*
2. Power off the device and connect it to the USB port.
3. The upload is running. The red led goes on dimmed.
4. See a lot of debug information.... wait for **Update done !!!!!!!!**...
5. Disconnect the device from USB.




## Troubleshoot

- Sometimes the first connect fails. Disconnect the device and reconnect it.
- If something goes wrong during upload. 
	Disconnect the device from USB port and disconnect also the battery !!. Try again
- Flashed a wrong a incomplete firmware. Wait 15 seconds for watchdog reset.

If nothing helps. Use the official windows version.

## To Do

A better error handling. 

Retry during upload a block

May be we have some timing issues

If you have a datasheet or some useful information

please send a e-mail to

Stefan.Mandl1@gmail.com
