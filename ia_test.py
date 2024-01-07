from ia import ia, minmax


from time import time

p = ia.Plateau()

start = time()
print(minmax.minmax(p, ia.HUMAIN, 5))
end = time()

print(f"search took {end - start}s")
