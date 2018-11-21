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

FREQUENCY = 440
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


def generate_tones(amount_of_tones):
    tone = []
    tones = []

    frequency_modifier = 0
    amplitude_modifier = (1 / amount_of_tones)

    for i in range(0, amount_of_tones):
        print((FREQUENCY + frequency_modifier))
        for j in range(0, N_FRAMES):
            part_of_a_sinewave = math.sin(2.0 * PI * (FREQUENCY + frequency_modifier) * (j / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * amplitude_modifier))
            print(part_of_a_sinewave)
            tone.append(part_of_a_sinewave)
        frequency_modifier = (frequency_modifier + 440)
        tones.append(tone)

    return combine_tones(tones)


def create_tone():
    amount_of_tones = int(input('How many tones to combine?: '))
    values = []
    combined_tone = generate_tones(amount_of_tones)
    for i in range(0, len(combined_tone)):

        packaged_value = struct.pack("i", int(combined_tone[i]))

        for j in range(0, N_CHANNELS):
            values.append(packaged_value)

    value_str = b''.join(values)
    noise_out.writeframes(value_str)
    noise_out.close()


def combine_tones(list_of_tones):

    combined_tone = []

    for i in range(0, len(list_of_tones[0])):
        combined_tone.append(0)
        for tone in list_of_tones:
            combined_tone[i] = combined_tone[i] + tone[i]

    print(combined_tone)

    return combined_tone


# largest = 0
# for value in values:
    # largest = max(largest, int(value))
# amplification = (32767.0 / largest)

# for value in values:
    # louder = amplification * int(value)
    # value = bytes(louder)
    # print(int(value))

create_tone()
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
