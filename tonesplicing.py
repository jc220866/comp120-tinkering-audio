import pygame
import sys
import wave
import math
import struct
from pygame.locals import *

N_CHANNELS = 1
SAMPLE_WIDTH = 2
FRAMERATE = 44100  # SAMPLE_RATE
N_FRAMES = int((FRAMERATE * 0.2))  # SAMPLE_LENGTH
COMP_TYPE = "NONE"
COMP_NAME = "not compressed"
AMPLITUDE = 32767  # BIT_DEPTH or MAX_VALUE - any higher than 32778 creates an awful noise
VOLUME = 1

pygame.init()

FPS = 30
FPS_CLOCK = pygame.time.Clock()

DISPLAYSURFACE = pygame.display.set_mode((400, 300), 0, 32)
ORANGE = (210, 69, 0)
FILE = 'samplecopy.wav'
pregenerated_tone = wave.open(FILE, 'r')
pregenerated_tone_copy = wave.open(FILE, 'r')

length_of_each_sample = 0.2

'''
we are splitting and rearranging tones inside of an audio file
our audio file contains three tones of equal length, 0.2 seconds each

the middle tone will be the 'main' tone, the first and last will be endings for
the menu closing and the menu opening respectively
'''

# Translate the audio file into sample numbers that we can use in code
channels_of_file = pregenerated_tone.getnchannels()
frames_in_file = pregenerated_tone.getnframes()

print(channels_of_file, frames_in_file, ((frames_in_file * 5) / 3))

samples_of_file_in_bytes = pregenerated_tone_copy.readframes(frames_in_file)
print(samples_of_file_in_bytes)



list_of_samples_in_bytes = []
for i in range(0, frames_in_file):
    list_of_samples_in_bytes.append(samples_of_file_in_bytes[i])

print(list_of_samples_in_bytes)

'''
list_of_samples_in_bytes = []
for i in range(0, frames_in_file):
    list_of_samples_in_bytes.append(pregenerated_tone.readframes(i))

print(list_of_samples_in_bytes)

list_of_samples_in_numbers = []
for sample in list_of_samples_in_bytes:
    list_of_samples_in_numbers.append(struct.unpack('h', sample))

print()
print(list_of_samples_in_numbers)
'''


# str[len(str-1):]

'''
print(frames_in_file)
#frames_in_tone = int(frames_in_file / 3)

frames_of_file_bytes = pregenerated_tone.readframes(frames_in_file)

print("String of Bytes")
print(frames_of_file_bytes)

print("Attempt to Unpack")

audio_data = []
for value in frames_of_file_bytes:
    audio_data.append(struct.pack('h', value))


new_tone = wave.open('new_tone.wav', 'w')
new_tone.setparams((
    N_CHANNELS,
    SAMPLE_WIDTH,
    FRAMERATE,
    N_FRAMES,
    COMP_TYPE,
    COMP_NAME
    ))
print(type(audio_data))
new_tone.writeframes(b''.join(audio_data))
new_tone.close()
'''



"""
frames_of_file_bytes_split = frames_of_file_bytes.split(b'\\')
print(frames_of_file_bytes_split)

frames_of_file = []
for byte in frames_of_file_bytes_split:
    print(byte)
    frame = struct.unpack("h", byte)
    frames_of_file.append(frame)

print(frames_of_file)
"""

# For every 0.2 seconds worth of samples in our audio file
# Split the entire file into lists(?), each list containing a 0.2 second tone
# Each list will be saved as a separate name (low, main, high for example)

# Combine the samples for main and high (in that order)
# Save that list as a separate list (menuopen)
# Combine the samples for main and low (in that order)
# Save that list as another separate list (menuclose)

# export the samples for menuopen and menuclose as .wav files



while True:
    DISPLAYSURFACE.fill(ORANGE)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == KEYDOWN:
            #if event.key == K_SPACE:

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
