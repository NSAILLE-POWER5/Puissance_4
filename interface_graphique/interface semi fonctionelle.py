import pygame
import sys

import sys
    
def draw_button(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    padding: tuple[int, int],
    bg_color: pygame.Color, hovered_color: pygame.Color,
    font_color: pygame.Color
    ) -> bool:
    """Renvoie si le bouton est survolé"""
    render_text = font.render(text, True, font_color, bg_color)
    rect = render_text.get_rect()
    rect.center = pos
    rect.width += padding[0]
    rect.height += padding[1]
    hovered = rect_hovered(rect)
    if hovered:
        pygame.draw.rect(screen, bg_color, rect)
    else:
        pygame.draw.rect(screen, hovered_color, rect)

    text_rect = render_text.get_rect(center=rect.center)
    screen.blit(render_text, text_rect)

    return hovered

def rect_hovered(rect: pygame.Rect) -> bool:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.collidepoint(mouse_x, mouse_y)

class Menu:
    def __init__(self):
        self.fond = (0, 0, 255)
        self.launch_hovered = False

    def event(self, event: pygame.event.Event) -> bool:
        """Renvoie si le bouton de lancement a été cliqué ou non"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.launch_hovered:
                return True
        return False

    def draw(self, screen: pygame.Surface):
        screen.fill(self.fond)

        taille = screen.get_size()
        menu_rect = pygame.Rect(
            (taille[0] - 0.4 * taille[0]) // 2,
            (taille[1] - 0.5 * taille[1]) // 2,
            0.4 * taille[0],
            0.5 * taille[1]
        )
        pygame.draw.rect(screen, (125, 125, 125), menu_rect)

        font = pygame.font.Font("interface_graphique/menu_font.ttf", 56)
        draw_button(
            screen, font, "Puissance 4",
            pos=(taille[0] // 2, taille[1] // 2 - taille[1] // 4),
            padding=(100, 50),
            bg_color=pygame.Color(255, 0, 0),
            hovered_color=pygame.Color(255, 0, 0),
            font_color=pygame.Color(255, 255, 0)
        )

        font = pygame.font.Font("interface_graphique/menu_font.ttf", 48)
        self.launch_hovered = draw_button(
            screen, font, "Play",
            pos=(taille[0] // 2, taille[1] // 2),
            padding=(100, 50),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
            font_color=pygame.Color(0, 0, 0)
        )

class ConnectFour:
    def __init__(self):
        #les constantes du programme
        self.largeur = 7
        self.hauteur = 6
        self.taile_plateau = 120
        self.rayon = self.taile_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)

        self.plateau = [[0] * self.largeur for _ in range(self.hauteur)]
        self.joueur_actuel = 1

    def draw(self, screen: pygame.Surface):
        """
        boucle principale du jeux
        
        return:
        None
        """
        # dessiner le pion actuel
        screen.fill(self.fond)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        colone = mouse_x // self.taile_plateau
        pygame.draw.circle(screen, self.j1_couleur if self.joueur_actuel == 1 else self.j2_couleur,
                        (colone * self.taile_plateau + self.taile_plateau // 2, self.taile_plateau // 2), self.rayon)

        # dessiner le plateau
        for ligne in range(self.hauteur):
            for colone in range(self.largeur):
                pygame.draw.rect(screen, self.fond, (colone * self.taile_plateau, (ligne + 1) * self.taile_plateau, self.taile_plateau, self.taile_plateau))
                pygame.draw.circle(screen, self.rond if self.plateau[ligne][colone] == 0 else (self.j1_couleur if self.plateau[ligne][colone] == 1 else self.j2_couleur),
                (colone * self.taile_plateau + self.taile_plateau // 2, (ligne + 1) * self.taile_plateau + self.taile_plateau // 2), self.rayon)

    def event(self, event: pygame.event.Event) -> bool:
        """
        S'occupe d'un seul evenement
        Renvoie si la partie est terminée
        """
        # ferme la fenetre si on appui sur le boutton croix en haut ou sur la touche echap
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # fait tomber le pion
        elif event.type == pygame.MOUSEBUTTONDOWN:
            colone = event.pos[0] // self.taile_plateau
            ligne = event.pos[1] // self.taile_plateau
            if self.placer_pion(colone):
                if self.chercher_gagnant(ligne, colone):
                    return True
                else:
                    self.changer_joueur()
        return False

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

pygame.init()
screen = pygame.display.set_mode(size=(400, 400), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()

menu = Menu()
game = ConnectFour()

MENU = False
GAME = True
current_state = MENU

while True:
    if current_state == MENU:
        for event in pygame.event.get():
            if menu.event(event):
                current_state = GAME
                print("changing state")
        menu.draw(pygame.display.get_surface())
    else:
        for event in pygame.event.get():
            if game.event(event):
                current_state = MENU
                game = ConnectFour()
        game.draw(screen)
    pygame.display.flip()
    clock.tick(30)
