/*
  This sample code is in public domain.

  This sample code is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
*/

/* 
  This sample draws a digital clock.
  It draws a color background with API vm_graphic_draw_solid_rectangle(),
  gets the time by vm_time_get_date_time(), and print the time text by API 
  vm_graphic_draw_text().
  Modify the macro SCREEN_WIDTH and SCREEN_HEIGHT to fit your display device.
*/

#include "vmtype.h"
#include "vmstdlib.h"
#include "vmlog.h"
#include "vmgraphic.h"
#include "vmsystem.h"
//#include "ResID.h"
#include "vmchset.h"
#include "vmgraphic_font.h"
#include "vmtimer.h"
#include "vmdatetime.h"
#include "lcd_sitronix_st7789s.h"
#include "vmdcl.h"
#include "vmdcl_gpio.h"
#include "vmdcl_pwm.h"



#define SCREEN_WIDTH    240
#define SCREEN_HEIGHT   240
#define STRING_LENGTH   10

#if defined(__HDK_LINKIT_ASSIST_2502__)
#define BACKLIGHT_PIN VM_PIN_P1
#else
#error " Board not support"
#endif

static VMUINT32* HARDWARE_CODE = (VMUINT32*)0x80000008;

static VMUINT32* RTC_TC_SEC =    (VMUINT32*)0xA0710014;

static VMUINT32* RTC_TC_MIN =    (VMUINT32*)0xA0710018;

static VMUINT32* RTC_POWERKEY1 = (VMUINT32*)0xA0710050;

vm_graphic_frame_t* g_frame_group[1];
vm_graphic_frame_t frame;
VMWCHAR g_wide_string[STRING_LENGTH];
VMINT g_clock_x;
VMINT g_clock_y;
VM_TIMER_ID_PRECISE g_timer_id;
VMUINT8* font_pool;

static void timer_callback(VM_TIMER_ID_PRECISE tid) {
    VMCHAR str[10];
    vm_graphic_color_argb_t color;
    vm_graphic_point_t positions[1] = {0, 0};
    VMINT size;
    vm_date_time_t date_time;
    VM_RESULT result;

    //vm_log_fatal("fatal timer");
	//vm_log_error("error timer Hello Ubuntu");
	//vm_log_warn("warn timer Hello rephone");

    //vm_log_info("info timer ding dang dong");
    vm_log_debug("debug timer  Hello Linux");

    vm_log_debug("Hardware code: %x",*HARDWARE_CODE);
    vm_log_debug("Tc Sec: %x",*RTC_TC_SEC);
    vm_log_debug("Tc Min: %x",*RTC_TC_MIN);



    color.a = 255;
    color.r = 243;
    color.g = 154;
    color.b = 30;
    vm_graphic_set_color(color);
    vm_graphic_draw_solid_rectangle(g_frame_group[0], 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    result = vm_time_get_date_time(&date_time);
    if(VM_IS_SUCCEEDED(result))
    {
        sprintf(str, "%02d:%02d:%02d", date_time.hour, date_time.minute, date_time.second);
        vm_chset_ascii_to_ucs2(g_wide_string, STRING_LENGTH * 2, str);
    }
    color.r = 255;
    color.g = 255;
    color.b = 255;
    vm_graphic_set_color(color);
    vm_graphic_draw_text(g_frame_group[0], g_clock_x, g_clock_y, g_wide_string);
    vm_graphic_blt_frame(g_frame_group, positions, 1);
}

static void draw_clock(void) {
    VM_RESULT result;
    VMUINT32 pool_size;



    frame.buffer_length = SCREEN_WIDTH * SCREEN_HEIGHT * 2;
    frame.buffer = (VMUINT8*)vm_malloc_dma(frame.buffer_length);
    if(frame.buffer == NULL)
    {
        return;
    }

    frame.color_format = VM_GRAPHIC_COLOR_FORMAT_16_BIT;
    frame.height = frame.width = SCREEN_WIDTH;
    g_frame_group[0] = &frame;
    result = vm_graphic_get_font_pool_size(0, 0, 0, &pool_size);
    if(VM_IS_SUCCEEDED(result))
    {
        font_pool = (VMUINT8*)vm_malloc(pool_size);
        if(NULL != font_pool)
        {
            vm_graphic_init_font_pool(font_pool, pool_size);
        }
    }
    vm_graphic_set_font_size(VM_GRAPHIC_LARGE_FONT);
    vm_chset_ascii_to_ucs2(g_wide_string, STRING_LENGTH * 2, "00:00:00");
    g_clock_x = (SCREEN_WIDTH - vm_graphic_get_text_width(g_wide_string)) >> 1;
    g_clock_y = (SCREEN_HEIGHT - vm_graphic_get_text_height(g_wide_string)) >> 1;
    g_timer_id = vm_timer_create_precise(500, (vm_timer_precise_callback)timer_callback, NULL);
    timer_callback(g_timer_id);
}

static void destroy_clock(void) {
    if(NULL != g_frame_group[0]->buffer)
    {
        vm_free(g_frame_group[0]->buffer);
        g_frame_group[0]->buffer = NULL;
    }
    if(NULL != font_pool)
    {
        vm_free(font_pool);
        font_pool = NULL;
    }
    vm_timer_delete_precise(g_timer_id);
}

void handle_sysevt(VMINT message, VMINT param) {

	switch (message) {

    	case VM_EVENT_CREATE:
            vm_res_init(0);
            break;
    	case VM_EVENT_PAINT:
    		draw_clock();
    		break;
    	case VM_EVENT_QUIT:
    		destroy_clock();
    		vm_res_release();
    		break;
	}
}

void lcd_backlight_level(VMUINT32 ulValue) {

      VM_DCL_HANDLE pwm_handle;
      vm_dcl_pwm_set_clock_t pwm_clock;
      vm_dcl_pwm_set_counter_threshold_t pwm_config_adv;

      vm_dcl_config_pin_mode(BACKLIGHT_PIN, VM_DCL_PIN_MODE_PWM);

      pwm_handle = vm_dcl_open(PIN2PWM(BACKLIGHT_PIN),vm_dcl_get_owner_id());
      vm_dcl_control(pwm_handle,VM_PWM_CMD_START,0);
      pwm_config_adv.counter = 100;
      pwm_config_adv.threshold = ulValue;
      pwm_clock.source_clock = 0;
      pwm_clock.source_clock_division =3;
      vm_dcl_control(pwm_handle,VM_PWM_CMD_SET_CLOCK,(void *)(&pwm_clock));
      vm_dcl_control(pwm_handle,VM_PWM_CMD_SET_COUNTER_AND_THRESHOLD,(void *)(&pwm_config_adv));
      vm_dcl_close(pwm_handle);
}

void vm_main(void) {


	lcd_st7789s_init();
    lcd_backlight_level(60);
	vm_pmng_register_system_event_callback(handle_sysevt);


}

