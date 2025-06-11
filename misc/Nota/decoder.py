
import numpy as np
from scipy.io.wavfile import read
from scipy import signal
import matplotlib.pyplot as plt

def decode_audio(audio_file):
    # Load the audio file
    sample_rate, audio_data = read(audio_file)
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]  # Use only the first channel if stereo
    
    # Convert to float
    if audio_data.dtype != np.float32 and audio_data.dtype != np.float64:
        audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
    
    # Parameters based on the encoder
    note_duration = 0.4  # seconds
    pause_duration = 0.1  # seconds
    total_duration = note_duration + pause_duration
    samples_per_note = int(sample_rate * total_duration)
    
    # Calculate number of notes
    num_notes = len(audio_data) // samples_per_note
    
    # Extract frequencies using FFT for each note
    frequencies = []
    for i in range(num_notes):
        start = i * samples_per_note
        end = start + int(note_duration * sample_rate)
        if end > len(audio_data):
            break
            
        # Get the note segment
        note_segment = audio_data[start:end]
        
        # Use FFT to find the dominant frequency
        fft_result = np.fft.rfft(note_segment)
        fft_freqs = np.fft.rfftfreq(len(note_segment), 1/sample_rate)
        peak_idx = np.argmax(np.abs(fft_result))
        freq = fft_freqs[peak_idx]
        frequencies.append(freq)
    
    # Convert frequencies back to characters
    flag = ""
    base_freq = 261.63  # C4
    
    for freq in frequencies:
        # Reverse the formula from char_to_note function
        ascii_value = round((freq - base_freq) / 5)
        flag += chr(ascii_value)
    
    return flag, frequencies

if __name__ == "__main__":
    # Decode the flag
    audio_file = "flag_melody.wav"
    decoded_flag, frequencies = decode_audio(audio_file)
    
    print(f"Decoded message: {decoded_flag}")
    
    # Plot the frequencies
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, 'o-')
    plt.title('Decoded Frequencies')
    plt.xlabel('Character Index')
    plt.ylabel('Frequency (Hz)')
    plt.grid(True)
    plt.savefig('decoded_frequencies.png')
    print("Decoded frequency plot saved to decoded_frequencies.png")
