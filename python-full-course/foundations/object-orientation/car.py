class Car:
    def __init__(self, model, year, color, for_sale): # Behövs alltid för att skapa objektet (klasserna kan läggas i egna filer)
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

    def drive(self):
        print(f"You drive the {self.model}")

    def stop(self):
        print(f"You stop the {self.model}")

    def describe(self):
        print(f"{self.year} {self.color} {self.model}")