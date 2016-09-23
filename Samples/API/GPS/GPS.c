/*
  This example code is in public domain.

  This example code is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
*/

/*
This example will open the GPS device and receive the current position.
Firstly it will open GPS with vm_gps_open. It then reads the GPS data and analyzes its GPGGA data.
Before you run this example, you need to insert a GPS antenna. 
Once the position is fixed, the example prints the number of satellites, latitude and longitude to monitor tool.

*/
#include <string.h>
#include "vmtype.h"
#include "vmsystem.h"
#include "vmlog.h"
#include "vmgps.h"

/* Parse token */
const VMCHAR *next_token(const VMCHAR* src, VMCHAR* buf) {

   VMINT i = 0; 

   while(src[i] != 0 && src[i] != ',') 
     i++; 
   
   if(buf){ 
     strncpy(buf, src, i); 
     buf[i] = 0; 
   } 
   
   if(src[i]) 
     i++; 
   return src+i; 
} 
 
/* Parse and print GPS GGA data */
void gps_print_gpgga(const VMCHAR* str){

  VMCHAR latitude[20]; 
  VMCHAR longitude[20]; 
  VMCHAR buf[20]; 
  const VMCHAR* p = str; 
   
  p = next_token(p, 0); /* GGA */
  p = next_token(p, 0); /* Time */
  p = next_token(p, latitude); /* Latitude */
  p = next_token(p, 0); /* N */
  p = next_token(p, longitude); /* Longitude */
  p = next_token(p, 0); /* E */
  p = next_token(p, buf); /* fix quality */
   
  if(buf[0] == '1') 
  { 
    /* GPS fix */
    p = next_token(p, buf); /* number of satellites */
    vm_log_info("GPS is fixed: %d satellite(s) found!", atoi(buf)); 
    vm_log_info("Latitude:%d", latitude); 
    vm_log_info("Longitude:%d",longitude); 
  } 
  else 
  { 
    vm_log_info("GPS is not fixed yet."); 
  } 
} 

/* GPS callback. */
static void gps_callback(VM_GPS_MESSAGE message, void* data, void* user_data){

     switch(message){
     case VM_GPS_OPEN_RESULT:
    {
             VMINT result = (VMINT)data;
             if(result == 1)
             {
                vm_log_info("open failed");
             }
             else
             {
                 vm_log_warn("open success");
                 /* set report period as 2 seconds */
                 vm_gps_set_parameters(VM_GPS_SET_LOCATION_REPORT_PERIOD, 2, NULL);
             }
         }
         break;
     case VM_GPS_SENTENCE_DATA:
         {
        	/* GPS data arriving */
            vm_gps_sentence_info_t info;
            memcpy(&info, (vm_gps_sentence_info_t*)data, sizeof(vm_gps_sentence_info_t));
            gps_print_gpgga(info.GPGGA);
         }
         break;
     }
 }

/* GPS power on. */
void gps_power_on(void)
{
  VMINT result;

  result = vm_gps_open( VM_GPS_ONLY, gps_callback, NULL);
  if(result == VM_SUCCESS)
  {
      vm_log_info("GPS open success");
  }
  else
  {
      vm_log_info("GPS open failed");
  }
}

/* The callback to be invoked by the system engine. */
void handle_sysevt(VMINT message, VMINT param) {
  switch (message) {
  case VM_EVENT_CREATE:
    gps_power_on();
    break;
  case VM_EVENT_QUIT:
    vm_gps_close();
    break;  
  }
}

/* Entry point */
void vm_main(void) {
    vm_pmng_register_system_event_callback(handle_sysevt);
}
