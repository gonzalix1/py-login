import random
import string
import hashlib
import mysql.connector
import getpass

##CONST
dbData = {"user": "root", "password": "", "host": "127.0.0.1", "database": "python"} ##Use your database config
CONN = mysql.connector.connect(user = dbData["user"], host = dbData["host"], database = dbData["database"])
CURSOR = CONN.cursor()

ADDITIONAL_SALT = "_+!ñ.,"

##FUNCTIONS
def hash_salt(salt):
    dict = {'a': 'Y', 'b': '~', 'c': '%', 'd': '=', 'e': 'a', 'f': 'H', 'g': 'x', 'h': 'R', 'i': '>', 'j': 'w', 'k': '[', 'l': 'I', 'm': 'u', 'n': '{', 'o': '#', 'p': 'V', 'q': 'A', 'r': ';', 's': '\\', 't': '*', 'u': 'f', 'v': 'g', 'w': 'm', 'x': '^', 'y': '(', 'z': 'b', 'A': '-', 'B': 's', 'C': '?', 'D': 'G', 'E': 'y', 'F': 'Z', 'G': '3', 'H': 'N', 'I': 'h', 'J': 'd', 'K': '<', 'L': '9', 'M': ',', 'N': ')', 'O': 'W', 'P': 'K', 'Q': '0', 'R': 'r', 'S': '8', 'T': 'X', 'U': 'Q', 'V': '7', 'W': '2', 'X': 'L', 'Y': 'k', 'Z': "'", '0': 'U', '1': '6', '2': 'q', '3': '5', '4': '`', '5': '_', '6': '|', '7': 'E', '8': 'D', '9': ']', '!': 'l', "'": 'O', '#': '}', '$': 'J', '%': 'p', '&': '@', '(': ':', ')': '1', '*': '!', '+': '&', ',': '4', '-': 'C', '.': 'z', '/': 'S', ':': '+', ';': 'e', '<': 'v', '=': 'c', '>': 'B', '?': 'i', '@': '/', '[': 'M', '\\': 'T', ']': '.', '^': 'o', '_': 't', '`': 'j', '{': 'F', '|': 'n', '}': '$', '~': "'", '"': 'P'}
    hashed_salt = "".join([dict.get(i) for i in salt])
    return hashed_salt


def generate_salt():
    characters = string.ascii_letters + string.digits + string.punctuation
    salt = ''.join(random.choice(characters) for _ in range(40))
    return salt


def Sha512Hash(string_to_hash):
    string_hashed = hashlib.sha512(string_to_hash.encode('utf-8')).hexdigest()
    return string_hashed





def DBInsertNewUser(user, unhashedPassword):
    salt = generate_salt()
    password = Sha512Hash(unhashedPassword+ADDITIONAL_SALT+hash_salt(salt))

    try:
        CURSOR.execute("INSERT INTO login (user, password, salt) VALUES (%s, %s, %s)", (user, password, salt))
        CONN.commit()
        main()
    except:
        CONN.rollback()
        print("Error. Try again")
        signUp()


def isUserRegistered(user):
    print("Checking if user ", user, " is registered")
    result = None
    try:
        CURSOR.execute("SELECT * FROM login WHERE user = '%s'" %user)
        result = CURSOR.fetchall()
    except:
        CONN.rollback()
    
    empty_list = [] #To check if result is an empty list or not
    return (result != empty_list), result


def doPasswordMatch(query, in_password):
    db_password = query[0][2]
    db_salt = query[0][3]
    in_password_hashed = Sha512Hash(in_password+ADDITIONAL_SALT+hash_salt(db_salt))

    if (db_password == in_password_hashed):
        LoggedIn(query)
    else:
        print("Error. Try again")
        logIn()


def signUp():
    user = input("Username: ")
    isAlreadyRegistered, _ = isUserRegistered(user)

    while (not user.isalnum()) or isAlreadyRegistered:
        if not user.isalnum():
            print("You can only use letters and numbers. Try again.")
        elif isAlreadyRegistered:
            print("That user is already in use. Try other.")
        user = input("Username: ")
        isAlreadyRegistered, _ = isUserRegistered(user)

    password = getpass.getpass("Password: ")
    while not password.isascii():
        print("You can only use ASCII characters. Try again.")
        password = input("Password: ")

    DBInsertNewUser(user, password)


def logIn():
    user = input("Username: ")
    userExists, query = isUserRegistered(user)
    while not userExists:
        print("That user is not in our database. Try again.")
        user = input("Username: ")
        userExists, query = isUserRegistered(user)

    in_password = getpass.getpass("Password: ")

    doPasswordMatch(query, in_password)

  
def LoggedIn(query):
    print("Welcome,", query[0][1] + ". Enjoy.")


def main():
    phase = int(input("0 (Sign Up) || 1 (Log In): "))
    if phase == 0:
        signUp()
    elif phase == 1:
        logIn()
    else:
        CONN.close()
        exit()  
   
main()

