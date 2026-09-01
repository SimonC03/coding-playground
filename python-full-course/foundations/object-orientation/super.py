# super() = function used in a child class to call methods from a parent class (superclass)

class Shape:
    def __init__(self, color, filled):
        self.color = color
        self.filled = filled

    def describe(self):
        print(f"It is {self.color} and {'filled' if self.filled else 'not filled'}")

class Circle(Shape):
    def __init__(self, color, filled, radius):
        super().__init__(color, filled)
        self.radius = radius

    def describe(self):
        print(f"It is a circle with an area of {3.14 * self.radius * self.radius} cm^2") #Method overriting, skriver över parents describe funktion.

class Square(Shape):
    def __init__(self, color, filled, width):
        super().__init__(color, filled)
        self.width = width

    def describe(self):
        print(f"Is is a square with an area of {self.width * 2} cm^2")
        super().describe()

class Triangle(Shape):
    def __init__(self, color, filled, width, heigth):
        super().__init__(color, filled)
        self.width = width
        self.heigth = heigth

circle = Circle(color="red", filled=True, radius=5)
square = Square(color="blue", filled=False, width=2)
triangle = Triangle(color="green", filled=True, width=5, heigth=2)

print(circle.radius)

circle.describe()
square.describe()