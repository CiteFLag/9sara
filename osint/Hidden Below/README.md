**Description**

A security researcher has shown how legitimate enterprise infrastructure can be weaponized for covert command and control operations. You have minimal intelligence about the service used in their proof of concept.

Your mission is to identify the platform find the researcher who demonstrated this technique locate their demonstration video and recover the hidden flag.

Read the description slowly and start looking, if you faced any probleme durring challenge open ticket on discord 

**Flag Format**: CITEFLAG{...} 

---

**👤 Author:** *xtle0o0*

---

## Solution

This was surprisingly an easy challenge, though no one managed to solve it during the competition. The solution involved identifying a specific security researcher and locating their demonstration video.

### Hints Provided

During the challenge, several hints were dropped:
1. "Search for challenge author (real name) below"
2. "Find the video of the researcher, look below for author name in comments"
3. **Final hint (dropped in last 5 minutes)**: "john hammond"
4. **Additional hint**: "it was 2 months ago"

### Solution Methods

The challenge was solvable through two approaches:
1. **Manual YouTube searching**
2. **AI-assisted research**

### Step 1: AI-Assisted Research

Using ChatGPT to search for the wanted video by giving it the challenge description:

**ChatGPT Query**: https://chatgpt.com/share/6847ca2e-f1a4-8009-a2d5-d804e13630a3

The AI successfully identified the target video by John Hammond discussing enterprise infrastructure C2 techniques.

![AI Search Results](../../assets/Screenshot%202025-06-10%20070327.png)

### Step 2: Video Analysis

After locating John Hammond's video about weaponizing enterprise infrastructure for command and control, we need to examine the comments section as hinted.

### Step 3: Comment Investigation

Following the hint "look below for author name in comments," we sort the comments by **newest first** to find recent activity.

![Comments Section](../../assets/Screenshot%202025-06-10%20070509.png)

### Step 4: Flag Recovery

Searching through the comments reveals a comment from the challenge author containing the hidden flag.

![Flag Discovery](../../assets/Screenshot%202025-06-10%20070553.png)

CITEFLAG{5h4d0w_1nfr4_c2_m45t3r}