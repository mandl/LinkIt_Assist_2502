
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
8. Connect to the download agent . Now the download agent takes over the communication.
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

<http://www.kosagi.com/w/index.php?title=MTK_Components>

## udev rule

Since Rephone is based on a Mediatek chip, ModemManager will, by default,
try to treat it as a modem and make it available for network connections.
This is undesirable.

To work around this problem, create a udev rule under /etc/udev/rules.d/
called 71-rephone.rules with the following contents:

	ATTRS{idVendor}=="0e8d" ATTRS{idProduct}=="0003", ENV{ID_MM_DEVICE_IGNORE}="1"

	ATTRS{idVendor}=="0e8d" ATTRS{idProduct}=="0023", ENV{ID_MM_DEVICE_IGNORE}="1"

## Backup your flash

see [backup](https://github.com/mandl/fernly/blob/master/read_flash.md)	


## Upload process

1. Install the udev rule *71-rephone.rules*
2. Disconnect the battery.

We need in the same folder

1. **/Download_Agent/6261/NOR_FLASH_TABLE**   This is the data for the NOR flash detection.
2. **/Download_Agent/6261/EXT_RAM**           This is the download agent.
3. **/Download_Agent/6261/INT_SYSRAM**        This is the download agent.
4. **/W15.19.p2-uart/EX_BOOTLOADER**
5. **/W15.19.p2-uart/SEEED02A_DEMO_BOOTLOADER_V005_MT2502_MAUI_11CW1418SP5_W15_19.bin**
6. **/W15.19.p2-uart/ROM**    this is the  *W15.19.p2-uart* version
7. **/W15.19.p2-uart/VIVA**   this is the  *W15.19.p2-uart* version

Doing the upload

1. Start the **firmwareUploader.py -nobat**
2. Disconnect the battery and connect the device to USB
3. The upload is running. The red led goes on dimmed.
4. See a lot of debug information.... wait for **Update done !!!!!!!!**...
5. Disconnect the device from USB.




## Troubleshoot


- If something goes wrong during upload. 
	Disconnect the device from USB port. Try again.
- Flashed a wrong a incomplete firmware. Wait 15 seconds for watchdog reset.

If nothing helps. Use the official windows version.


## Mac OS X

1. *firmwareUploader.py --port /dev/cu.usbmodem1410*


Update does **not** work .... at moment ...

    DA_LoadImage done
    Check Efuse backup data...
    maker 0x5a5a5a5a
    efuse_backup_data_1 0x0
    efuse_backup_data_2 0x500000
    DA_CBRInfo
    val: 0x0
    Traceback (most recent call last):
    File "./firmwareUploader.py", line 1645, in <module>
    main()
    File "./firmwareUploader.py", line 1622, in main
    h.DA_CBRInfo()
    File "./firmwareUploader.py", line 740, in DA_CBRInfo
    raise Exception('no nack')
    Exception: no nack

Try this version from Mediatek Labs

[mediatek_linkit_sdk_tools_osx](http://download.labs.mediatek.com/mediatek_linkit_sdk_tool_osx-1.1.21.tar.gz)

## Log file



## To Do

A better error handling. 

May be we have some timing issues

If you have a datasheet or some useful information

please send a e-mail to

Stefan.Mandl1@gmail.com
