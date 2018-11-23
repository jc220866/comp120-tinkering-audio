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
pygame.display.set_caption('Tone Generator')
PURPLE = (155, 0, 255)
FILE = 'sample.wav'

FREQUENCY = 340
seconds = 0.2

N_CHANNELS = 1
SAMPLE_WIDTH = 2
FRAMERATE = 44100  # SAMPLE_RATE
N_FRAMES = int((FRAMERATE * seconds))  # SAMPLE_LENGTH
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


def create_tone():
    '''
    this function is the 'main' function
    it prompts the user for input and calls the other functions to generate and combine tones
    then it packages and exports those tones into a .wav file that we open in the while loop

    :return: none
    '''
    amount_of_tones = int(input('How many tones to combine?: '))
    values = []
    combined_tone = generate_tones(amount_of_tones)
    for i in range(0, len(combined_tone)):

        packaged_value = struct.pack("h", int(combined_tone[i]))

        for j in range(0, N_CHANNELS):
            values.append(packaged_value)

    value_str = b''.join(values)
    noise_out.writeframes(value_str)
    noise_out.close()


def generate_tones(amount_of_tones):
    '''
    this function creates a list of lists - a list of tones
    each tone is made of a series of samples generated by the math.sin() function

    :param amount_of_tones: the user inputs how many tones they want to generate
    :return: the result of combine_tones()
    '''
    tone = []
    tones = []

    frequency_modifier = 0
    amplitude_modifier = (1 / amount_of_tones)

    for i in range(0, amount_of_tones):
        print((FREQUENCY + frequency_modifier))
        for j in range(0, N_FRAMES):
            part_of_a_sinewave = math.sin(2.0 * PI * (FREQUENCY + frequency_modifier) * (j / float(FRAMERATE))) * (VOLUME * (AMPLITUDE * amplitude_modifier))
            # print(part_of_a_sinewave)
            tone.append(part_of_a_sinewave)
        frequency_modifier = (frequency_modifier + 100)
        tones.append(tone)

    return combine_tones(tones)


def combine_tones(list_of_tones):
    '''
    this code is supposed to create a sawtooth-wave by combining different tones together
    but instead it appends these tones to eachother, creating a staircase of tones
    i am good probrammer

    :param list_of_tones: is the list of lists generated by generate_tones()
    :return: the result of combining the tones in the list of tones
    '''

    combined_tone = []

    for item in list_of_tones:
        print('hi')

    print(len(list_of_tones))
    print((len(list_of_tones[0]) / 4), ' - this should not be ', str(N_FRAMES))
    # print(len((list_of_tones[0] + list_of_tones[1] + list_of_tones[2] + list_of_tones[3])))

    for i in range(0, len(list_of_tones[0])):
        tone_sample = 0.0
        for tone in list_of_tones:
            print(float(tone[i]))
            tone_sample = tone_sample + float(tone[i])
            # print(tone_sample)
        combined_tone.append(tone_sample)

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
