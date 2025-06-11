#!/usr/bin/env python3
import string

class EnigmaMachine:
    def __init__(self, rotors, reflector, ring_settings, rotor_positions, plugboard_pairs):
        self.ROTOR_WIRING = {
            'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
            'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
            'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
            'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
            'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
        }
        
        self.REFLECTOR_WIRING = {
            'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
        }
        
        self.rotors = rotors
        self.reflector = reflector
        self.ring_settings = ring_settings
        self.rotor_positions = [ord(pos) - ord('A') for pos in rotor_positions]
        
        self.plugboard = {}
        for pair in plugboard_pairs:
            if len(pair) == 2:
                a, b = pair[0], pair[1]
                self.plugboard[a] = b
                self.plugboard[b] = a
                
        self.alphabet = string.ascii_uppercase
    
    def _apply_plugboard(self, char):
        return self.plugboard.get(char, char)
    
    def _forward_through_rotors(self, char):
        c = ord(char) - ord('A')
        
        for i in range(len(self.rotors) - 1, -1, -1):
            rotor_type = self.rotors[i]
            rotor_wiring = self.ROTOR_WIRING[rotor_type][0]
            
            offset = self.rotor_positions[i]
            ring_offset = self.ring_settings[i] - 1
            
            c = (c + offset - ring_offset) % 26
            c = ord(rotor_wiring[c]) - ord('A')
            c = (c - offset + ring_offset) % 26
            
        return chr(c + ord('A'))
    
    def _backward_through_rotors(self, char):
        c = ord(char) - ord('A')
        
        for i in range(len(self.rotors)):
            rotor_type = self.rotors[i]
            rotor_wiring = self.ROTOR_WIRING[rotor_type][0]
            
            offset = self.rotor_positions[i]
            ring_offset = self.ring_settings[i] - 1
            
            c = (c + offset - ring_offset) % 26
            c = rotor_wiring.find(chr(c + ord('A'))) % 26
            c = (c - offset + ring_offset) % 26
            
        return chr(c + ord('A'))
    
    def _reflect(self, char):
        reflector_wiring = self.REFLECTOR_WIRING[self.reflector]
        c = ord(char) - ord('A')
        return reflector_wiring[c]
    
    def _step_rotors(self):
        if len(self.rotors) > 1:
            middle_rotor_type = self.rotors[1]
            middle_rotor_notch = self.ROTOR_WIRING[middle_rotor_type][1]
            middle_at_notch = chr((self.rotor_positions[1] % 26) + ord('A')) in middle_rotor_notch
            
            if middle_at_notch:
                self.rotor_positions[0] = (self.rotor_positions[0] + 1) % 26
                self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
            
        if len(self.rotors) > 2:
            right_rotor_type = self.rotors[2]
            right_rotor_notch = self.ROTOR_WIRING[right_rotor_type][1]
            right_at_notch = chr((self.rotor_positions[2] % 26) + ord('A')) in right_rotor_notch
            
            if right_at_notch and not middle_at_notch:
                self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
        
        if len(self.rotors) > 0:
            self.rotor_positions[-1] = (self.rotor_positions[-1] + 1) % 26
    
    def encrypt(self, text):
        result = []
        
        for char in text:
            if char.upper() in self.alphabet:
                self._step_rotors()
                
                is_lowercase = char.islower()
                char = char.upper()
                
                char = self._apply_plugboard(char)
                
                char = self._forward_through_rotors(char)
                
                char = self._reflect(char)
                
                char = self._backward_through_rotors(char)
                
                char = self._apply_plugboard(char)
                
                if is_lowercase:
                    char = char.lower()
                    
                result.append(char)
            else:
                result.append(char)
                
        return ''.join(result)
    
    def decrypt(self, text):
        return self.encrypt(text)
    
    def get_rotor_positions(self):
        return ''.join([chr((pos % 26) + ord('A')) for pos in self.rotor_positions])

if __name__ == "__main__":
    rotors = ['I', 'II', 'III']
    reflector = 'B'
    ring_settings = [1, 1, 1]
    rotor_positions = ['A', 'A', 'A']
    plugboard_pairs = ['AB', 'CD', 'EF']
    
    enigma = EnigmaMachine(rotors, reflector, ring_settings, rotor_positions, plugboard_pairs)
    
    message = "HELLO WORLD"
    encrypted = enigma.encrypt(message)
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    
    enigma = EnigmaMachine(rotors, reflector, ring_settings, rotor_positions, plugboard_pairs)
    decrypted = enigma.decrypt(encrypted)
    print(f"Decrypted: {decrypted}") 