from random import *

def tour_J(couleur, plateau):
    colonnes = [1, 2, 3, 4, 5, 6, 7]
    tour_fini_interrogation = False
    while True:
        try:
            colonne = int(input("quelle colonne ? (de 1 à 7):"))
            if colonne not in colonnes:
                print("colonne non valide")
            else:
                for ligne in range(5, -1, -1):
                    if plateau[ligne][colonne-1] == " ":
                        plateau[ligne][colonne-1] = couleur
                        return [ligne, colonne-1]
                    elif ligne==0:
                        print("N'observe donc tu pas que cette colonne est emplie de jetons ?")
        except:
            print("colonne non valide")

def tour_O(couleur, plateau):          
    tour_fini_interrogation = False
    while tour_fini_interrogation == False:
        colonne = randint(0, 6)
        for ligne in range(5, -1, -1):
            if plateau[ligne][colonne] == " ":
                plateau[ligne][colonne] = couleur
                print("L'ordi joue en ", colonne+1)
                tour_fini_interrogation = True
                break