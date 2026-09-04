# Exception = An event that interrupts the flow of a program
#           (ZeroDivisionError, TypeError, ValueError)
#                      1/0     int("pizza")
#           1.try, 2.except, 3.finally

try:
    number = int(input("Enter a number: "))
    print(1 / number)
except ZeroDivisionError:
    print("You can't divide by zero!")
except ValueError:
    print("Enter only numbers please!")
except Exception:
    print("Something went wrong!")
finally:
    print("Do some cleanup here")

# Vissa kör except Exceptions, men de är bad practice, då de grupperar allt i ett. Bättre veta vad som gick fel.