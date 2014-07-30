#
# Copyright (c) 2014 Shailen Sobhee
#

all: pcm roof.x

PCMLIB=/home/shailen/Projects/Kepler-workspace/roofline-plotter/lib/pcm-2.6
SRC=src
CC=g++ 
OPT= -g -O3 -I$(PCMLIB)

# uncomment if you want to rely on Linux perf support (user needs CAP_SYS_ADMIN privileges)
ifneq ($(wildcard /usr/include/linux/perf_event.h),)
#OPT+= -DPCM_USE_PERF 
endif

UNAME:=$(shell uname)

ifeq ($(UNAME), Linux)
LIB= -lpthread -lrt
endif
ifeq ($(UNAME), Darwin)
LIB= -lpthread -lPcmMsr
endif
ifeq ($(UNAME), FreeBSD)
LIB= -lpthread
endif

# PCMLIB=/home/shailen/Projects/Kepler-workspace/Roofline-Plotter/pcm-2.6/*
TEMP=pcm-2.6/

pcm:
	cd $(PCMLIB) && $(MAKE)

roof.o: $(SRC)/RooflinePlotter.cpp $(PCMLIB)/cpucounters.h $(PCMLIB)/msr.h $(PCMLIB)/pci.h $(PCMLIB)/client_bw.h
	$(CC) $(OPT) $(SRC)/RooflinePlotter.cpp -c -o $(SRC)/RooflinePlotter.o 

roof.x: pcm roof.o
	$(shell cd $(SRC); $(CC) $(OPT) RooflinePlotter.o $(PCMLIB)/pci.o $(PCMLIB)/msr.o $(PCMLIB)/cpucounters.o $(PCMLIB)/client_bw.o -o roof.x $(LIB))

nice:
	uncrustify --replace -c ~/uncrustify.cfg *.cpp *.h WinMSRDriver/Win7/*.h WinMSRDriver/Win7/*.c WinMSRDriver/WinXP/*.h WinMSRDriver/WinXP/*.c  PCM_Win/*.h PCM_Win/*.cpp  

clean:
	cd $(PCMLIB) && $(MAKE) clean
	cd $(SRC) && rm -rf *.x *.o *~
