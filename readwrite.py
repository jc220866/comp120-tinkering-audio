import pygame
import sys
import wave
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('WAV')
chirp = pygame.mixer.Sound('chirp.wav')
pygame.mixer.music.load('strings.ogg')
pygame.mixer.music.play(-1, 0.0)

catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

PURPLE = (255, 0, 255)
chirpvolume = 0.60
musicvolume = 0.3
chirp.set_volume(chirpvolume)
pygame.mixer.music.set_volume(musicvolume)
playingmusic = True
print('Chirp volume is: ' + str(chirpvolume))
print('Music volume is: ' + str(musicvolume))


while True:  # the main game loop
    DISPLAYSURF.fill(PURPLE)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if playingmusic:
                    print('Space pressed, pausing music.')
                    pygame.mixer.music.pause()
                    playingmusic = False
                elif not playingmusic:
                    print('Space pressed, unpausing music.')
                    pygame.mixer.music.unpause()
                    playingmusic = True

            if event.key == K_RIGHT:
                if musicvolume < 0.85:
                    musicvolume += 0.1
                    pygame.mixer.music.set_volume(musicvolume)
                    print('Music volume set to: ' + str(musicvolume))
                else:
                    musicvolume = 1.0
                    pygame.mixer.music.set_volume(musicvolume)
                    print('Music volume set to: ' + str(musicvolume))
            if event.key == K_LEFT:
                if musicvolume > 0.15:
                    musicvolume -= 0.1
                    pygame.mixer.music.set_volume(musicvolume)
                    print('Music volume set to: ' + str(musicvolume))
                else:
                    musicvolume = 0.0
                    pygame.mixer.music.set_volume(musicvolume)
                    print('Music volume set to 0, music muted.')

            if event.key == K_p:
                print('Playing chirp.')
                chirp.play()
            if event.key == K_UP:
                if chirpvolume < 1.0:  # volume above 1.0 has no effect
                    chirpvolume += 0.20
                    chirp.set_volume(chirpvolume)
                    print('Chirp volume set to: ' + str(chirpvolume))
            if event.key == K_DOWN:
                if chirpvolume > 0.25:  # floats in python are buggy (see prints)
                    chirpvolume -= 0.20
                    chirp.set_volume(chirpvolume)
                    print('Chirp volume set to: ' + str(chirpvolume))
                else:
                    chirpvolume = 0.0  # to prevent volume going negative
                    chirp.set_volume(chirpvolume)
                    print('Chirp volume set to 0, chirp muted.')

            if event.key == K_c:
                filename = 'this file was also made by the pygame gang'
                file = wave.open(filename + '.wav', "wb")
                sound = bytearray(range(69))
                file.setsampwidth(2)
                file.setframerate(5)
                file.setnchannels(1)
                file.writeframes(sound)

    pygame.display.update()
    fpsClock.tick(FPS)
