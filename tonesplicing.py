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

length_of_each_sample = 0.2

'''
we are splitting and rearranging tones inside of an audio file
our audio file contains three tones of equal length, 0.2 seconds each

the middle tone will be the 'main' tone, the first and last will be endings for
the menu closing and the menu opening respectively
'''


def read_wav(filename):
    """
    this solution was provided by Dr. Scott via comp120 Slack channel

    :param filename:
    :return:
    """
    print('Reading wav file...')

    noise_in = wave.open(filename, 'r')

    channels = noise_in.getnchannels()
    sample_rate = noise_in.getframerate()
    sample_width = noise_in.getsampwidth()
    frame_count = noise_in.getnframes()

    raw_audio = noise_in.readframes(frame_count)
    noise_in.close()

    total_samples = frame_count * channels

    if sample_width == 1:
        fmt = "%ib" % total_samples
    elif sample_width == 2:
        fmt = "%ih" % total_samples
    else:
        raise ValueError("Not 8 or 16 bit")

    audio_data = struct.unpack(fmt, raw_audio)
    del raw_audio

    amount_of_tones = calculate_amount_of_tones(sample_rate, list(audio_data))
    frames_per_tone = int(frame_count / amount_of_tones)
    print('wav file read successfully. ')
    print('Amount of tones:', amount_of_tones)
    print('frames per tone:', frames_per_tone)

    return list(audio_data), amount_of_tones, frames_per_tone


# For every 0.2 seconds worth of samples in our audio file
def calculate_amount_of_tones(sample_rate, audio_data_list):
    """
    assuming we only use wav files consisting of multiple 200 millisecond-
    long tones joined together, this function calculates how many of those tones
    are within the audio file we are reading

    :param sample_rate: the framerate of the audio, typically 44100
    :param audio_data_list: the reading of the samples provided by read_wav()
    :return: the amount of 200 millisecond tones in our wav file
    """
    one_tone = (sample_rate / 5)
    amount_of_tones = len(audio_data_list) / one_tone

    return int(amount_of_tones)


def separate_tones(filename):

    audio_data_list, amount_of_tones, frames_per_tone = read_wav(filename)

    separated_tones = {}

    for i in range(0, amount_of_tones):

        key_number = str(i + 1)
        key_name = 'tone_' + key_number
        current_tone = []
        lower = i * frames_per_tone
        upper = lower + frames_per_tone

        for sample in audio_data_list[lower:upper]:
            # Split the entire file into lists(?), each list containing a 0.2 second tone
            # separated_tones[key_name] += sample
            current_tone.append(sample)

        separated_tones[key_name] = current_tone
        print('contents of tone', key_number, '= ', separated_tones[key_name])

    return separated_tones


def user_define_file():
    filename = input('Please specify the name of the wav file you wish to work with.\n'
                     'Do not include \".wav\" at the end, this is done automatically:\n')

    filename = filename + '.wav'
    print('filename is:', filename)

    return filename


def user_choose_tones_to_combine():

    amount_of_tones_to_combine = input('How many tones to combine?:\n')
    print('Please choose', amount_of_tones_to_combine, 'tones to combine.')
    # TODO ensure input is a sensible int and loop through 'amount_to_combine'
    # TODO ensure inputs for 'first' and 'second' are also integers between 0 and amount_of_tones
    tone_A = input('First tone: ')
    tone_B = input('Second tone: ')

    list_of_tones = [tone_A, tone_B]

    return list_of_tones


def combine_tones(dictionary_of_tones, list_of_tones):
    # TODO once again, make this a for loop for a variable amount of combinations
    tone_A = 'tone_' + str(list_of_tones[0])
    tone_B = 'tone_' + str(list_of_tones[1])

    print(tone_A)
    print(tone_B)

    tone_combination = dictionary_of_tones[tone_A] + dictionary_of_tones[tone_B]

    print(tone_combination)

    return tone_combination


def package_tone_combination(combined_tone):
    print('Choose a name for the current output.')
    output_filename = input('Again, the \'.wav\' suffix will be added automatically:\n')
    output_filename = output_filename + '.wav'

    # call a function to create blank .wav file with the user inputted file name to overwrite
    noise_out = wave.open(output_filename, 'wb')
    # noise_out = wave.open(generate_blank_file(output_filename), 'wb')
    noise_out.setparams((
        N_CHANNELS,
        SAMPLE_WIDTH,
        FRAMERATE,
        N_FRAMES,
        COMP_TYPE,
        COMP_NAME
    ))

    values = []
    for i in range(0, len(combined_tone)):

        packaged_value = struct.pack("h", int(combined_tone[i]))
        # we are assuming that we are working with mono (single channel) audio
        values.append(packaged_value)

    value_str = b''.join(values)
    noise_out.writeframes(value_str)
    noise_out.close()


# def generate_blank_file(input):



# Combine and save that list as a separate list
# export the samples for menuopen and menuclose as .wav files

# provide a way to play each separate sound with the number keys
    # so for example, the first combined tone the user creates with the 1 key
    # the second sound they create with the 2 key, up until we run out of keys

def main():
    tone_combination = combine_tones(separate_tones(user_define_file()), user_choose_tones_to_combine())
    package_tone_combination(tone_combination)

while True:
    DISPLAYSURFACE.fill(ORANGE)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                main()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
