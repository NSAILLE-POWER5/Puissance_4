from ctypes import c_float, c_int, Structure, CDLL, sizeof
from ia.ia import COLONNES, HUMAIN, LIGNES, ROBOT, Ia, Plateau

class C_PLATEAU(Structure):
    _fields_ = [("cases", (c_int * 7) * 6)]

class C_MINMAX(Structure):
    _fields_ = [
        ("score", c_float),
        ("coups", c_int * 42),
        ("num_coups", c_int)
    ]

C_CASE_VIDE = 0
C_CASE_ROBOT = 1
C_CASE_HUMAIN = 2

def plateau_convertion(plateau: Plateau) -> C_PLATEAU:
    c_plateau = C_PLATEAU()
    for j in range(LIGNES):
        for i in range(COLONNES):
            case = plateau.t[j][i]
            c_case = C_CASE_VIDE
            if case == ROBOT:
                c_case = C_CASE_ROBOT
            elif case == HUMAIN:
                c_case = C_CASE_HUMAIN

            c_plateau.cases[j][i] = c_case
    return c_plateau

class Minmax(Ia):
    def __init__(self, plateau_initial: Plateau):
        super().__init__(plateau_initial)

        libminmax = CDLL("ia/libminmax.so")

        self.minmax = libminmax.minmax
        self.minmax.argtypes = [C_PLATEAU, c_int, c_int]
        self.minmax.restype = C_MINMAX

    def coup(self, joueur: bool, colonne: int):
        valide = self.plateau.placer(joueur, colonne)
        assert(valide)

    def prediction(self) -> int | None:
        p = plateau_convertion(self.plateau)
        # arguments: plateau, joueur, profondeur
        m = self.minmax(p, C_CASE_ROBOT, 7)
        assert(m.num_coups > 0)
        return m.coups[m.num_coups - 1]
