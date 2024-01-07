from ia import ia, minmax

p = ia.Plateau()
arbre = minmax.Arbre(p, ia.HUMAIN, 3)
print(arbre.minmax(ia.HUMAIN, 3))
