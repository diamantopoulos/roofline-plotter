#
# Copyright (c) 2014 Shailen Sobhee
#
example: main

all: pcm roof.x

# Include public version of PCM
PCMLIB=lib/pcm-2.6
# Include unreleased/private PCM. Code not pushed to Github for NDA reasons.
PCMLIB_RESTRICTED=../ssg_intelpcm-main
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

pcm:
	cd $(PCMLIB) && $(MAKE)

pcm-restricted:
	cd $(PCMLIB_RESTRICTED) && $(MAKE)

roof.o: $(SRC)/RooflinePlotter.cpp $(PCMLIB)/cpucounters.h $(PCMLIB)/msr.h $(PCMLIB)/pci.h $(PCMLIB)/client_bw.h
	$(CC) $(OPT) $(SRC)/RooflinePlotter.cpp -c -o $(SRC)/RooflinePlotter.o 

roof.x: pcm roof.o
	$(CC) $(OPT) $(SRC)/RooflinePlotter.o $(PCMLIB)/pci.o $(PCMLIB)/msr.o $(PCMLIB)/cpucounters.o $(PCMLIB)/client_bw.o -o $(SRC)/roof.x $(LIB)

main.o: $(SRC)/RooflinePlotter.cpp
	$(CC) $(OPT) $(SRC)/RooflinePlotter.cpp -c -o $(SRC)/RooflinePlotter.o

main: main.o
	$(CC) $(OPT) $(SRC)/RooflinePlotter.o -o $(SRC)/out.x $(LIB)


nice:
	uncrustify --replace -c ~/uncrustify.cfg *.cpp *.h WinMSRDriver/Win7/*.h WinMSRDriver/Win7/*.c WinMSRDriver/WinXP/*.h WinMSRDriver/WinXP/*.c  PCM_Win/*.h PCM_Win/*.cpp  

clean:
	cd $(PCMLIB) && $(MAKE) clean
	cd $(SRC) && rm -rf *.x *.o *~
