import os
import wave
import struct
import math
import random

def generate_ambient_sounds():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    configs = {
        "forest": (220, 440, "Soft wind & birds tone"),
        "river": (150, 300, "Flowing water frequency"),
        "wind": (100, 180, "Deep relaxing wind breeze"),
        "rain": (280, 560, "Rhythmic rain droplets")
    }

    sample_rate = 22050  # 22.05 kHz for lightweight files
    duration_sec = 15     # 15 second loopable ambient track

    for name, (f1, f2, desc) in configs.items():
        wav_path = os.path.join(sounds_dir, f"{name}.wav")
        mp3_path = os.path.join(sounds_dir, f"{name}.mp3")
        
        n_samples = int(sample_rate * duration_sec)
        print(f"Generating {name} sound ({desc})...")
        
        with wave.open(wav_path, 'wb') as wav:
            wav.setnchannels(1)  # Mono
            wav.setsampwidth(2)  # 16-bit PCM
            wav.setframerate(sample_rate)
            
            frames = bytearray()
            for i in range(n_samples):
                t = i / sample_rate
                # Harmonic ambient wave with gentle modulation
                env = 0.5 + 0.5 * math.sin(2 * math.pi * 0.2 * t)
                val1 = math.sin(2 * math.pi * f1 * t)
                val2 = math.sin(2 * math.pi * f2 * t)
                noise = (random.random() - 0.5) * 0.15
                
                signal = (0.4 * val1 + 0.3 * val2 + noise) * env * 0.3
                sample = int(signal * 32767)
                sample = max(-32768, min(32767, sample))
                frames.extend(struct.pack('<h', sample))
                
            wav.writeframes(frames)
            
        # Also create a copy as .mp3 filename so any code expecting .mp3 gets a valid playable audio file
        with open(wav_path, 'rb') as f_in, open(mp3_path, 'wb') as f_out:
            f_out.write(f_in.read())
            
        print(f"  Saved {wav_path} and {mp3_path}")

    print("\nALL ambient sound files successfully created!")

if __name__ == "__main__":
    generate_ambient_sounds()
