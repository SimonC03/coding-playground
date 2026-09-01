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

"""
fruits = ("apple", "orange", "banana", "coconut", "coconut")

print(fruits.count("coconut"))
# fruits.add("orange") fungerar ej då de inte kan modifieras
print(fruits)
"""

# 2D list 

"""
    
fruits = ["apple", "banaan", "coconut"]
vetegables = ["celery", "carrots"]
meats = ["chicken", "fish", "turkey"]

groceries = [fruits, vetegables, meats]

for collection in groceries:
    for food in collection:
        print(food, end=" ")
    print()

"""

# dictionary = a collection of {key:value} pairs ordered and changeable. No duplicates

"""
capitals = {"USA": "Washington D.C",
            "India": "New Delhi",
            "China": "Beijing",
            "Russia": "Moscow"}

print(capitals.get("USA")) # Ger värdet kopplat till nyckeln USA

if capitals.get("India"):
    print("Capital exists")

capitals.update({"Germany": "Berlin"})
capitals.update({"USA": "Detroit"}) #Uppdaterar befintlig nyckel om de finns
# capitals.popitem()
# capitals.clear()

keys = capitals.keys()

for key in capitals.keys():
    print(key)

values = capitals.values()

for value in capitals.values():
    print(value)

items = capitals.items()
print(items)

for key, value in capitals.items(): # Hämtar Key och Value från capitals.items() som ger en dict_items
    print(f"{key}: {value}")

"""