import cv2
import sqlite3
import base64
import imageio


# Set a random global password for the program. Can easily be changed to users choice
PASSWORD = "admin123"

# Prompt user for global passoword
connect = input("What is your password? ")

while connect != PASSWORD:
    print('Please try again!')
    connect = input("What is your password? ")
    if connect.lower() == "q":
        break
# Create or connect to filesafe database
if connect == PASSWORD:
    conn = sqlite3.connect('filesafe.db')
    try:
        conn.execute('''CREATE TABLE safe
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print(
            'Your filesafe database has been created!\nWhat would you like to store in it?')
    except:
        print("You already have a filesafe database, what would you like to do with it?")

# Program interface
while True:
    print("\n" + "*"*25)
    print("Options:")
    print("q = Quit Program")
    print("o = Open a File")
    print("s = Store a File")
    print("*"*25)
    answer = input("What is your selection: ")

    if answer.lower() == "q":
        break
    if answer.lower() == "o":
        print("right away sir!")
        # retrieve and create the file
        file_type = input(
            "What is the filetype of the file you want to open?\n")
        file_name = input(
            "What is the name of the file you want to open?\n")
        FILE_ = file_name + "." + file_type

        cursor = conn.execute(
            "SELECT * FROM safe WHERE FULL_NAME=" + '"' + FILE_ + '"')

        file_string = ""
        for row in cursor:
            file_string = row[3]
        with open(FILE_, 'wb') as f_output:
            print(file_string)
            f_output.write(base64.b64decode(file_string))

    if answer.lower() == "s":
        # store file
        PATH = input(
            "Type in the full path to the file you want to store:\nExample: /Users/Desktop/myfile.png\n")

        # Types of files that can be stored in the database
        FILE_TYPES = {
            "txt": "TEXT",
            "py": "TEXT",
            "jpg": "IMAGE",
            "png": "IMAGE",
            "jpeg": "IMAGE"
        }

        # Breaks up filename and extension from the path
        file_name = PATH.split("/")
        file_name = file_name[len(file_name) - 1]
        file_string = ""

        NAME = file_name.split(".")[0]
        EXTENSION = file_name.split(".")[1]

        # Based on the extension it will determine what to do with the file
        try:
            EXTENSION = FILE_TYPES[EXTENSION]
        except:
            Exception()

        if EXTENSION == "IMAGE":
            IMAGE = cv2.imread(PATH)
            file_string = base64.b64encode(
                cv2.imencode('.jpg', IMAGE)[1]).decode()

        elif EXTENSION == "TEXT":
            file_string = open(PATH, "r").read()
            file_string = base64.b64encode(file_string)

        EXTENSION = file_name.split(".")[1]

        # Stores file into the database for later retrieval
        command = 'INSERT INTO safe (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' % (
            '"' + file_name + '"', '"' + NAME + '"', '"' + EXTENSION + '"', '"' + file_string + '"')

        conn.execute(command)
        conn.commit()
