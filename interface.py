import pygame
import sys

from pygame.math import clamp

import ia
from ia import minmax
from sounds import Sound
import plateau
import ia.minmax

LASTWINNER = None
def draw_button(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    size: tuple[int, int],
    font_color: pygame.Color,
    bg_color: pygame.Color,
    hovered_color: pygame.Color | None = None,
    ) -> bool:
    """Renvoie si le bouton est survolé"""
    pos_x, pos_y = pos
    size_x, size_y = size

    rect = pygame.Rect(pos_x - size_x/2, pos_y - size_y/2, size_x, size_y)
    rect.center = pos
    hovered = rect_hovered(rect)
    if hovered and hovered_color != None:
        pygame.draw.rect(screen, hovered_color, rect)
    else:
        pygame.draw.rect(screen, bg_color, rect)

    render_text = font.render(text, True, font_color)
    text_rect = render_text.get_rect()
    text_rect.center = pos
    screen.blit(render_text, text_rect)

    return hovered

def rect_hovered(rect: pygame.Rect) -> bool:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.collidepoint(mouse_x, mouse_y)

def norm_width(screen_w: int, x: int) -> int:
    return x * screen_w // 1920

def norm_height(screen_h: int, x: int) -> int:
    return x * screen_h // 1080

def norm_size(screen: pygame.Surface, x: int) -> int:
    """Normalizes a given value on the width or height, whichever is smaller"""
    if screen.get_width()/1920 < screen.get_height()/1080:
        return norm_width(screen.get_width(), x)
    else:
        return norm_height(screen.get_height(), x)

