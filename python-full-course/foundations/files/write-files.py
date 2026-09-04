#txt

employees = ["Simon", "Alex", "Max"]

file_path = "python-full-course/foundations/files/output.txt"

try:
    with open(file_path, "x") as file:
        for employee in employees:
            file.write(employee + " ")
        print(f"txt file {file_path} was created")
except FileExistsError:
    print("That file already exists!")



employee = {
    "name": "spongebob",
    "age": 30,
    "job": "director"
}


# .json
import json

file_path = "python-full-course/foundations/files/output.csv"

try:
    with open(file_path, "w") as file:
        json.dump(employee, file, indent=4)
        print(f"txt file '{file_path}' was created")
except FileExistsError:
    print("That file already exists")

# .csv
import csv
file_path = "python-full-course/foundations/files/output.csv"

employees = [
    ["name", "Age", "job"],
    ["Patrick", 30, "Cook"],
    ["Sandy", 14, "Scientist"]
]

try:
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in employees:
            writer.writerow(row)
        print(f"csv fie '{file_path}' was created")
except FileExistsError:
    print("That file already exists!")