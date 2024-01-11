from ia import ia, minmax
from time import time

ia = minmax.Minmax(ia.Plateau())

ia.coup(minmax.HUMAIN, 4)

start = time()
print(ia.prediction())
end = time()

print(f"search took {end - start}s")
