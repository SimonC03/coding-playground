# Python file detection

import os

file_path = "python-full-course/foundations/files/text.txt"

if os.path.exists(file_path):
    print(f"The location {file_path} exists")

    if os.path.isfile(file_path):
        print("That is a file")
    elif os.path.isdir(file_path):
        print("This is a directory")
else:
    print("That location doesen't exists")