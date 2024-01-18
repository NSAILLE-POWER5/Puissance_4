import pygame
import sys

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
        self.fond = (70, 100, 255)
        self.launch_hovered = False
        self.mode_hovered = False
        self.mode_ia = 0
        self.mode_text = ("Joueur contre joueur", "Joueur contre IA")

    def event(self, event: pygame.event.Event) -> bool:
        """Renvoie si le bouton de lancement a été cliqué ou non"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if self.launch_hovered:
                return True
            if self.mode_hovered:
                # boucle `mode_ia` entre 0 et 1
                self.mode_ia = (self.mode_ia + 1) % 2
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


        if LASTWINNER!=None:
            font = pygame.font.Font("interface_graphique/menu_font.ttf", 32)

            render_text= font.render("", True, (255,  255,  0), (0, 0, 255))
            if LASTWINNER=='J2':
                render_text = font.render("Vainqueur J2 ", True, (255,  255,  0), (0, 0, 255))
            elif LASTWINNER=='J1':
                render_text = font.render("Vainqueur J1 ", True, (255,  0,  0), (0, 0, 255))
            else:
                render_text = font.render("égaliter ", True, (0,  0,  0), (0, 0, 255))
            rect = render_text.get_rect()
            rect.width += 20
            rect.height += 10
            rect.center = (taille[0] // 2, taille[1] // 7)
            text_rect = render_text.get_rect(center=rect.center)
            screen.blit(render_text, text_rect)
        self.mode_hovered = draw_button(
            screen, font, self.mode_text[self.mode_ia],
            pos=(taille[0] // 2, taille[1] // 2 + 2 * taille[1] // 16),
            padding=(100, 50),
            bg_color=pygame.Color(140, 140, 140),
            hovered_color=pygame.Color(110, 110, 110),
            font_color=pygame.Color(0, 0, 0)
        )

        text_rect = render_text.get_rect(center=rect.center)
        screen.blit(render_text, text_rect)
        

class ConnectFour:
    def __init__(self):
        # les constantes du programme
        self.taille_plateau = 80
        self.rayon = self.taille_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (70, 100, 255)
        self.rond = (255, 255, 255)

        self.plateau = plateau.Plateau()
        self.joueur_actuel = plateau.JOUEUR1

        self.ia: ia.Ia | None = None

    def draw(self, screen: pygame.Surface):
        """
        boucle principale du jeu
        
        return:
        None
        """
        # dessine le pion actuel
        screen.fill(self.fond)
        mouse_x, _ = pygame.mouse.get_pos()
        colonne = mouse_x // self.taille_plateau
        pygame.draw.circle(screen, self.j1_couleur if self.joueur_actuel == plateau.JOUEUR1 else self.j2_couleur,
                        (colonne * self.taille_plateau + self.taille_plateau // 2, self.taille_plateau // 2), self.rayon)

        # dessine le plateau
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
                sound.pion()      
                colonne = event.pos[0] // self.taille_plateau
                if colonne < 0 or colonne >= plateau.COLONNES:
                    return False

                if self.plateau.placer(self.joueur_actuel, colonne):
                    if self.ia != None:
                        self.changer_joueur()
                        coup = self.ia.prediction(self.plateau)
                        if coup != None: # si coup == None, un des joueurs a gagné
                            self.plateau.placer(self.joueur_actuel, coup)

                    gagner = self.plateau.joueur_a_gagne()
                    if gagner != None:
                        print(gagner, self.joueur_actuel,"à gagner")
                        global LASTWINNER
                        if gagner:
                            LASTWINNER = 'J2'
                        else:
                            LASTWINNER='J1'
                        return True
                    elif self.plateau.tour == 42:
                        print("égalité")
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
        for event in pygame.event.get():
            if menu.event(event):
                current_state = GAME
                if menu.mode_ia == 1:
                    game.ia = minmax.Minmax()
                sound.jouer_musique_jeu(menu.mode_ia)
        menu.draw(pygame.display.get_surface())
    elif current_state == GAME:
        for event in pygame.event.get():
            if game.event(event):
                current_state = END_GAME
                end_game_ticks = 0
                sound.jouer_musique_menu()
        game.draw(screen)
    else:
        if LASTWINNER != None:
            taille = screen.get_size()
            font = pygame.font.Font("interface_graphique/menu_font.ttf", 32)

            render_text= font.render("", True, (255,  255,  0), (0, 0, 255))
            if LASTWINNER:
                render_text = font.render("Vainqueur J2 ", True, (255,  255,  0), (0, 0, 255))
            else:
                render_text = font.render("Vainqueur J1 ", True, (255,  0,  0), (0, 0, 255))
            rect = render_text.get_rect()
            rect.width += 20
            rect.height += 10
            rect.center = (taille[0] // 2, taille[1] // 7)
            text_rect = render_text.get_rect(center=rect.center)
            screen.blit(render_text, text_rect)
            pygame.display.flip()

        end_game_ticks += 1
        if end_game_ticks > 60: # 2 seconds passed
            current_state = MENU
            game = ConnectFour()
    pygame.display.flip()
    clock.tick(30)
