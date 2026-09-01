age = int(input("Enter your age: "))

if 10 <= age <= 18:
    print("You are now signed up")

response = input("Would you like food? (Y/N): ")

if response == "Y":
    print("Have some food!")
else:
    print("No food for you!")

name = input("Enter your name: ")

if name == "":
    print("You did not type in your name!")

for_sale = True

if for_sale:
    print("This item is for sale")
else:
    print("This item is NOT for sale")