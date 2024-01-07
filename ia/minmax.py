from math import inf
from ia.ia import COLONNES, HUMAIN, ROBOT, Ia, Plateau
import copy

def evaluate(plateau: Plateau) -> float:
    valeurs = {
        2: 1.0,
        3: 10.0,
        4: inf
    }

    score = 0
    for adjacents, valeur in valeurs.items():
        score += plateau.nombre_pions_adjacents_total(ROBOT, adjacents) * valeur
        score -= plateau.nombre_pions_adjacents_total(HUMAIN, adjacents) * valeur
    return score

class Arbre:
    def __init__(self, plateau: Plateau, joueur: bool, profondeur: int):
        self.plateau = plateau
        self.valeur = evaluate(self.plateau)
        self.coups: list[tuple[int, Arbre]] = []
        if profondeur <= 0:
            self.feuille = True
        else:
            self.feuille = False
            for i in range(COLONNES):
                plateau = copy.deepcopy(self.plateau)
                valide = plateau.placer(joueur, i)
                if valide:
                    self.coups.append((i, Arbre(plateau, not joueur, profondeur - 1)))

    def minmax(self, joueur: bool, profondeur: int) -> tuple[float, list[int]]:
        """Renvoie la liste des meilleurs coups proportionellement possibles"""
        if profondeur == 0 or self.feuille:
            return (self.valeur, [])

        if joueur == ROBOT:
            valeur = -inf
            coups = []
            for (coup, enfant) in self.coups:
                (valeur_enfant, coups_enfant) = enfant.minmax(not joueur, profondeur - 1)
                if valeur_enfant > valeur:
                    valeur = valeur_enfant
                    coups = [ coup, *coups_enfant ]
                    print(coups)
            print(coups)
            return (valeur, coups)
        else:
            valeur = inf
            coups = []
            for coup, enfant in self.coups:
                (valeur_enfant, coups_enfant) = enfant.minmax(not joueur, profondeur - 1)
                if valeur_enfant < valeur:
                    valeur = valeur_enfant
                    coups = [ coup, *coups_enfant ]
                    print(coups)
            print(coups)
            return (valeur, coups)

class Minimax(Ia):
    def __init__(self, plateau_initial: Plateau):
        super().__init__(plateau_initial)

    def coup_joueur(self, joueur: bool, colonne: int):
        valide = self.plateau.placer(joueur, colonne)
        assert(valide)

    def prediction(self) -> int | None:
        return super().prediction()
