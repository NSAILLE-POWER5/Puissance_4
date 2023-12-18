def Verification(couleur, plateau):
    for ligne in range(0, 6):
        for colonne in range(0, 4):
            if Verification_horizontale(ligne, colonne, couleur, plateau) == True:
                return True
                
    for ligne in range(0, 3):
        for colonne in range(0, 7):
            if Verification_verticale(ligne, colonne, couleur, plateau) == True:
                return True

    for ligne in range(0, 3):
        for colonne in range(0, 4):
            if Verification_diagonale_décroissante(ligne, colonne, couleur, plateau) == True:
                return True

    for ligne in range(5, 2, -1):
        for colonne in range(0, 4):
            if Verification_diagonale_croissante(ligne, colonne, couleur, plateau) == True:
                return True

def Verification_horizontale(ligne, colonne, couleur, plat, t = 0):
    if t == 4:
        return True
    if plat[ligne][colonne] != couleur:
        return False
    return Verification_horizontale(ligne, colonne+1, couleur, plat, t+1)
    
def Verification_verticale(ligne, colonne, couleur, plat, t = 0):
    if t == 4:
        return True
    if plat[ligne][colonne] != couleur:
        return False
    return Verification_verticale(ligne+1, colonne, couleur, plat, t+1)

def Verification_diagonale_décroissante(ligne, colonne, couleur, plat, t = 0):
    if t == 4:
        return True
    if plat[ligne][colonne] != couleur:
        return False
    return Verification_diagonale_décroissante(ligne+1, colonne+1, couleur, plat, t+1)

def Verification_diagonale_croissante(ligne, colonne, couleur, plat, t = 0):
    if t == 4:
        return True
    if plat[ligne][colonne] != couleur:
        return False
    return Verification_diagonale_croissante(ligne-1, colonne+1, couleur, plat, t+1)