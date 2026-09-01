name = input("Enter your full name: ")

lenght = len(name)
# result = name.find(" ") # Hittar första platsen med " "
# result = name.rfind("o") # Hittar platsen för sista o
# name = name.capitalize() # Gör första bokstaven stor
name = name.upper() # Gör alla bostäder stora, motsvarighet lower
# result = name.isdigit() # True om de enbart innehåller siffror
# result = name.isalpha() # True om de enbart innehåller bokstäver
# result = name.count("s") # Räkna totalt antal s
result = name.replace("x", "s") # ersätter x med s


print(lenght)
print(result)
print(name)

print(help(str)) # Ger alla sträng operationer