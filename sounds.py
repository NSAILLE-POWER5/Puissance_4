import pygame

class Sound:


    def __init__(self):
        self.music = pygame.mixer_music.load("fondsonore.mp3")
        self.music_play = pygame.mixer.music.play(loops=-1)
        self.music_volume = pygame.mixer.music.set_volume(0.25)
        self.pion_son = pygame.mixer.Sound("pion.mp3")
        self.pion_son.set_volume(0.5)


    def pion(self):
        self.pion_son.play()