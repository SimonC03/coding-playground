import math

friends = 0
# friends = friends + 1
friends += 1

x = 3.14
y = 4
z = 5

# result = round(x)
# result = abs(y)
# result = pow(z)
# result = max(x, y, z)
# result = min(x, y, z)

# from math lib
# result = math.sqrt(x)
# result = math.ceil(x) # Always round up
# result = math.floor(x) # Always round down


print(math.pi)

radius = float(input("Enter the radius of a circle: "))

circumference = 2 * math.pi * radius
area = math.pi * pow(radius, 2)
print(f"The circumference is: {round(circumference, 2)}")
print(f"The area of the circle is: {round(area, 2)} cm^2")

a = float(input("Enter side A: "))
b = float(input("Enter side B: "))

c = math.sqrt(pow(a, 2) + pow(b, 2))
print(f"Side C = {c}")