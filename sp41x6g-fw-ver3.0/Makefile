C_SRC := sp41x6g-fw-ver.c
CFLAGS := -g -O2 -Werror -Wall

RM := rm -rf
ELF ?= $(basename $(firstword $(C_SRC)))
OBJ := $(patsubst %.c,%.o,$(C_SRC))

.PHONY: all
all: $(ELF)

.PHONY:
clean:
	$(RM) $(ELF) $(OBJ)

$(OBJ): %.o: %.c
	$(RM) $(ELF)
	$(CROSS_COMPILE)gcc $(CFLAGS) -c $< -o $@

$(ELF): $(OBJ)
	$(CROSS_COMPILE)gcc $(CFLAGS) $(OBJ) -o $@ -static
	$(CROSS_COMPILE)strip $(ELF)
