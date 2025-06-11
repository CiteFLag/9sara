import scapy.all as scapy
import struct
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import sys

KEY = bytes.fromhex('8f2a1d4b6e3c7f9a0b5c2d1e4f6a8b0c9d2e4f6a8b0c2d1e')
IV = bytes.fromhex('00000000000000000000000000000000')

def decrypt_data(encrypted_data):
    if len(encrypted_data) % 16 != 0:
        padded_data = pad(encrypted_data, 16)
    else:
        padded_data = encrypted_data
    
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_data = cipher.decrypt(padded_data)
    return decrypted_data

def extract_from_pcap(pcap_file):
    print(f"[*] Reading pcap file: {pcap_file}")
    
    packets = scapy.rdpcap(pcap_file)
    
    port_96_packets = [pkt for pkt in packets if pkt.haslayer(scapy.TCP) and 
                  (pkt[scapy.TCP].sport == 96 or pkt[scapy.TCP].dport == 96)]
    
    port_69_packets = [pkt for pkt in packets if pkt.haslayer(scapy.TCP) and 
                    (pkt[scapy.TCP].sport == 69 or pkt[scapy.TCP].dport == 69)]
        
    print(f"[*] Found {len(port_96_packets)} TCP packets on port 96")
    print(f"[*] Found {len(port_69_packets)} TCP packets on port 69")

    
    output_file = "decrypted_communications.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Process port 96 packets
        f.write("===== PORT 96 COMMUNICATIONS =====\n\n")
        
        for pkt in port_96_packets:
            if pkt.haslayer(scapy.Raw):
                try:
                    data = pkt[scapy.Raw].load
                    decrypted = decrypt_data(data)
                    
                    try:
                        # Try to decode as text without unpadding first
                        decoded = decrypted.decode('utf-8', errors='replace')
                        
                        direction = "→" if pkt[scapy.TCP].dport == 96 else "←"
                        src_ip = pkt[scapy.IP].src
                        dst_ip = pkt[scapy.IP].dst
                        
                        f.write(f"{src_ip} {direction} {dst_ip}: {decoded}\n")
                    except Exception as e:
                        f.write(f"[Binary data from {pkt[scapy.IP].src}]: Failed to decode as text\n")
                except Exception as e:
                    f.write(f"[Error decrypting packet from {pkt[scapy.IP].src}]: {str(e)}\n")
        
        # Process port 69 packets
        f.write("\n\n===== PORT 69 COMMUNICATIONS =====\n\n")
        
        for pkt in port_69_packets:
            if pkt.haslayer(scapy.Raw):
                try:
                    data = pkt[scapy.Raw].load
                    
                    # For port 69 check if the data is encrypted
                    is_encrypted = True
                    try:
                        # Try to decode as plain text first
                        decoded = data.decode('utf-8', errors='strict')
                        is_encrypted = False
                    except UnicodeDecodeError:
                        # If it fails, it's likely encrypted
                        is_encrypted = True
                    
                    if is_encrypted:
                        decrypted = decrypt_data(data)
                        decoded = decrypted.decode('utf-8', errors='replace')
                    else:
                        decoded = data.decode('utf-8', errors='replace')

                    direction = "→" if pkt[scapy.TCP].dport == 69 else "←"
                    src_ip = pkt[scapy.IP].src
                    dst_ip = pkt[scapy.IP].dst
                    
                    f.write(f"{src_ip} {direction} {dst_ip}: {decoded}\n")
                except Exception as e:
                    f.write(f"[Error processing packet from {pkt[scapy.IP].src}]: {str(e)}\n")

    print(f"[+] Successfully extracted and decrypted communications to: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python general.py <pcap_file>")
        sys.exit(1)
        
    pcap_file = sys.argv[1]
    extract_from_pcap(pcap_file) 