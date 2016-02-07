
# 4_9-2014q4/

TOOLCHAIN=/home/mandl/gcc-arm-none-eabi-4_9-2014q4

CC=$(TOOLCHAIN)/bin/arm-none-eabi-gcc
AS=$(TOOLCHAIN)/bin/arm-none-eabi-as
LD=$(TOOLCHAIN)/bin/arm-none-eabi-gcc
OBJCOPY=$(TOOLCHAIN)/bin/arm-none-eabi-objcopy

INCLUDE=-I./include -I./2502A_DigitalClock/ResID -I./2502A_DigitalClock

#flags
CFLAGS = -mthumb-interwork -c -gdwarf-2 -gstrict-dwarf -fpic -mcpu=arm7tdmi-s -fvisibility=hidden -mthumb -mlittle-endian -O2 -D__COMPILER_GCC__  -D__HDK_LINKIT_ASSIST_2502__ -fno-exceptions -fno-non-call-exceptions $(INCLUDE)

ASFLAGS = 

BASENAME = main

ELFFILE = $(BASENAME).elf
AXF = $(BASENAME).axf
VXP = $(BASENAME).vxp


LSCRIPT = ./LINKIT10/armgcc_t/scat.ld



TARGETS = $(ELFFILE) $(AXF)

OBJS = ./2502A_DigitalClock/DigitalClock.o ./2502A_DigitalClock/lcd_sitronix_st7789s.o  ./LINKIT10/src/gccmain.o       

all:$(TARGETS)

$(ELFFILE): $(OBJS) Makefile
	$(CC) -o $(ELFFILE) $(OBJS) -T $(LSCRIPT) -Wl,--gc-sections -fpic -pie --specs=nosys.specs -B $(TOOLCHAIN)/arm-none-eabi/lib/thumb ./LINKIT10/armgcc/percommon.a
	

$(AXF): $(ELFFILE)
	$(OBJCOPY) -g -R .comment $(ELFFILE) $(AXF)
	$(OBJCOPY) --only-keep-debug $(ELFFILE) $(BASENAME)dbg.axf
	./merge_mtk.py $(AXF) mtk_header.bin $(VXP) 

clean:
	rm -f *.o *.lst *.map *.axf *.vxp *.elf $(OBJS) 

upload:
	./uploader.py
