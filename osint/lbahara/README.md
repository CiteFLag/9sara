**Description**  

Someone took this image from the middle of the sea — can you figure out who?

![lbahara](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmFrNnRydjUzZDhwNmlvOW1ibmg4dXk5NW1hMGQ3bWl6azVtMXlqeSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/UvOcKPHrkKSLm/giphy.gif)

**🎯 Flag Format**: `CITEFLAG{FirstName_LastName}`  

---

**👤 Authors:** Reo-0x  

---

The image provided:  
![Original Image](../../assets/image.jpg)

Looking at the image we can see some land, so it's close to coast.  

Check metadata using `exiftool`:  
![EXIF Data](../../assets/exf_image.png)  

📌 **Comment**: "The Mediterranean Sea"  
This suggests the image was likely taken somewhere in the Mediterranean region.  
By combining the landmass visible in the image with the hint from the EXIF data, let's open Google Maps and see:

![Map Matching](../../assets/map.png)

Check and...

![Final Match](../../assets/map1.png)

You can find the same view in the image — it was taken by **Manu Vilela**.

🟩 **Flag**: `CITEFLAG{Manu_Vilela}`
