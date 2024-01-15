from plateau import JOUEUR1, JOUEUR2, Plateau
import copy

HUMAIN = JOUEUR1
ROBOT = JOUEUR2

class Ia:
    def prediction(self, plateau: Plateau) -> int | None:
        """Renvoie l'endroit sur lequel l'IA va jouer, ou `None` si aucun coup n'est possible,
        Ne pas oublier d'appeller `coup` avec le résultat de cette fonction si il n'est pas `None`"""
        assert False, "Ia est classe de base, il faut construire une classe enfant"
