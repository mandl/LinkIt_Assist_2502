This example scans the nearby APs and prints their information to log.

It set the device to station mode by API vm_wlan_mode_set, then call vm_wlan_scan. The results are reported to the registered scan callback function.
