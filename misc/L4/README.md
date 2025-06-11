**Description**

Only a true genius will solve this one.
No further hints — you’ll need to think *outside the box* to succeed.

Access the server, and if you’re clever enough, the flag will be waiting:

**SSH Command:**
`ssh -p 2233 root@134.209.31.135`
**Password:** `root`

---

**👤 Authors:** *Npc's*

## Solution

This was quite a tricky challenge! I'm not sure how teams managed to solve it, but they did.

One team solved it by trying different approaches, while another team was fortunate enough to read the bash history before my automated script deleted it.

### Analysis

The challenge name "L4" suggests it's related to the Transport Layer (Layer 4 of the OSI model). Common protocols on this layer include TCP and UDP.

### Investigation

Upon conducting some investigation using `tcpdump` (which you'll find on the machine), you'll notice something unusual coming through on **port 6979**.

![Network Traffic Screenshot](../../assets/Screenshot%202025-06-10%20052622.png)

The captured data shows:
```
'PVGRSYNT{T00Q_Q4ZA_L0H_4E3_FZ4EG}'
```

### Flag Recovery

Simple ROT13 decoding reveals the flag:
```
'CITEFLAG{G00D_D4MN_Y0U_4R3_SM4RT}'
```
