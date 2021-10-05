import random
import string
from itertools import combinations_with_replacement
import pandas as pd
vault = []
pwd = []
diff_comb = []  # x
filtered_comb = []  # v
uc = string.ascii_uppercase
lc = string.ascii_lowercase
p = string.punctuation
d1 = string.digits


# df=pd.open('C:/Users/lenovo/PycharmProjects/Password_Management/password.'),
def password_generation(web_name, user_name, dig):
    ri = 2
    comb = combinations_with_replacement(range(1, dig + 1), 4)
    for i in comb:
        d = list(i)
        diff_comb.append(d)
    for z in range(0, len(diff_comb)):
        if sum(diff_comb[z]) == dig:
            filtered_comb.append(diff_comb[z])
    final_comb = random.choice(filtered_comb)
    for i in range(0, final_comb[0]):
        pwd1 = random.choice(uc)
        pwd.append(pwd1)
    for i in range(0, final_comb[1]):
        pwd1 = random.choice(lc)
        pwd.append(pwd1)
    for i in range(0, final_comb[2]):
        pwd1 = random.choice(p)
        pwd.append(pwd1)
    for i in range(0, final_comb[3]):
        final_pwd = random.choice(d1)
        pwd.append(final_pwd)
    random.shuffle(pwd)
    password = ""
    for ele in pwd:
        password += ele
    f = open("password.txt", "a")
    f.write("{}-{}-{}\n".format(web_name, user_name, str(password)))
    f.close()
    print(f"Here's your password: {password}")
    print("password saved succesfully")

def password_saving(web_name, user_name, dig):
    f = open("password.txt", "a")
    f.write("{}-{}-{}\n".format(web_name, user_name, str(dig)))
    f.close()
    print("password saved successfully")


def search_password():
    username_or_website = int(input("To Search password with  website name enter \'1\' or with username Enter \'2\' :" ))
    if username_or_website == 1:
        value = input("Enter website URL : ")
    if username_or_website == 2:
        value = input("Enter website username : ")
    f = open("password.txt", "r")
    for line in f:
        info = line.split("-")
        if username_or_website == 1:
            if value == info[0]:
                print(f"password: {info[2]}",end="")
                print(f"user : {info[1]}")
        elif username_or_website == 2:
            if value == info[1]:
                print(f"password: {info[2]}",end="")
                print(f"website:{info[0]}")




while True:
    print("Welcome to  password Management:")
    print('1. Generate/Save new password')
    print('2. search password')
    print('3. Password vault')

    user_choice =int(input())

    if user_choice ==1:
            print("Choose one option from below:")
            print('1. To generate Random password')
            print('2. To save existing password')
            val=int(input())
            if val==1:
                web_name = input('Enter website name : ')
                user_name = input('Enter user name :')
                dig = int(input("No digits of password required :"))
                password_generation(web_name, user_name, dig)
            if val==2:
                web_name = input('Enter website name : ')
                user_name = input('Enter user name :')
                dig = input("Enter of password :")
                password_saving(web_name, user_name, dig)

    elif user_choice == 2:
        search_password()

    elif user_choice == 3:
        f = open("password.txt", "r")
        for line in f:
            info = line.split("-")
            vault.append(info)
        df = pd.DataFrame(vault,index=None, columns=["website name","user_name","password"])
        print(df)

    else:
        print("Not a valid option")

    print("Press q to quit and c to continue")
    user_choice2 = ""
    while (user_choice2 != "c" and user_choice2 != "q"):
        user_choice2 = input()
    if user_choice2 == "q":
        exit()
    if user_choice2 == "c":
        continue