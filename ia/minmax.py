from math import inf
from ia.ia import COLONNES, HUMAIN, LIGNES, ROBOT, Ia, Plateau
import copy

def evaluate(plateau: Plateau) -> float:
    valeurs = {
        2: 1.0,
        3: 5.0,
        4: 10000.0
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

    def show(self, profondeur: int = 0):
        indent = "  " * profondeur
        print(f"{indent}{self.valeur}")
        for j in range(LIGNES):
            print(indent, end="")
            for i in range(COLONNES):
                v = self.plateau.t[j][i]
                if v == HUMAIN:
                    print("X", end=" ")
                elif v == ROBOT:
                    print("O", end=" ")
                else:
                    print("`", end=" ")
            print()

        if self.feuille:
            return
        for coup, enfant in self.coups:
            print(f"{indent} coup en {coup}:")
            enfant.show(profondeur + 1)

def minmax(plateau: Plateau, joueur: bool, profondeur: int, alpha: float = -inf, beta: float = inf) -> tuple[float, list[int]]:
    """Renvoie la liste des meilleurs coups proportionellement possibles"""
    if profondeur <= 0:
        return (evaluate(plateau), [])

    if joueur == ROBOT:
        valeur = -inf
        coups = []
        for col in range(COLONNES):
            copie_plateau = copy.deepcopy(plateau)
            valide = copie_plateau.placer(joueur, col)
            if not valide:
                continue

            (valeur_enfant, coups_enfant) = minmax(copie_plateau, not joueur, profondeur - 1, alpha, beta)
            if valeur_enfant > valeur:
                valeur = valeur_enfant
                coups = [ col, *coups_enfant ]

            if valeur > beta: # arreter de rechercher ce sous-arbre
                break
            alpha = max(alpha, valeur)
        return (valeur, coups)
    else:
        valeur = inf
        coups = []
        for col in range(COLONNES):
            copie_plateau = copy.deepcopy(plateau)
            valide = copie_plateau.placer(joueur, col)
            if not valide:
                continue

            (valeur_enfant, coups_enfant) = minmax(copie_plateau, not joueur, profondeur - 1, alpha, beta)
            if valeur_enfant < valeur:
                valeur = valeur_enfant
                coups = [ col, *coups_enfant ]
            if valeur < alpha: # arreter de rechercher ce sous-arbre
                break
            beta = min(beta, valeur)
        return (valeur, coups)

class Minimax(Ia):
    def __init__(self, plateau_initial: Plateau):
        super().__init__(plateau_initial)

    def coup_joueur(self, joueur: bool, colonne: int):
        valide = self.plateau.placer(joueur, colonne)
        assert(valide)

    def prediction(self) -> int | None:
        return super().prediction()
