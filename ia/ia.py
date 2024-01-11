from plateau import JOUEUR1, JOUEUR2, Plateau
import copy

HUMAIN = JOUEUR1
ROBOT = JOUEUR2

class Ia:
    def __init__(self, plateau_initial: Plateau):
        self.plateau = copy.deepcopy(plateau_initial)

    def coup(self, joueur: bool, colonne: int) -> None:
        """Appeler cette fonction avec le coup effectué par un joueur pour mettre à jour l'état interne du plateau de l'IA.
        Le coup doit être valide."""
        assert False, "Ia est une classe de base, il faut construire une classe enfant"
        
    def prediction(self) -> int | None:
        """Renvoie l'endroit sur lequel l'IA va jouer, ou `None` si aucun coup n'est possible,
        Ne pas oublier d'appeller `coup` avec le résultat de cette fonction si il n'est pas `None`"""
        assert False, "Ia est classe de base, il faut construire une classe enfant"
