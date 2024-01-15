import platform
from ctypes import c_float, c_int, Structure, cdll
from ia import HUMAIN, ROBOT, Ia
from plateau import COLONNES, LIGNES, Plateau

class C_PLATEAU(Structure):
    _fields_ = [("cases", (c_int * 7) * 6)]

class C_MINMAX(Structure):
    _fields_ = [
        ("score", c_float),
        ("coup", c_int),
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
    def __init__(self):
        platform_name = platform.uname()[0]
        library_name = ""
        if platform_name == "Windows":
            library_name = "libminmax.dll"
        elif platform_name == "Linux":
            library_name = "libminmax.so"
        else:
            raise Exception("platforme non supportée")

        libminmax = cdll.LoadLibrary("ia/" + library_name)

        self.minmax = libminmax.minmax
        self.minmax.argtypes = [C_PLATEAU, c_int, c_int]
        self.minmax.restype = C_MINMAX

    def prediction(self, plateau: Plateau) -> int | None:
        p = plateau_convertion(plateau)
        # arguments: plateau, joueur, profondeur
        m = self.minmax(p, C_CASE_ROBOT, 7)
        return None if m.coup == -1 else m.coup
