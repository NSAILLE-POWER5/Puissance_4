import pygame

class Sound:

    def __init__(self):
        pygame.mixer.init()  # Initialiser le module mixer
        self.pion_sound = pygame.mixer.Sound("pion.mp3")
        self.pion_sound.set_volume(0.5)

    def pion(self):
        self.pion_sound.play()

    def jouer_musique_jeu(self):
        pygame.mixer.music.load("fondsonore.mp3")  # Chargez la musique du jeu
        pygame.mixer.music.play(loops=-1, start=1.25)
        pygame.mixer.music.set_volume(0.25)

    def jouer_musique_menu(self):
        pygame.mixer.music.load("menu.mp3")  # Chargez la musique du menu
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.75)

    def jouer_musique_ia_hard(self):
        pygame.mixer.music.load("ia_hard")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.33)