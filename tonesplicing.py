import pygame
import sys
import wave
import math
import struct
from pygame.locals import *

pygame.init()

FPS = 30
FPS_CLOCK = pygame.time.Clock()

DISPLAYSURFACE = pygame.display.set_mode((400, 300), 0, 32)
ORANGE = (210, 69, 0)
FILE = 'samplecopy.wav'
pregenerated_tone = wave.open(FILE, 'r')

length_of_each_sample = 0.2

'''
we are splitting and rearranging tones inside of an audio file
our audio file contains three tones of equal length, 0.2 seconds each

the middle tone will be the 'main' tone, the first and last will be endings for
the menu closing and the menu opening respectively
'''

# Translate the audio file into sample numbers that we can use in code
frames_in_total = pregenerated_tone.getnframes()
frames_per_tone = int(frames_in_total / 3)

frames_of_tone = pregenerated_tone.readframes(frames_in_total)
frames_of_tone = int(frames_of_tone)
print(str(frames_of_tone))


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
