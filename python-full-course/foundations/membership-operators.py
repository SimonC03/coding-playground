# Membership operators = used to test whether a value or variable is found in a srquence (in, not in)

students = {"Spongebob", "Patrick", "Sandy"}

student = input("Enter the name of a student: ")

if student in students:
    print(f"{student} is a student")
else:
    print(f"{student} is not in student")


grades = {"Sandy": "A", "Patrick": "B", "Spongebob": "F"}

if student in grades:
    print(f"{student}'s grade is {grades[student]}")
else:
    print(f"{student} was not found!")

 # Example
 
email = "Simon@gmail.com"

if "@" in email and "." in email:
    print("Valid email")
else:
    print("Invalid email")