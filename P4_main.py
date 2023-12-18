from P4_def_verification import *
from P4_def_tours import *

while True:
    #On choisi le mode de jeu    
    mode_de_jeu = ["JvJ", "JvO"]
    print(mode_de_jeu)
    m_d_j = input("Quel mode de jeu ? : ")
    if m_d_j not in mode_de_jeu:
        print("entrée non valide")
    else:
        plateau = [[" " for i in range(7)] for i in range(6)]
        if m_d_j == "JvJ":
            #Donc en mode de jeu Joueur contre Joueur 
            #On appelle donc a chaque tour un Joueur a jouer
            J1 = input("nom du premier joueur :")
            J2 = input("nom du deuxième joueur :")
            for tour in range(1, 43):
                if (tour//2)!=(tour/2):
                    couleur = "x"
                    bosseman = J1
                    tour_J(couleur, plateau)

                else:
                    couleur = "o"
                    bosseman = J2
                    tour_J(couleur, plateau)

                for l in plateau:
                    print(l)
                    
                if Verification(couleur, plateau)==True:
                    print(bosseman, "a gagné")
                    break

        if m_d_j == "JvO":
            #Et donc en mode de jeu Joueur contre Ordi
            #On appelle donc le joueur a jouer un tour sur deux
            J1 = input("nom du joueur :")
            for tour in range(1, 43):
                if (tour//2)!=(tour/2):
                    couleur = "x"
                    bosseman = J1
                    tour_J(couleur, plateau)
                    
                else:
                    couleur = "o"
                    bosseman = "Monsieur Ordinateur"
                    tour_O(couleur, plateau)
                
                for l in plateau:
                    print(l)
                
                if Verification(couleur, plateau)==True:
                    print(bosseman, "a gagné")
                    break