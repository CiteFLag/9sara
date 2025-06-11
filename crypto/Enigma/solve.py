#!/usr/bin/env python3
from enigma import EnigmaMachine

encrypted_message = "HDDEGHXRWUPJKUF QZO BWNEXJE IBL OMQPTM PSIOZS AQDT YCJIGSV CQXIXU WU HDZR PWZO LI LUQ RUC FEMGBMF JCIH"
rotors = ['I', 'II', 'III']
reflector = 'B'
ring_settings = [1, 1, 1]
plugboard_pairs = ['AB', 'CD', 'EF']
first_position = 'K'
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for second in alphabet:
    for third in alphabet:
        positions = [first_position, second, third]
        enigma = EnigmaMachine(rotors, reflector, ring_settings, positions, plugboard_pairs)
        decrypted = enigma.decrypt(encrypted_message)
        if any(word in decrypted for word in (" THE ", " AND ", " IS " , " FLAG ")):
            print('Rotor positions:', ''.join(positions))
            print('Decrypted:', decrypted)
            exit()
