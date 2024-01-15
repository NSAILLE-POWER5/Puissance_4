from ia import Ia
import random

from plateau import COLONNES, Plateau

class Aleatoire(Ia):
    def prediction(self, plateau: Plateau) -> int | None:
        colonnes_valides = []
        for col in range(COLONNES):
            if plateau.t[0][col] == None: # vérifie que la première ligne de la colonne est vide
                colonnes_valides.append(col)

        if len(colonnes_valides) == 0:
            return None

        index_aleatoire = random.randint(0, len(colonnes_valides))
        return index_aleatoire

