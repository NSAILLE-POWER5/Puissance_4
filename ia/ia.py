
HUMAIN = True
ROBOT = False

LIGNES = 6
COLONNES = 7

class Plateau:
    def __init__(self):
        self.t: list[list[bool | None]] = [[None for _ in range(7)] for _ in range(6)]
    
    def placer(self, joueur: bool, colonne: int) -> bool:
        """Place un pion dans la colonne `colonne` (index commence à 0).
        Renvoie si oui ou non la case était libre."""
        ligne_max = None
        for i in range(6):
            if self.t[i][colonne] != None:
                break
            ligne_max = i
        if ligne_max == None:
            return False

        self.t[ligne_max][colonne] = joueur
        return True

    def nombre_pions_adjacents(self, ligne: int, colonne: int, joueur: bool, n: int) -> int:
        """Renvoie le nombre de lignes de longueur `n` formées avec le pion en donné."""
        verifications = [
            (1,  0), # Horizontale
            (0,  1), # Verticale
            (1,  1), # Diagonale vers le bas
            (1, -1), # Diagonale vers le haut
        ]

        num = 0
        for direction in verifications:
            (dx, dy) = direction
            for i in range(n):
                complete = True
                for position in range(n):
                    (x, y) = (colonne + dx*(position - i), ligne + dy*(position - i)) 

                    if not (0 <= x < COLONNES) or not (0  <= y < LIGNES): # vérifie que la position est valide
                        complete = False
                        break
                    if self.t[y][x] != joueur:
                        complete = False
                        break
                if complete:
                    num += 1
        return num

    def nombre_pions_adjacents_total(self, joueur: bool, n: int) -> int:
        num = 0
        for ligne in range(LIGNES):
            for colonne in range(COLONNES):
                num += self.nombre_pions_adjacents(ligne, colonne, joueur, n)
        return num

    def joueur_a_gagne(self) -> bool | None:
        """Renvoie quel joueur a gagné, ou `None` si aucun des deux n'ont gagné."""
        if self.nombre_pions_adjacents_total(HUMAIN, 4) > 0:
            return HUMAIN
        if self.nombre_pions_adjacents_total(ROBOT, 4) > 0:
            return ROBOT
        return None

class Ia:
    def __init__(self, plateau_initial: Plateau):
        self.plateau = plateau_initial

    def coup(self, joueur: bool, colonne: int):
        """Appeler cette fonction avec le coup effectué par un joueur pour mettre à jour l'état interne du plateau de l'IA.
        Le coup doit être valide."""
        assert False, "Ia est une classe de base, il faut construire une classe enfante"
        
    def prediction(self) -> int | None:
        """Renvoie l'endroit sur lequel l'IA va jouer, ou `None` si aucun coup n'est possible,
        Ne pas oublier d'appeller `coup` avec le résultat de cette fonction si il n'est pas `None`"""
        assert False, "Ia est classe de base, il faut construire une classe enfante"
