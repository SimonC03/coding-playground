# Class methods = Allow operations related to the class itself
#               Take (cls) as the first parameter, whitch represents the class itself.

# Instance methods = Best for operations on instances of the class (objects)
# Static methods = Best for utility functions that do not need access to class data
# Class methods = Best for class-level data or require access to the class itself

class Student:

    count = 0
    total_gpa = 0

    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
        Student.count += 1
        Student.total_gpa += gpa

    # Instance method
    def get_info(self):
        return f"{self.name} {self.gpa}"

    # Class methods
    @classmethod
    def get_count(cls):
        return f"Total # of students: {cls.count}"

    @classmethod
    def get_average_gpa(cls):
        if cls.count == 0:
            return 0
        else:
            return f"Average GPA: {cls.total_gpa / cls.count:.2f}"

student1 = Student("Simon", 4.9)
student2 = Student("Max", 4.0)

print(Student.get_count())
print(Student.get_average_gpa())


# Magic methods = Dunder methods (double underscore) __init__, __str__, __eq__
#                   They are automatically called by many of python's built-in operations
#                   They allow developers to define or custimize the behavior of objects

class Book:

    def __init__(self, title, author, num_pages):
        self.title = title
        self.author = author
        self.num_pages = num_pages

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

    def __lt__(self, other): # lt = less then
        return self.num_pages < other.num_pages

    def __gt__(self, other): # gt = greater then
        return self.num_pages > other.num_pages

    def __add__(self, other):
        return self.num_pages + other.num_pages

    def __contains__(self, keyword):
        return keyword in self.title or keyword in self.author

    def __getitem__(self, key):
        if key == "title":
            return self.title
        elif key == "author":
            return self.author
        elif key == "num_pages":
            return self.num_pages
        else:
            return f"Key {key} was not found"
        

book1 = Book("The Hobbit", "J.R.R. Tolkien", 310)
book2 = Book("Harry potter", "J.K Rowling", 223)
book3 = Book("The Lion", "C.S Lewis", 152)

print(book1)
print(book1 == book2)
print(book1 + book2)

print("Lion" in book3)
print(book1['title'])


# @property = Decorator used to define a method as a property (it can be accessed like an attribute)
#           Benefit: Add additional logic when read, write, or delete attributes
#           Gives you getter, setter and deleter method

class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return f"{self._width:.1f}cm"

    @property
    def height(self):
        return f"{self._height:.1f}cm"

    @width.setter
    def width(self, new_width):
        if new_width > 0:
            self._width = new_width
        else:
            print("Width must be greater than zero")

    @height.setter
    def height(self, new_height):
        if new_height > 0:
            self._height = new_height
        else:
            print("Height must be greater than zero")

    @width.deleter
    def width(self):
        del self._width
        print("Width has been deleted")

    @height.deleter
    def height(self):
        del self._height
        print("height has been deleted")


rectangle = Rectangle(3, 4)
rectangle.width = 0

del rectangle.width
del rectangle.height

print(rectangle.width)
print(rectangle.height)