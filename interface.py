import pygame
import sys

import sys

import plateau
import ia.minmax
tour=0

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
    rect.width += padding[0]
    rect.height += padding[1]
    rect.center = pos
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
        self.mode_hovered = False
        self.mode_ai = 1
        self.mode_text = ("Joueur contre joueur", "Joueur contre AI")

    def event(self, event: pygame.event.Event) -> bool:
        """Renvoie si le bouton de lancement a été cliqué ou non"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if self.launch_hovered:
                return True
            if self.mode_hovered:
                if self.mode_ai==1:
                    self.mode_ai-=1
                else:
                    self.mode_ai+=1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
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
            pos=(taille[0] // 2, taille[1] // 2 - taille[1] // 16),
            padding=(100, 50),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
            font_color=pygame.Color(0, 0, 0)
        )

        font = pygame.font.Font("interface_graphique/menu_font.ttf", 26)
        render_text = font.render("mode actuel :", True, (255,  255,  255), (125, 125, 125))
        rect = render_text.get_rect()
        rect.width += 20
        rect.height += 10
        rect.center = (taille[0] // 2, taille[1] // 2 + taille[1] // 16)
        text_rect = render_text.get_rect(center=rect.center)
        screen.blit(render_text, text_rect)

        self.mode_hovered = draw_button(
            screen, font, self.mode_text[self.mode_ai],
            pos=(taille[0] // 2, taille[1] // 2 + 2 * taille[1] // 16),
            padding=(100, 50),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
            font_color=pygame.Color(0, 0, 0)
        )

class ConnectFour:
    def __init__(self):
        # les constantes du programme
        self.taille_plateau = 80
        self.rayon = self.taille_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)

        self.plateau = plateau.Plateau()
        self.joueur_actuel = plateau.JOUEUR1

        #self.ia = ia.minmax.Minmax(self.plateau)

    def draw(self, screen: pygame.Surface):
        """
        boucle principale du jeux
        
        return:
        None
        """
        # dessiner le pion actuel
        screen.fill(self.fond)
        mouse_x, _ = pygame.mouse.get_pos()
        colonne = mouse_x // self.taille_plateau
        pygame.draw.circle(screen, self.j1_couleur if self.joueur_actuel == plateau.JOUEUR1 else self.j2_couleur,
                        (colonne * self.taille_plateau + self.taille_plateau // 2, self.taille_plateau // 2), self.rayon)

        # dessiner le plateau
        for ligne in range(plateau.LIGNES):
            for colonne in range(plateau.COLONNES):
                pygame.draw.rect(screen, self.fond, (colonne * self.taille_plateau, (ligne + 1) * self.taille_plateau, self.taille_plateau, self.taille_plateau))
                couleur = self.rond
                case = self.plateau.t[ligne][colonne]
                if case == plateau.JOUEUR1:
                    couleur = self.j1_couleur
                elif case == plateau.JOUEUR2:
                    couleur = self.j2_couleur
                circle_x = colonne * self.taille_plateau + self.taille_plateau // 2
                circle_y = (ligne + 1) * self.taille_plateau + self.taille_plateau // 2
                pygame.draw.circle(screen, couleur, (circle_x, circle_y), self.rayon)

    def event(self, event: pygame.event.Event) -> bool:
        """
        S'occupe d'un seul evenement
        Renvoie si la partie est terminée
        """
        # ferme la fenetre si on appuie sur le boutton croix en haut ou sur la touche echap
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # fait tomber le pion
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:      
                colonne = event.pos[0] // self.taille_plateau
                if colonne < 0 or colonne >= plateau.COLONNES:
                    return False

                if self.plateau.placer(self.joueur_actuel, colonne):
                    gagner = self.plateau.joueur_a_gagne()
                    if gagner != None:
                        print(gagner, "à gagner")
                        return True
                    elif plateau.TOUR==41:
                        print("égalité")
                        return True
                    else:
                        self.changer_joueur()
                        plateau.TOUR+=1
        return False

    def changer_joueur(self):
        """
        input:
        None
        
        change le joueur actuel
        
        return:
        None
        """
        if self.joueur_actuel == plateau.JOUEUR1:
            self.joueur_actuel = plateau.JOUEUR2
        else:
            self.joueur_actuel = plateau.JOUEUR1

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
                plateau.TOUR=0
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
