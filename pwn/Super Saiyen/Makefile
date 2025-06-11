CC = gcc
CFLAGS = -fno-stack-protector -no-pie -Wl,-z,norelro

TARGET = super-saiyan

all: $(TARGET)

$(TARGET): chall.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean 