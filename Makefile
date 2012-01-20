
CC = gcc
LD = gcc
DEP = gcc -M
RM = rm -rf
DEPS = depend

ORIG_CC := $(CC)
CC = @echo CC $<; $(ORIG_CC)
ORIG_AS := $(AS)
AS = @echo AS $<; $(ORIG_AS)
ORIG_LD := $(LD)
LD = @echo LD $@; $(ORIG_LD)
ORIG_DEP := $(DEP)
DEP = @echo DEP $@; $(ORIG_DEP)

INCLUDE = -I/usr/include/CUnit
CFLAGS = -Wall -g $(INCLUDE)

LIB = -llibcunit

SRC = $(FILE)

OBJS = $(SRC:.c=.o) main.o

PROG = tests

$(PROG): $(OBJS)
	$(LD) $(LFLAGS) -o $@ $^ $(LIB)


PHONY: clean cleandep allclean

allclean: clean cleandep

clean:
	$(RM) *.o *.exe main.c

cleandep:
	$(RM) depend

$(DEPS): $(SRC)
	$(DEP) -M $(INCLUDE) $(SRC) > $(DEPS)

ifeq ($(findstring clean, $(MAKECMDGOALS)),)
-include $(DEPS)
endif

