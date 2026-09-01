class Animal:
    def __init__(self, name):
        self.name = name
        self.is_alive = True

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    def speak(self):
        print("WOOF!")

class Car(Animal):
    def speak(self):
        print("MEEW")

class Mouse(Animal):
    pass

dog = Dog("Max")
car = Car("Tusse")
mouse = Mouse("Mickey")

print(dog.name)
dog.eat()
dog.sleep()
dog.speak()