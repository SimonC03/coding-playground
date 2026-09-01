# object = A "bundle" of related attributes (variables) and methods (functions)
# ex phone, book, car
# you need a "class" to create many objects

# class = (blueprint) used to design the structure and layout of an object

from car import Car

car1 = Car("Porsche", 2026, "Green", True)
car2 = Car("BMW", 2010, "Red", False)

print(car1.model)
print(car2.model)

car1.drive()
car2.stop()
car1.describe()

# Class variables = Shared among all instances of a class
#                   defined outside the constructor
#                   Allow you to share data among all objects created from that class

class Student:

    class_year = 2024
    num_students = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Student.num_students += 1 #Self kan ersättas med student1, refererar till sig själv, även Student klassen med.

student1 = Student("Spongebob", 30)
student2 = Student("Patrick", 15)
student3 = Student("Max", 24)

print(student1.name)
print(student1.age)
print(Student.class_year) # Snyggare att ta direkt från klassens variabler, än en instans

print(Student.num_students)
