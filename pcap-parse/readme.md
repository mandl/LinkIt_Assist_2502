

#Capture USB traffic

1. Setup wireshark

	sudo modprobe usbmon
	
	sudo chmod 644 /dev/usbmon*
	
	wireshark
	
2. Capture the traffic between the device and the download tool

3. Save file as *.pcap

4. run parse-commands

	./parse-commands *.pcap
