/*
  This sample code is in public domain.

  This sample code is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
*/

/* 
  This sample connects to an AP with the ssid and password.

  It set the device to station mode first by API vm_wlan_mode_set(), after set mode
  successfully, it will call vm_wlan_connect() to connect the AP, then print the
  AP information in the callback function.
  Modify the macro AP_SSID, AP_PASSWORD and AP_AUTHORIZE_MODE to connect your own AP.
*/ 

#include "vmtype.h" 
#include "vmsystem.h"
#include "vmlog.h" 
#include "ResID.h"
#include "WLANConnect.h"
#include "vmwlan.h"

#define AP_SSID "Xperia ray_null"
#define AP_PASSWORD "12345678"
#define AP_AUTHORIZE_MODE   VM_WLAN_AUTHORIZE_MODE_WPA2_ONLY_PSK

static VM_RESULT g_wlan_job_id;
static wlan_connect_callback(
            void *user_data,
            vm_wlan_connect_result_t *connect_result)
{
    if(VM_WLAN_SUCCESS == connect_result->result)
    {
        vm_log_info("Connect to AP successfully");
    }
    vm_log_info("AP info shows below:");
    vm_log_info("connect result:%d", connect_result->result);
    vm_log_info("connect cause:%d", connect_result->cause);
    vm_log_info("connect bssid:%s", connect_result->bssid);
    vm_log_info("connect ssid:%s", connect_result->ssid);
    vm_log_info("connect init_by_socket:%d", connect_result->init_by_socket);
    vm_log_info("connect ssid_length:%d", connect_result->ssid_length);
    vm_log_info("connect channel_number:%d", connect_result->channel_number);
    vm_log_info("connect profile_id:%d", connect_result->profile_id);
    vm_log_info("connect authorize_type:%d", connect_result->authorize_type);
    vm_log_info("connect eap_peap_authorize_type:%d", connect_result->eap_peap_authorize_type);
    vm_log_info("connect eap_ttls_authorize_type:%d", connect_result->eap_ttls_authorize_type);
    vm_log_info("connect connection_type:%d", connect_result->connection_type);
    vm_log_info("connect encry_mode:%d", connect_result->encry_mode);
    vm_log_info("connect passphrase:%s", connect_result->passphrase);
    vm_log_info("connect passphrase_length:%d", connect_result->passphrase_length);
    vm_log_info("connect need_login:%d", connect_result->need_login);
    vm_log_info("connect cancel_by_disconnect:%d", connect_result->cancel_by_disconnect);
    vm_log_info("connect rssi:%d", connect_result->rssi);
}

static void wlan_connect(void)
{
    vm_wlan_ap_info_t ap_info;
    VM_RESULT result;
    
    strcpy(ap_info.ssid, AP_SSID);
    strcpy(ap_info.password, AP_PASSWORD);
    ap_info.authorize_mode = AP_AUTHORIZE_MODE;
    result = vm_wlan_connect(&ap_info, wlan_connect_callback, NULL);
    vm_log_info("wlan_connect, return result:%d", result);

}
static void wlan_callback(void* user_data, VM_WLAN_REQUEST_RESULT result_type)
{
    vm_log_debug("wlan result:%d", result_type);
    if(VM_WLAN_REQUEST_DONE == result_type)
    {
        wlan_connect();
    }
}
static void wlan_mode_set(void)
{
    VM_RESULT result;
    result = vm_wlan_mode_set(VM_WLAN_MODE_STA, wlan_callback, NULL);
    vm_log_info("mode set return value:%d", result);
}

void handle_sysevt(VMINT message, VMINT param) 
{
    switch (message) 
    {
    case VM_EVENT_CREATE:
        wlan_mode_set();
        break;

    case VM_EVENT_QUIT:

        break;
    }
}

void vm_main(void)
{
    vm_pmng_register_system_event_callback(handle_sysevt);
}

