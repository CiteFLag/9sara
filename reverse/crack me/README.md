**Description**

Our security team intercepted a suspicious binary that seems to be protecting sensitive information. The binary asks for a password, and upon correct entry, reveals a hidden message. Your task is to reverse engineer the binary and figure out the password.



---

**👤 Author:** *xtle0o0*

## Solution Approach

**Initial Binary Analysis**

First things first, gotta scope out what we're dealing with here. Hit the binary with some basic recon to understand its structure and see what strings are hanging around:

```bash
$ file crack_me
# Check basic binary type and architecture

$ strings crack_me
# Look for interesting strings

$ chmod +x crack_me
$ ./crack_me
# Test basic functionality - requires a password
```

**Disassembly Deep Dive**

Now it's time to get into the weeds with some proper analysis tools. Fire up Ghidra, IDA Pro, radare2 etc:

```bash
$ r2 -A crack_me
# or
$ ghidra crack_me
```

Once you're in there, the disassembly reveals the whole architecture - there's a main function handling password input, some crypto validation function doing the heavy lifting on password processing, comparisons against encoded values, and finally a function that spits out the flag when you nail the correct password.

**Finding the Encoded Values**

Here's where it gets interesting. Buried in the binary is this vector of integer values that's basically the key to everything:

```
1827, 1859, 1571, 1699, 1731, 1923, 1619
```

You can dig these out of the .rodata section:

```bash
$ objdump -s -j .rodata ./crack_me
```

**Reverse Engineering the Crypto**

By analyzing the disassembly, you can figure out exactly what transformation the binary applies to passwords. Turns out it's doing this for each character:

```
For each character (c) in the input:
- Left shift 4 bits: (c << 4)
- XOR with 0x13
```

This maps directly to `val = (int(i) << 4) ^ 0x13` in the original source.

**Flipping the Algorithm**

To crack this, we just need to reverse those operations. For each encoded value, we XOR with 0x13, right shift 4 bits, then mask to get back the original character:

```python
def reverse_crypto(encoded_values):
    results = []
    for val in encoded_values:
        original = ((val ^ 0x13) >> 4) & 0xFF
        results.append(chr(original))
    return ''.join(results)
```

**Password Requirements Discovery**

Digging deeper into the binary reveals some additional constraints the password needs to satisfy - it's gotta be exactly 7 characters long, and the sum of all ASCII values needs to be over 700.

**Cracking the Password**

Time to put it all together. Running our reverse algorithm on those encoded values:

```python
encoded = [1827, 1859, 1571, 1699, 1731, 1923, 1619]
password = reverse_crypto(encoded)
# Results in "suckmyd"
```

**Flag Extraction**

Finally, feed the cracked password back to the original binary:

```bash
$ echo "suckmyd" | ./crack_me
Enter Password (or q to quit): CITEFLAG{r0s3bud_is_th3_k3y}
```

The binary runs through all its validation logic, sees that our password matches the encoded values perfectly and then the flag get printed.