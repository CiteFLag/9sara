import scapy.all as scapy
import struct
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys


KEY = bytes.fromhex('8f2a1d4b6e3c7f9a0b5c2d1e4f6a8b0c9d2e4f6a8b0c2d1e')
IV = bytes.fromhex('00000000000000000000000000000000')

def decrypt_data(encrypted_data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def extract_from_pcap(pcap_file):
    print(f"[*] Reading pcap file: {pcap_file}")
    

    packets = scapy.rdpcap(pcap_file)
    

    tcp_port_96 = [pkt for pkt in packets if pkt.haslayer(scapy.TCP) and 
                   (pkt[scapy.TCP].sport == 96 or pkt[scapy.TCP].dport == 96)]
    
    if not tcp_port_96:
        print("[!] No TCP packets on port 96 found in the capture")
        return
        
    print(f"[*] Found {len(tcp_port_96)} TCP packets on port 96")
    

    client_to_server = []
    for pkt in tcp_port_96:
        if pkt[scapy.TCP].dport == 96 and pkt.haslayer(scapy.Raw):
            client_to_server.append(pkt[scapy.Raw].load)
    
    if not client_to_server:
        print("[!] No payload data found in the packets")
        return
        
    print(f"[*] Extracted {len(client_to_server)} data packets")
    

    full_stream = b''.join(client_to_server)
    
    try:

        offset = 0
        

        filename_length = struct.unpack('!I', full_stream[offset:offset+4])[0]
        offset += 4
        

        encrypted_filename = full_stream[offset:offset+filename_length]
        offset += filename_length
        filename = unpad(decrypt_data(encrypted_filename), AES.block_size).decode()
        

        file_size = struct.unpack('!Q', full_stream[offset:offset+8])[0]
        offset += 8
        
        print(f"[*] Found file: {filename}")
        print(f"[*] Original file size: {file_size} bytes")
        

        if not os.path.exists('extracted_files'):
            os.makedirs('extracted_files')
            
        output_path = os.path.join('extracted_files', filename)
        

        extracted_data = b''
        
        while offset < len(full_stream):

            if offset + 4 > len(full_stream):
                break
                
            chunk_size = struct.unpack('!I', full_stream[offset:offset+4])[0]
            offset += 4
            

            if offset + chunk_size > len(full_stream):
                break
                
            encrypted_chunk = full_stream[offset:offset+chunk_size]
            offset += chunk_size
            

            decrypted_chunk = decrypt_data(encrypted_chunk)
            

            extracted_data += decrypted_chunk
        

        try:
            extracted_data = unpad(extracted_data, AES.block_size)
        except Exception as e:
            print(f"[!] Warning: Error removing padding: {e}")
            print("[*] Continuing with potentially padded data...")
        

        with open(output_path, 'wb') as f:
            f.write(extracted_data)
            
        print(f"[+] Successfully extracted and decrypted file: {output_path}")
        print(f"[+] Extracted {len(extracted_data)} bytes")
        
    except Exception as e:
        print(f"[!] Error extracting file from pcap: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract_file.py <pcap_file>")
        sys.exit(1)
        
    pcap_file = sys.argv[1]
    extract_from_pcap(pcap_file)