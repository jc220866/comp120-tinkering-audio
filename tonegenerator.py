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
PURPLE = (155, 0, 255)
FILE = 'sample.wav'

FREQUENCY_A = 440
FREQUENCY_B = 880
FREQUENCY_C = 1320
FREQUENCY_D = 1760
seconds = 1

N_CHANNELS = 1
SAMPLE_WIDTH = 2
FRAMERATE = 44100  # SAMPLE_RATE
N_FRAMES = (FRAMERATE * seconds)  # SAMPLE_LENGTH
COMP_TYPE = "NONE"
COMP_NAME = "not compressed"
AMPLITUDE = 32767  # BIT_DEPTH or MAX_VALUE - any higher than 32778 creates an awful noise
VOLUME = 1
PI = math.pi

noise_out = wave.open(FILE, 'wb')
noise_out.setparams((
    N_CHANNELS,
    SAMPLE_WIDTH,
    FRAMERATE,
    N_FRAMES,
    COMP_TYPE,
    COMP_NAME
    ))

values = []

for i in range(0, N_FRAMES):
    tone_A = math.sin(2.0 * PI * FREQUENCY_A * (i / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * 0.5))
    tone_B = math.sin(2.0 * PI * FREQUENCY_B * (i / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * 0.5))
    #tone_C = math.sin(2.0 * PI * FREQUENCY_C * (i / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * 0.25))
    #tone_D = math.sin(2.0 * PI * FREQUENCY_D * (i / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * 0.25))

    combined_tone = (tone_A + tone_B)# + tone_C + tone_D) * 1.30  # TODO hardcoding is naughty

    if combined_tone > AMPLITUDE:
        combined_tone = AMPLITUDE
    elif combined_tone < -AMPLITUDE:
        combined_tone = -AMPLITUDE

    print(int(combined_tone))

    packaged_value = struct.pack("i", int(combined_tone))

    for j in range(0, N_CHANNELS):
        values.append(packaged_value)

# largest = 0
# for value in values:
    # largest = max(largest, int(value))
# amplification = (32767.0 / largest)

# for value in values:
    # louder = amplification * int(value)
    # value = bytes(louder)
    # print(int(value))

value_str = b''.join(values)
noise_out.writeframes(value_str)
noise_out.close()
my_noise = pygame.mixer.Sound('sample.wav')

while True:
    DISPLAYSURFACE.fill(PURPLE)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                my_noise.play()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
