import pygame
import sys

pygame.init()

ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
image = pygame.image.load("grille.png").convert_alpha()
taille_ecran = pygame.display.get_surface().get_size()
taille_img = image.get_size()
image=pygame.transform.scale(image, (1000,  850))

difx = taille_ecran[0] - taille_img[0]
dify = taille_ecran[1] - taille_img[1]

x = difx // 2;
y = dify // 2

clock = pygame.time.Clock()
couleur = {'j1': (255, 0, 0), 'j2': (255, 255, 0)}


def place_rond(joueur, colonne, ligne):
    global couleur,x,y
    xr = colonne * ((taille_img[0] + difx) // 7) + ((taille_img[0] + difx) // 14) + x
    yr = ligne * ((taille_img[1] + dify) // 6) + ((taille_img[1] + dify) // 12) + y
    pygame.draw.circle(ecran, couleur[joueur], (xr, yr), 60)
    

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            continuer = False
        elif event.type == pygame.QUIT:
            continuer = False
    ecran.fill((255, 255, 255))
    ecran.blit(image, (x, y))
    place_rond('j1', 0, 0)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
