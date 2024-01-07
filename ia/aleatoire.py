from ia.ia import COLONNES, Ia
import random

class Aleatoire(Ia):
    def coup_joueur(self, joueur: bool, colonne: int):
        valide = self.plateau.placer(joueur, colonne)
        assert(valide)

    def prediction(self) -> int | None:
        colonnes_valides = []
        for col in range(COLONNES):
            if self.plateau.t[0][col] == None: # vérifie que la première ligne de la colonne est vide
                colonnes_valides.append(col)

        if len(colonnes_valides) == 0:
            return None

        index_aleatoire = random.randint(0, len(colonnes_valides))
        return index_aleatoire

