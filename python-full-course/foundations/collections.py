# collection = single "variable" used to store multiple values
# List = [] ordered and changeable. Duplicates ok
# Set = {} unordered and immutable, but Add/Remove OK. No duplicates
# Tuple = () ordered and unchangable. Duplicates OK. FASTER

#Lists

"""

fruits = ["apple", "orange", "banana", "coconut"]

# Help functions
# print(dir(fruits))
# print(help(fruits))

# print(fruits[0:2])
print(len(fruits))

fruits[0] = "mango" # Skriver över
fruits.append("kiwi") # add to the end
fruits.remove("orange")
fruits.insert(2, "Nut")
fruits.sort()
fruits.reverse()
# fruits.clear()

print(fruits.count("mango"))

for fruit in fruits:
    print(fruit)

"""
# Sets

"""
fruits = {"apple", "orange", "banana", "coconut"}

fruits.add("pinaple")
fruits.add("coconut") # Läggs ej till då det bara kan finnas 1st
print(fruits)

"""

# Tuple

fruits = ("apple", "orange", "banana", "coconut", "coconut")

print(fruits.count("coconut"))
# fruits.add("orange") fungerar ej då de inte kan modifieras
print(fruits)