from Crypto.Cipher import DES
import base64

def unpad(text):
    padding_length = text[-1]
    return text[:-padding_length]

def decrypt_flag(encrypted: bytes, key: str) -> bytes:
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    
    return cipher.decrypt(encrypted)

def main():
    key = "CITEFLAG"
    
    with open("encrypted.txt", "rb") as f:
        encrypted_b64 = f.read()
    
    encrypted = base64.b64decode(encrypted_b64)
    
    decrypted = encrypted
    for i in range(256):
        decrypted = decrypt_flag(decrypted, key)
    
    try:
        flag = decrypted.decode()
        print("Decrypted flag:", flag)
    except UnicodeDecodeError:
        print("Decryption failed - the result is not valid UTF-8")
        print("Raw bytes:", decrypted)

if __name__ == "__main__":
    main() 