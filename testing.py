import math


Lat_EVEN = 52.25720214843750
Lat_ODD  = 52.26578017412606

dlate = 6.0
scalar = 2 ** 17

xy = math.floor(scalar * (Lat_EVEN % dlate / dlate) + 0.5)
print(xy)

#print(int(xy) & 2**17)

print(bin(10))