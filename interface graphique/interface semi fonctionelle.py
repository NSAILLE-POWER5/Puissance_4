import pygame
import sys


class ConnectFour:
    def __init__(self):
        pygame.init()
        self.largeur = 7
        self.hauteur = 6
        self.taile_plateau = 100
        self.rayon = self.taile_plateau // 2 - 5
        self.j1_couleur = (255, 0, 0)
        self.j2_couleur = (255, 255, 0)
        self.fond = (0, 0, 255)
        self.rond = (255, 255, 255)
        self.fps = 60
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.plateau = [[0] * self.largeur for _ in range(self.hauteur)]
        self.joueur_actuel = 1
        self.fin_partie = False

    def dessiner_plateau(self):
        for row in range(self.hauteur):
            for col in range(self.largeur):
                pygame.draw.rect(self.screen, self.fond, (col * self.taile_plateau, (row + 1) * self.taile_plateau, self.taile_plateau, self.taile_plateau))
                pygame.draw.circle(self.screen, self.rond if self.plateau[row][col] == 0 else (self.j1_couleur if self.plateau[row][col] == 1 else self.j2_couleur),
                (col * self.taile_plateau + self.taile_plateau // 2, (row + 1) * self.taile_plateau + self.taile_plateau // 2), self.rayon)

    def placer_pion(self, col):
        for row in range(self.hauteur - 1, -1, -1):
            if self.plateau[row][col] == 0:
                self.plateau[row][col] = self.joueur_actuel
                return True
        return False

    def chercher_gagnant(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < self.hauteur and 0 <= c < self.largeur and self.plateau[r][c] == self.joueur_actuel:
                    count += 1
                else:
                    break

            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < self.hauteur and 0 <= c < self.largeur and self.plateau[r][c] == self.joueur_actuel:
                    count += 1
                else:
                    break

            if count >= 4:
                return True

        return False

    def changer_joueur(self):
        self.joueur_actuel = 3 - self.joueur_actuel

    def run(self):
        while not self.fin_partie:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.fond, (0, 0, self.largeur * self.taile_plateau, self.taile_plateau))
                    col = event.pos[0] // self.taile_plateau
                    pygame.draw.circle(self.screen, self.j1_couleur if self.joueur_actuel == 1 else self.j2_couleur,
                                       (col * self.taile_plateau + self.taile_plateau // 2, self.taile_plateau // 2), self.rayon)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // self.taile_plateau
                    row = self.hauteur - 1 - self.plateau[self.hauteur - 1 - self.plateau[col].count(0)].count(0)
                    if self.placer_pion(col):
                        if self.chercher_gagnant(row, col):
                            print(f"Player {self.joueur_actuel} wins!")
                            self.fin_partie = True
                        else:
                            self.changer_joueur()

            self.dessiner_plateau()
            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = ConnectFour()
    game.run()