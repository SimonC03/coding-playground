# Typecasting = The process of converting a variable from one data type to another
# str(), int(), float(), bool()

name = "Bro Code"
age = 25
gpa = 4.9
is_student = True

gpa = int(gpa)
age = float(age)

name = bool(name)


# input() = A function that prompts the user to enter data
# Returns the entered data as a string

name = input("What is your name?: ")
age = input("How old are you?: ")

age = int(age)
age = age + 1

print(f"Hello {name}! You are {age} years old")

# Exercise 1 - Ractangle Area Calc

length = float(input("Enter the length: "))
width = float(input("Enter the width: "))

area = length * width
print(f"The area is: {area} cm2")

# Exercise 2 - Shopping Cart Program

item = input("What item would you like to buy?: ")
price = float(input("What is the price?: "))
quantity = int(input("How many would you like to buy?: "))
total = price * quantity
print(int(total))