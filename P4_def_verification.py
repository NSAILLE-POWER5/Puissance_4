LIGNES = 6
COLONNES = 7

def vertification(ligne: int, colonne: int, plateau: list[list[bool | None]]) -> bool | None:
    """Renvoie si la position donnée est gagnante, ou `None` si aucun des deux n'ont gagné."""
    verifications = [
        ((1,  0), [(1,  0), (2,  0), (3,  0)]), # Horizontale
        ((0,  1), [(0,  1), (0,  2), (0,  3)]), # Verticale
        ((1,  1), [(1,  1), (2,  2), (3,  3)]), # Diagonale vers le bas
        ((1, -1), [(1, -1), (2, -2), (3, -3)]), # Diagonale vers le haut
    ]

    pion = plateau[ligne][colonne]
    if pion == None:
        return None

    for (direction, verif) in verifications:
        (dx, dy) = direction
        for i in range(4):
            gagne = True
            for position in verif:
                (x, y) = (position[0] + colonne - dx * i, position[1] + ligne - dy * i) 

                if not (0 <= x < COLONNES) or not (0  <= y < LIGNES): # vérifie que la position est valide
                    gagne = False
                    break
                if plateau[y][x] != pion:
                    gagne = False
                    break
            if gagne:
                return pion
    return None
