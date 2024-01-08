import pygame
import sys

import sys

class ConnectFour:
    def __init__(self):
        pygame.init()
        #les constantes du programme
        self.inGame = False
        self.largeur = 7
        self.menuButtonColor = (140, 140, 140)
        self.menuButtonRect = pygame.Rect(0, 0, 0, 0)
        self.hauteur = 6
        self.taile_plateau = 120
        self.rayon = self.taile_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)
        self.fps = 30
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
        colone: colone ou on place le pion
        
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

    def check_hover(self, rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y):
            self.menuButtonColor = (90, 90, 90)
        else:
            self.menuButtonColor = (110, 110, 110)
    
    def write_text(self, font_adress, text_content, font_size, pos_x, pos_y, inflate_x, inflate_y,bg_color, font_color, reactive, Menu_button):
        font = pygame.font.Font(font_adress, font_size)
        text = font.render(text_content, True,  font_color, bg_color )
        rect = text.get_rect()
        rect.width += inflate_x
        rect.height += inflate_y
        rect.center = (pos_x, pos_y)
        text_rect = text.get_rect(center=rect.center)
        if reactive:
            self.check_hover(rect)
        if Menu_button:
            self.menuButtonRect = rect
        pygame.draw.rect(self.screen, bg_color, rect)
        self.screen.blit(text, text_rect)

    def run(self):
        """
        input:
        None
        32        boucle principale du jeux
        
        return:
        None
        """

        while not self.fin_partie:
            # ferme la fenetre si on appui sur le boutton croix en haut ou sur la touche echap
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.menuButtonRect.collidepoint(mouse_x, mouse_y) and not self.inGame:
                        self.inGame = True

                # fait bouger le pion en haut
                elif event.type == pygame.MOUSEMOTION:
                    if self.inGame:
                        pygame.draw.rect(self.screen, self.fond, (0, 0, self.taille[0], self.taille[1]))
                        colone = event.pos[0] // self.taile_plateau
                        pygame.draw.circle(self.screen, self.j1_couleur if self.joueur_actuel == 1 else self.j2_couleur,
                                        (colone * self.taile_plateau + self.taile_plateau // 2, self.taile_plateau // 2), self.rayon)
                        
                # fait tomber le pion
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.inGame:
                        colone = event.pos[0] // self.taile_plateau
                        ligne = event.pos[1] // self.taile_plateau
                        if self.placer_pion(colone):
                            if self.chercher_gagnant(ligne, colone):
                                self.fin_partie = True
                            else:
                                self.changer_joueur()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.menuButtonRect.collidepoint(mouse_x, mouse_y) and not self.inGame:
                        self.inGame = True

            if self.inGame:
                self.dessiner_plateau()

            else:
                self.screen.fill(self.fond)
                menu_rect = pygame.Rect(
                    (self.taille[0] - 0.4 * self.taille[0]) // 2,
                    (self.taille[1] - 0.5 * self.taille[1]) // 2,
                    0.4 * self.taille[0],
                    0.5 * self.taille[1]
                )

                pygame.draw.rect(self.screen, (125, 125, 125), menu_rect)
                
                font = "interface_graphique/menu_font.ttf"
                self.write_text(font_adress=font,
                                text_content="Play",
                                font_size=48,
                                pos_x=self.taille[0] // 2,
                                pos_y=self.taille[1] // 2,
                                inflate_x=100,
                                inflate_y=50,
                                bg_color=self.menuButtonColor,
                                font_color=(0, 0, 0),
                                reactive=True,
                                Menu_button=True)
                
                self.write_text(font_adress=font,
                                text_content="Puissance 4",
                                font_size=56,
                                pos_x=self.taille[0] // 2,
                                pos_y=self.taille[1] // 2 - self.taille[1] // 4,
                                inflate_x=100,
                                inflate_y=50,
                                bg_color=(255, 0, 0),
                                font_color=(255, 255, 0),
                                reactive=False,
                                Menu_button=False)
            pygame.display.flip()
            self.clock.tick(self.fps)

game = ConnectFour()
game.run()
