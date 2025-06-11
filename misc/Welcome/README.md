**Description**

- The image location has nothing to do with the challenge.

- The flag is plainly visible right before your eyes.

- Once you uncover it, it will appear as **CITEFLAG{SOMETHING}**.


https://www.mediafire.com/file/buw57rdb2jm4mlk/image.png/file

---

**👤 Author:** *xtle0o0*

---

## Solution

I wasn't aware that `zsteg` could automatically detect and extract data from images that use binary steganography, where each pixel color represents one bit of the encoded message.

If I had known this, I would have decreased the points for this challenge or even never dropping it!

### Multiple Solution Paths

This challenge is solvable via:
1. **zsteg** (automated steganography detection tool)
2. **Writing your own decoding script**

### Original Intended Solution

My original idea was more complex:

1. **Rabbit Hole**: Place misleading metadata in the picture that leads to a ZIP archive
   - Archive URL: https://www.mediafire.com/file/ajemuxzjmn4hubf/archived_files.zip/file
   - The archive was password-protected and would take several minutes to crack

2. **Visual Analysis**: Participants were supposed to notice the weird pixels in the top-left corner
   - Each pixel represented either `0` or `1` 
   - By noting the pixel colors, contestants could craft a script to decode and retrieve the flag

### The Simple Solution

Unfortunately, `zsteg` made this much easier than intended! 

![Pixel Pattern Screenshot](../../assets/Screenshot%202025-06-10%20054724.png)

