Step back in time to World War II, where cryptographic battles were fought with mechanical ingenuity. You've intercepted an encrypted message from a mysterious source, along with details of an Enigma machine implementation. Your mission: determine the exact machine settings and decrypt the message to reveal the hidden flag.

Make sure to use all your hints 😉

**nc crypto.citeflag.online 13337**

---

**👤 Author:** *xtle0o0*

Participants were given the `enigma.py` implementation of the historic Enigma cipher and tasked with recovering the hidden flag by decrypting the intercepted message. Connecting to the challenge service reveals an interactive prompt:

```bash
root@citeflag:~# nc crypto.citeflag.online 13337
[ASCII art and welcome banner]

Welcome to the Enigma Challenge!

Can you decrypt the secret message to obtain the flag?
You must understand the inner workings of this historical encryption device.

The encrypted message was created using specific machine settings.
Your task is to figure out those settings and decrypt the message.

Commands available:
- HELP:           Show available commands
- ENCRYPT <msg>:  Encrypt a message using current settings
- DECRYPT <msg>:  Decrypt a message using current settings
- INFO:           Get information about the challenge
- FLAG <msg>:     Submit your decrypted message to get the flag
- EXIT:           Close the connection

Good luck!

╔═══════════════════════════════════════════════╗
║ Encrypted message to decrypt:                ║
║ HDDEGHXRWUPJKUF QZO BWNEXJE IBL OMQPTM       ║
║ PSIOZS AQDT YCJIGSV CQXIXU WU HDZR PWZO LI   ║
║ LUQ RUC FEMGBMF JCIH                        ║
╚═══════════════════════════════════════════════╝
Enter commands (type HELP for available commands):
>
```

Below is the core of the provided `EnigmaMachine` class:

- **Rotors**: Three rotors (I, II, III) with defined wirings and turnover notches.
- **Reflector**: Reflector B (or C) that maps each letter to its partner.
- **Ring Settings**: Offsets that shift the internal wiring alignment.
- **Rotor Positions**: Initial rotor offsets from ‘A’.
- **Plugboard**: A set of letter-pair swaps applied before and after the rotor mechanism.

---

### Hints Recap

1. **Rotors:** I, II, III (in that order).  
2. **Reflector & Rings:** Reflector B; all ring settings set to 1.  
3. **Plugboard:** Connections are A↔B, C↔D, E↔F.  
4. **First Rotor Position:** Starts at K.  

After exhausting all hints, any further `HINT` command yields:

```bash
> HINT
⚠️ You've used all available hints!
```

---

### Decryption Strategy

1. **Configure the Machine:**  
   - Rotors: I, II, III  
   - Reflector: B  
   - Ring Settings: [1, 1, 1]  
   - Plugboard Pairs: AB, CD, EF  
   - First Rotor Position: K  

2. **Brute-Force Remaining Positions:**  
   With the first rotor fixed at K, iterate through all 26×26 combinations for the second and third rotors. For each candidate setting:
   - Instantiate `EnigmaMachine` with the current rotor positions.
   - Decrypt the intercepted string.
   - Check for English plaintext markers (e.g., “ THE ”, “ AND ”, “ IS ”).

3. **Identify Correct Decryption:**  
   When a decrypted output contains common English words, record the rotor settings and reveal the hidden flag.

---

**Screenshots of the process:**  

![Terminal interaction showing brute-force output](../../assets/Screenshot%202025-06-10%20050944.png)  
![Final flag submission](../../assets/Screenshot%202025-06-10%20051045.png)