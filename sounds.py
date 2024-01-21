import pygame

class Sound:

    def __init__(self):
        pygame.mixer.init()  # Initialiser le module mixer
        self.pion_sound = pygame.mixer.Sound("pion.mp3")
        self.pion_sound.set_volume(0.5)
        self.final_sound = pygame.mixer.Sound("fin.mp3")
        self.final_sound.set_volume(1)
        self.music = 0

    def pion(self):
        self.pion_sound.play()

    def jouer_musique_jeu(self, mode, dif):
        if mode == 0: # Chargez la musique du jeu
            pygame.mixer.music.load("fondsonore.mp3")
            pygame.mixer.music.play(loops=-1, start=3)
            pygame.mixer.music.set_volume(0.15)
        else:
            musique = ("easy.mp3", "medium.mp3", "hard.mp3", "demoniaque.mp3")
            volume = (0.15, 0.20, 0.15, 0.15)
            pygame.mixer.music.load(musique[dif])
            pygame.mixer.music.play(loops=-1, start=1.25)
            pygame.mixer.music.set_volume(volume[dif])


    def jouer_musique_menu(self):
        pygame.mixer.music.load("menu.mp3")  # Chargez la musique du menu
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

    def final(self):
        self.final_sound.play()
