def happy_birthday(name, age):
    print(f"Happy birthday to {name}! You are {age} years old now.")


# for i in range(0, 23):
#    happy_birthday("Simon", i+1)

def display_invoice(username, amount, due_date):
    print(f"Hello {username}")
    print(f"Your bill of {amount}kr is due: {due_date}")

# display_invoice("Carre", 231, "01/03")

def add(number1: int, number2: int) -> float: # På denna rad är : int och -> float enbart noteringar för läsbarhet, dom gör inget
    return float(number1 + number2)

# print(type(add(1, 2)))

# Default arguments

def net_price(list_price, discount=0, tax=0.05):
    return list_price * (1 - discount) * (1 + tax)

print(net_price(500, 0.2, 10))
print(net_price(10, tax=20)) # såhär kan man skippa discount (Heter Keyword arguments)


# Keyword arguments

def hello(greeting, title, first, last):
    print(f"{greeting} {title}{first} {last}")

hello("Hello", title="Mr.", last="Simon", first="Carlén") # Kan ej vara icke keyword arguments efter en keyword argument

# for x in range(1, 11):
#    print(x, end=" ") # end är ett exempel i print funktionen

def get_phone(country, area, first, last):
    return f"{country}-{area}-{first}-{last}"

phone_num = get_phone(country=1, area=123, first=1234, last=1234)

# print(phone_num)

# args and kwargs
#  *args = allows you to pass multiple non-key arguments
#  **kwargs = allows you to pass multiple keyword arguments
#   * = unpacking operator

def add(*args): # Detta gör att man kan skicka in obegränsat många saker
    total = 0
    for arg in args:
        total += arg
    return total

# print(add(1, 2, 3, 6))


def display_name(*args):
    for arg in args:
        print(arg, end=" ")

# display_name("Simon", "dr", "mr")

def print_address(**kwargs): # Ger dict som typ
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_address(street="123 fake street", city="stockholm", zip="123 12")


def shipping_label(*args, **kwargs): # Det måste vara args före kwargs
    for arg in args:
        print(arg, end=" ")
    print()
    for value in kwargs.values():
        print(value, end=" ")

    print(f"{kwargs.get('street')}")

    print(f"{kwargs.get('city')} {kwargs.get('state')}, {kwargs.get('zip')}")

shipping_label("Dr.", "Spongebob", "Squarepants", "III", street="123 fake street", state="11121", apt="100", city="Stockholm", zip="123 12")