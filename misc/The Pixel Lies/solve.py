#!/usr/bin/env python3
import numpy as np
from PIL import Image
import os

def extract_hidden_data(stego_image_path, output_path="recovered.png", original_width=None, original_height=None, is_grayscale=True):
    stego_img = Image.open(stego_image_path)
    stego_data = np.array(stego_img).flatten()
    
    stego_binary = ''.join([format(byte, '08b') for byte in stego_data])
    
    hidden_bits = ""
    for i in range(31, len(stego_binary), 32):
        if i < len(stego_binary):
            hidden_bits += stego_binary[i]
    
    print(f"Extracted {len(hidden_bits)} hidden bits")
    
    byte_array = bytearray()
    for i in range(0, len(hidden_bits), 8):
        if i + 8 <= len(hidden_bits):
            byte = int(hidden_bits[i:i+8], 2)
            byte_array.append(byte)
    
    if original_width is None or original_height is None:
        if os.path.exists("dimensions.txt"):
            try:
                with open("dimensions.txt", "r") as f:
                    dims = f.read().strip().split(",")
                    original_width = int(dims[0])
                    original_height = int(dims[1])
                print(f"Read dimensions from file: {original_width}x{original_height}")
            except Exception as e:
                print(f"Error reading dimensions: {e}")
                side = int(np.sqrt(len(byte_array)))
                original_width = original_height = side
    
    channels = 1 if is_grayscale else 3
    required_bytes = original_width * original_height * channels
    print(f"Using dimensions: {original_width}x{original_height} pixels, {'Grayscale' if is_grayscale else 'RGB'}")
    
    if len(byte_array) > required_bytes:
        byte_array = byte_array[:required_bytes]
    elif len(byte_array) < required_bytes:
        print(f"Warning: Not enough data for specified dimensions. Padding with zeros.")
        byte_array.extend([0] * (required_bytes - len(byte_array)))
    
    try:
        mode = 'L' if is_grayscale else 'RGB'
        shape = (original_height, original_width) if is_grayscale else (original_height, original_width, 3)
        array = np.array(list(byte_array), dtype=np.uint8).reshape(shape)
        recovered_img = Image.fromarray(array, mode=mode)
        recovered_img.save(output_path)
        print(f"Recovered image saved as {output_path}")
    except Exception as e:
        print(f"Error creating image: {e}")
        print("Try specifying the correct original width and height.")

def main():
    stego_image = "corrupted.png"
    output_image = "recovered.png"
    
    if not os.path.exists(stego_image):
        print(f"Error: {stego_image} not found!")
        return
    
    extract_hidden_data(stego_image, output_image, is_grayscale=True)
    
    extract_hidden_data(stego_image, "recovered_rgb.png", is_grayscale=False)

if __name__ == "__main__":
    main() 