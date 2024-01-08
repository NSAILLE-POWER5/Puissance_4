import pygame
import sys

class ConnectFour:
    def __init__(self):
        pygame.init()
        # Les constantes du programme
        self.largeur = 7
        self.hauteur = 6
        self.taile_plateau = 120
        self.rayon = self.taile_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)
        self.fps = 30
        # Pour mettre en plein écran
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.plateau = [[0] * self.largeur for _ in range(self.hauteur)]
        self.joueur_actuel = 1
        self.fin_partie = False
        self.taille = pygame.display.get_surface().get_size()

    def dessiner_plateau(self):
        """
        Actualise le plateau en le centrant dans la fenêtre.
        Appelé à chaque tour de la boucle principale.

        Input:
        None

        Output:
        None
        """
        for ligne in range(self.hauteur):
            for colone in range(self.largeur):
                # Calcul des coordonnées pour centrer le plateau
                x = colone * self.taile_plateau + (self.taille[0] - self.largeur * self.taile_plateau) // 2
                y = (ligne + 1) * self.taile_plateau + (
                            self.taille[1] - (self.hauteur + 1) * self.taile_plateau) // 2

                # Dessin du rectangle pour représenter l'emplacement de chaque cellule du plateau
                pygame.draw.rect(self.screen, self.fond, (x, y, self.taile_plateau, self.taile_plateau))

                # Dessin du cercle en fonction de l'occupation de la cellule
                if self.plateau[ligne][colone] == 1:
                    pygame.draw.circle(self.screen, self.j1_couleur,
                                       (x + self.taile_plateau // 2, y + self.taile_plateau // 2), self.rayon)
                elif self.plateau[ligne][colone] == 2:
                    pygame.draw.circle(self.screen, self.j2_couleur,
                                       (x + self.taile_plateau // 2, y + self.taile_plateau // 2), self.rayon)
                else:
                    pygame.draw.circle(self.screen, self.rond,
                                       (x + self.taile_plateau // 2, y + self.taile_plateau // 2), self.rayon)

    def placer_pion(self, colone):
        """
        Ajoute un nouveau pion sur le plateau.

        Input:
        colone: Colonne où on place le pion

        Output:
        True si possible, sinon False
        """
        for ligne in range(self.hauteur - 1, -1, -1):
            if self.plateau[ligne][colone] == 0:
                self.plateau[ligne][colone] = self.joueur_actuel
                return True
        return False

    def chercher_gagnant(self, ligne, colone):
        """
        Vérifie s'il y a un gagnant à partir d'une position donnée.

        Input:
        ligne: Ligne du pion central de la recherche
        colone: Colonne du pion central de la recherche

        Output:
        True si un gagnant, sinon False
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
        Change le joueur actuel.

        Input:
        None

        Output:
        None
        """
        self.joueur_actuel = 3 - self.joueur_actuel

    def run(self):
        """
        Boucle principale du jeu.

        Input:
        None

        Output:
        None
        """
        while not self.fin_partie:
            # Ferme la fenêtre si on appuie sur le bouton croix en haut ou sur la touche Echap
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # Fait bouger le pion en haut
                elif event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.fond, (0, 0, self.taille[0], self.taille[1]))
                    colone = event.pos[0] // self.taile_plateau
                    pygame.draw.circle(self.screen,
                                       self.j1_couleur if self.joueur_actuel == 1 else self.j2_couleur,
                                       (colone * self.taile_plateau + self.taile_plateau // 2,
                                        self.taile_plateau // 2), self.rayon)
                # Fait tomber le pion
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    colone = event.pos[0] // self.taile_plateau
                    ligne = event.pos[1] // self.taile_plateau
                    if self.placer_pion(colone):
                        if self.chercher_gagnant(ligne, colone):
                            self.fin_partie = True
                        else:
                            self.changer_joueur()
            self.dessiner_plateau()
            pygame.display.flip()
            self.clock.tick(self.fps)

game = ConnectFour()
game.run()
