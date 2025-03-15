import random
import simpleaudio as sa

def generate_data(size):
    return [random.randint(1, 100) for _ in range(size)]

def play_sound():
    wave_obj = sa.WaveObject.from_wave_file("sound.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()