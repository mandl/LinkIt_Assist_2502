#
# Makefile for a rephone sample under Linux
#
# https://github.com/mandl/LinkIt_Assist_2502
#

# Set your path to gcc-arm-none-eabi-4_9-2014q4
TOOLCHAIN=~/gcc-arm-none-eabi-4_9-2014q4

# Set your LinkIt sdk path
LINKIT_ASSIST_SDK_PATH=/home/mandl/Entwicklung

CC=$(TOOLCHAIN)/bin/arm-none-eabi-gcc
AS=$(TOOLCHAIN)/bin/arm-none-eabi-as
LD=$(TOOLCHAIN)/bin/arm-none-eabi-gcc
OBJCOPY=$(TOOLCHAIN)/bin/arm-none-eabi-objcopy

INCLUDE=-I$(LINKIT_ASSIST_SDK_PATH)/LINKIT_ASSIST_SDK/include

#flags
CFLAGS = -mthumb-interwork -c -gdwarf-2 -gstrict-dwarf -fpic -mcpu=arm7tdmi-s -fvisibility=hidden -mthumb -mlittle-endian -O2 -D__COMPILER_GCC__  -D__HDK_LINKIT_ASSIST_2502__ -fno-exceptions -fno-non-call-exceptions $(INCLUDE)

ASFLAGS = 

BASENAME = main

ELFFILE = $(BASENAME).elf
AXF = $(BASENAME).axf
VXP = $(BASENAME).vxp


LSCRIPT = $(LINKIT_ASSIST_SDK_PATH)/LINKIT_ASSIST_SDK/lib/LINKIT10/armgcc/scat.ld -lm

TARGETS = $(ELFFILE) $(AXF)

OBJS = SpinningLine.o lcd_sitronix_st7789s.o $(LINKIT_ASSIST_SDK_PATH)/LINKIT_ASSIST_SDK/lib/LINKIT10/src/gccmain.o       

all:$(TARGETS)

$(ELFFILE): $(OBJS) Makefile
	$(CC) -o $(ELFFILE) $(OBJS) -T $(LSCRIPT) -Wl,--gc-sections -fpic -pie --specs=nosys.specs -B $(TOOLCHAIN)/arm-none-eabi/lib/thumb $(LINKIT_ASSIST_SDK_PATH)/LINKIT_ASSIST_SDK/lib/LINKIT10/armgcc/percommon.a
	

$(AXF): $(ELFFILE)
	$(OBJCOPY) -g -R .comment $(ELFFILE) $(AXF)
	$(OBJCOPY) --only-keep-debug $(ELFFILE) $(BASENAME)dbg.axf
	../../../merge_mtk.py $(AXF) $(VXP) 

clean:
	rm -f *.o *.lst *.map *.axf *.vxp *.elf $(OBJS) 

upload:$(TARGETS)
	../../../uploader.py
