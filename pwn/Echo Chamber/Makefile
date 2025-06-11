CC := $(or $(CC),gcc)
CFLAGS := -no-pie -m32
CONTAINER := format_string_write

all: chall

clean: .PHONY
	rm -f chall

chall: chall.c
	$(CC) $(CFLAGS) $^ -o $@

docker: Dockerfile
	docker build -t $(CONTAINER) .

run: docker
	docker run -d --name $(CONTAINER) -m 32m --memory-swap 32m --read-only --restart always --cpus=".1" -p 2030:2030 $(CONTAINER)

extract: docker
	$(eval id := $(shell docker create $(CONTAINER)))
	docker cp $(id):/pwn/chall - | tar xv chall
	docker cp --follow-link $(id):/lib/i386-linux-gnu/libc.so.6 .
	docker rm -v $(id)

.PHONY: