import pygame
import sys


class ConnectFour:
    def __init__(self):
        pygame.init()
        #les constantes du programme

        self.largeur = 7
        self.hauteur = 6
        self.taile_plateau = 120
        self.rayon = self.taile_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)
        self.fps = 60
        # pour metre en plain ecran
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.plateau = [[0] * self.largeur for _ in range(self.hauteur)]
        self.joueur_actuel = 1
        self.fin_partie = False
        self.taille = pygame.display.get_surface().get_size()

    def dessiner_plateau(self):
        """
        input:
        None
        
        actualise le plateau
        appelé a chaque tour de la boucle principale
        
        return:
        None
        """
        for ligne in range(self.hauteur):
            for colone in range(self.largeur):
                pygame.draw.rect(self.screen, self.fond, (colone * self.taile_plateau, (ligne + 1) * self.taile_plateau, self.taile_plateau, self.taile_plateau))
                pygame.draw.circle(self.screen, self.rond if self.plateau[ligne][colone] == 0 else (self.j1_couleur if self.plateau[ligne][colone] == 1 else self.j2_couleur),
                (colone * self.taile_plateau + self.taile_plateau // 2, (ligne + 1) * self.taile_plateau + self.taile_plateau // 2), self.rayon)


    def placer_pion(self, colone):
        """
        input:
        colone: coloneone ou on place le pion
        
        ajoute un nouveau pion sur le plateau
        
        return:
        True si possible sinon False
        """
        for ligne in range(self.hauteur - 1, -1, -1):
            if self.plateau[ligne][colone] == 0:
                self.plateau[ligne][colone] = self.joueur_actuel
                return True
        return False


    def chercher_gagnant(self, ligne, colone):
        """
        input:
        ligne: ligne du pion centrae de la recherche
        colone: coloneone du pion centrale de la recherche
        
        tres mal fait je sais mais c'est pas a moi de m'en occuper
        
        return:
        True si un gagnant sinon False
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = ligne + i * dr, colone + i * dc
                if 0 <= r < self.hauteur and 0 <= c < self.largeur and self.plateau[r][c] == self.joueur_actuel:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = ligne - i * dr, colone - i * dc
                if 0 <= r < self.hauteur and 0 <= c < self.largeur and self.plateau[r][c] == self.joueur_actuel:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False


    def changer_joueur(self):
        """
        input:
        None
        
        change le joueur actuel
        
        return:
        None
        """
        self.joueur_actuel = 3 - self.joueur_actuel

    def run(self):
        """
        input:
        None
        
        boucle principale du jeux
        
        return:
        None
        """
        while not self.fin_partie:
            #ferme la fenetre si on appui sur le boutton croix en haut
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #fait bouger le pion en haut
                elif event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.fond, (0, 0, self.taille[0] , self.taille[1]))
                    colone = event.pos[0] // self.taile_plateau
                    pygame.draw.circle(self.screen, self.j1_couleur if self.joueur_actuel == 1 else self.j2_couleur,
                                       (colone * self.taile_plateau + self.taile_plateau // 2, self.taile_plateau // 2), self.rayon)
                #fait tomber le pion
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    colone = event.pos[0] // self.taile_plateau
                    ligne= event.pos[1] // self.taile_plateau
                    if self.placer_pion(colone):
                        if self.chercher_gagnant(ligne, colone):
                            print(f"Player {self.joueur_actuel} wins!")
                            self.fin_partie = True
                        else:
                            self.changer_joueur()
            self.dessiner_plateau()
            pygame.display.flip()
            self.clock.tick(self.fps)


game = ConnectFour()
game.run()