def draw_winner(screen: pygame.Surface):
    screen_w, screen_h = screen.get_size()

    if LASTWINNER != None:
        font = pygame.font.Font("menu_font.ttf", norm_size(screen, 32))

        if LASTWINNER == 'J1':
            draw_button(
                screen, font, "Vainqueur J1",
                pos=(screen_w // 2, screen_h // 8), size=(norm_width(screen_w, 400), norm_height(screen_h, 48)),
                font_color=pygame.Color(255, 0, 0),
                bg_color=pygame.Color(0, 0, 255)
            )
        elif LASTWINNER == 'J2':
            draw_button(
                screen, font, "Vainqueur J2",
                pos=(screen_w // 2, screen_h // 8), size=(norm_width(screen_w, 400), norm_height(screen_h, 48)),
                font_color=pygame.Color(255, 255, 0),
                bg_color=pygame.Color(0, 0, 255)
            )
        else:
            draw_button(
                screen, font, "Egalite",
                pos=(screen_w // 2, screen_h // 8), size=(norm_width(screen_w, 400), norm_height(screen_h, 48)),
                font_color=pygame.Color(255, 255, 255),
                bg_color=pygame.Color(0, 0, 255)
            )

class Menu:
    def __init__(self):
        self.fond = (70, 100, 255)
        self.mode_ia = 0
        self.mode_text = ("Joueur contre joueur", "Joueur contre IA")
        self.difficulte_ia = 0
        self.difficulte_text = ("Facile", "Moyen", "Difficile", "Challengeur")
        self.difficulte_profondeur = (5, 8, 10, 12)
        self.premier_joueur = 0
        self.premier_joueur_texte = ("1er joueur: Humain", "1er joueur: Robot")

    def draw(self, screen: pygame.Surface) -> bool:
        """Renvoie si le bouton de lancement a été cliqué ou non"""
        screen.fill(self.fond)

        screen_w, screen_h = screen.get_size()
        def norm_w(x: int) -> int:
            return norm_width(screen_w, x)
        def norm_h(x: int) -> int:
            return norm_height(screen_h, x)
        def norm_s(x: int) -> int:
            return norm_size(screen, x)

        menu_largeur = norm_w(1200)
        menu_hauteur = norm_h(700)
        menu_rect = pygame.Rect(
            (screen_w - menu_largeur)//2,
            (screen_h - menu_hauteur)//2,
            menu_largeur,
            menu_hauteur
        )
        pygame.draw.rect(screen, (125, 125, 125), menu_rect)

        font = pygame.font.Font("menu_font.ttf", norm_s(56))
        draw_button(
            screen, font, "Puissance 4",
            pos=(screen_w // 2, screen_h // 4),
            size=(norm_w(12 * 56), norm_h(90)),
            font_color=pygame.Color(255, 255, 0),
            bg_color=pygame.Color(255, 0, 0),
        )

        font = pygame.font.Font("menu_font.ttf", norm_s(48))
        launch_hovered = draw_button(
            screen, font, "Play",
            pos=(screen_w//2 - menu_largeur//2 + norm_w(185), screen_h // 2),
            size=(norm_w(300), norm_h(80)),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
            font_color=pygame.Color(0, 0, 0)
        )

        mode_ia_x = screen_w//2 + menu_largeur//2 - norm_w(435)
        mode_hovered = draw_button(
            screen, font, self.mode_text[self.mode_ia],
            pos=(mode_ia_x, screen_h // 2),
            size=(norm_w(800), norm_h(80)),
            font_color=pygame.Color(0, 0, 0),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
        )

        def draw_indic(center_x: int, size_x: int, top_y: int, chosen_idx: int, num: int):
            for i in range(num):
                indic_rect = pygame.Rect(center_x - size_x//2 + i*size_x//num, top_y, size_x//num, norm_h(5))
                color = pygame.Color(255, 255, 255) if i == chosen_idx else pygame.Color(180, 180, 180)
                pygame.draw.rect(screen, color, indic_rect)

        draw_indic(mode_ia_x, norm_w(800), screen_h//2 + norm_h(35), self.mode_ia, 2)

        difficulte_hovered = False
        premier_joueur_hovered = False
        if self.mode_ia == 1:
            difficulte_hovered = draw_button(
                screen, font, self.difficulte_text[self.difficulte_ia],
                pos=(mode_ia_x, screen_h // 2 + norm_h(100)),
                size=(norm_w(700), norm_h(80)),
                font_color=pygame.Color(0, 0, 0),
                bg_color=pygame.Color(140, 140, 140),
                hovered_color=pygame.Color(110, 110, 110)
            )
            draw_indic(mode_ia_x, norm_w(700), screen_h//2 + norm_h(135), self.difficulte_ia, 4)

            premier_joueur_hovered = draw_button(
                screen, font, self.premier_joueur_texte[self.premier_joueur],
                pos=(mode_ia_x, screen_h // 2 + norm_h(200)),
                size=(norm_w(700), norm_h(80)),
                font_color=pygame.Color(0, 0, 0),
                bg_color=pygame.Color(140, 140, 140),
                hovered_color=pygame.Color(110, 110, 110)
            )
            draw_indic(mode_ia_x, norm_w(700), screen_h//2 + norm_h(235), self.premier_joueur, 2)

        draw_winner(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if launch_hovered:
                    return True
                if mode_hovered:
                    # boucle `mode_ia` entre 0 et 1
                    self.mode_ia = (self.mode_ia + 1) % 2
                if difficulte_hovered:
                    self.difficulte_ia = (self.difficulte_ia + 1) % 4
                if premier_joueur_hovered:
                    self.premier_joueur = (self.premier_joueur + 1) % 2
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return False
        
class ConnectFour:
    def __init__(self):
        # les constantes du programme
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (70, 100, 255)
        self.rond = (255, 255, 255)

        self.plateau = plateau.Plateau()
        self.joueur_actuel = plateau.JOUEUR1

        self.ia: ia.Ia | None = None

        # informations nécessaires communiquées entre `event` et `draw`
        self.plateau_x = 0
        self.taille_case = 0

    def draw(self, screen: pygame.Surface):
        """
        boucle principale du jeu
        
        return:
        None
        """
        largeur, hauteur = screen.get_size()

        # padding: 1/6 de la taille de chaque coté
        largeur_padde = largeur - largeur//3
        hauteur_padde = hauteur - hauteur//3

        largeur_plateau = min(largeur_padde, hauteur_padde*7 // 6)
        hauteur_plateau = min(hauteur_padde, largeur_padde*6 // 7)

        self.plateau_x = largeur // 6 + (largeur_padde - largeur_plateau) // 2 
        self.plateau_y = hauteur // 6 + (hauteur_padde - hauteur_plateau) // 2

        taille_case = largeur_plateau // 7
        self.taille_case = taille_case
        rayon = taille_case//2 - 4

        # dessine le pion actuel
        screen.fill(self.fond)
        mouse_x, _ = pygame.mouse.get_pos()

        # remap la souris de [0; largeur] à [0; plateau.COLONNES]
        mouse_x = clamp((mouse_x - self.plateau_x) // taille_case, 0, plateau.COLONNES-1)

        pygame.draw.circle(
            screen,
            self.j1_couleur if self.joueur_actuel == plateau.JOUEUR1 else self.j2_couleur,
            (self.plateau_x + mouse_x * taille_case + taille_case//2, self.plateau_y - taille_case//2),
            rayon
        )

        # dessine le plateau
        for ligne in range(plateau.LIGNES):
            for colonne in range(plateau.COLONNES):
                couleur = self.rond
                case = self.plateau.t[ligne][colonne]
                if case == plateau.JOUEUR1:
                    couleur = self.j1_couleur
                elif case == plateau.JOUEUR2:
                    couleur = self.j2_couleur

                circle_x = self.plateau_x + colonne*taille_case + taille_case//2
                circle_y = self.plateau_y + ligne*taille_case + taille_case//2
                pygame.draw.circle(screen, couleur, (circle_x, circle_y), rayon)

    def ia_place(self):
        """Place un coup si une IA est activée"""
        if self.ia != None and self.plateau.joueur_a_gagne() == None:
            self.draw(screen)
            pygame.display.flip()
            self.changer_joueur()
            coup = self.ia.prediction(self.plateau)
            if coup != None: # si coup == None, un des joueurs a gagné
                self.plateau.placer(self.joueur_actuel, coup)

    def event(self, screen: pygame.Surface, event: pygame.event.Event) -> bool:
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
                sound.pion()      
                colonne = int(clamp((event.pos[0] - self.plateau_x) // self.taille_case, 0, plateau.COLONNES))
                if colonne < 0 or colonne >= plateau.COLONNES:
                    return False

                if self.plateau.placer(self.joueur_actuel, colonne):
                    self.ia_place()

                    # éviter d'accumuler les inputs
                    pygame.event.clear()

                    global LASTWINNER
                    gagner = self.plateau.joueur_a_gagne()
                    if gagner != None:
                        if gagner:
                            LASTWINNER='J2'
                        else:
                            LASTWINNER='J1'
                        return True
                    elif self.plateau.tour == 42:
                        LASTWINNER="egalite"
                        return True
                    else:
                        self.changer_joueur()
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

MENU = 0
GAME = 1
END_GAME = 2

end_game_ticks = 0

current_state = MENU
sound = Sound()
sound.jouer_musique_menu()

while True:
    if current_state == MENU:
        if menu.draw(pygame.display.get_surface()):
            current_state = GAME
            if menu.mode_ia == 1:
                game.ia = minmax.Minmax(menu.difficulte_profondeur[menu.difficulte_ia])
                if menu.premier_joueur == 1:
                    game.ia_place()
                    game.changer_joueur()
            sound.jouer_musique_jeu(menu.mode_ia, menu.difficulte_ia)
    elif current_state == GAME:
        for event in pygame.event.get():
            if game.event(screen, event):
                current_state = END_GAME
                end_game_ticks = 0
                sound.final(game.ia, LASTWINNER)
                sound.jouer_musique_menu()
        game.draw(screen)
    else:
        draw_winner(screen)

        end_game_ticks += 1
        if end_game_ticks > 150: # 5 seconds passed
            pygame.event.clear()
            current_state = MENU
            game = ConnectFour()
    pygame.display.flip()
    clock.tick(30)
