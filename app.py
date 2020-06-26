import sqlite3
from user import *

conn = sqlite3.connect('.credentials.db')
c= conn.cursor()

#################################### THE LOGIN/REGISTER PAGE ####################################    

def db_contains(user_mail):
    
        try:
            c.execute("SELECT * FROM credentials WHERE email=?",(user_mail,))
            value=c.fetchone()
        except:
            value=0
        if value:
            return True
        else:
            return False
    

def get_val():

    user_mail = input("Enter your mail id : ")
    user_password = input("Enter your password : ")

    return [user_mail,user_password]

### ------------------- Registration -------------- ###

def register(user_mail,user_password):

        user = user_credentials(user_mail,user_password)
        
        if not user.email_check():
            print("Enter Valid email address")
            return

        if not user.password_check():
            print("Password is too short!")
            return

        if db_contains(user.email):
            print("User already exists!")
            return

        else:
            params = (user.email,user.password)
            c.execute(f"INSERT INTO credentials(email,password) VALUES(?,?)",params)
            uname = user.email.split('@')[0]
            print(f"Succesfully registered Welcome {uname}")
            val=-1
            c.execute("SELECT user_id FROM credentials WHERE (email=? and password=?)",params)
            value = c.fetchone()[0]

            while val!=3:
                print("1 --> enter data")
                print("2 --> display data")
                print("3 --> logout")
                val = int(input("What do you want to do next? : "))
                if val==1:
                    data_insert(value)
                elif val==2:
                    data_display(value)
                else:
                    break
            
    

### ----------------- Login ----------------- ###

def login(user_mail,user_password):
    
    user = user_credentials(user_mail,user_password)
    
    params=(user.email,user.password)
    try:
        c.execute("SELECT user_id FROM credentials WHERE (email=? and password=?)",params)
        value = c.fetchone()[0]
    except:
        value=False
    
    if value:
        uname = user_mail.split('@')[0]
        print(f"Welcome {uname}")
        data_display(value)
        
        val=-1
        while val!=3:
            print("1 --> enter data")
            print("2 --> display data")
            print("3 --> logout")
            val = int(input("What do you want to do next? : "))
            if val==1:
                data_insert(value)
            elif val==2:
                data_display(value)
            else:
                break
        
        
    else:
        print("Error Please check your credentials!!")
        return
    


########################################## THE HOME PAGE ########################################


def data_display(user_id):
    c.execute("SELECT account,username,password FROM data WHERE user_id=?",str(user_id))
    details = c.fetchall()
    if len(details)!=0:
        for detail in details:
            print("-------------------------")
            print(f"Account-{detail[0]}")
            print(f"    Username - {detail[1]}")
            print(f"    Password - {detail[2]}")
            print("-------------------------")
    else:
        print("You have no data Added")
        
def data_insert(user_id):

    data_account = input("Enter what type of account : ")
    data_username = input("Enter the username of that account : ")
    data_password = input("Enter the password of that account : ")

    params = (user_id,data_account,data_username,data_password)
    c.execute("INSERT INTO data(user_id,account,username,password) VALUES(?,?,?,?)",params)

    print("Data has been added!!")
    
def display_all_user():

    c.execute("SELECT user_id,email FROM credentials")

    user_list = c.fetchall()
    if len(user_list)>0:
        for user in user_list:
            print(f"{user[0]}. {user[1]}")
    else:
        print()
        print("--------------No users---------------")
        print()

def delete_all_users():
    c.execute("DROP TABLE credentials")
    c.execute("DROP TABLE data")


#----------------------------creating table credentials------------------------#
try:
    c.execute("""CREATE TABLE credentials(
                user_id INTEGER PRIMARY KEY,
                email text,
                password text)""")
except:
    pass

#-----------------------------creating table data-------------------------------#

try:
    c.execute("""CREATE TABLE data(
        user_id INTEGER,
        account text,
        username text,
        password text,
        FOREIGN KEY (user_id) REFERENCES credentials(user_id)
    )
    """)
except:
    pass


#-----------------------main function--------------------------#

print("##########################################")
print("########      PassKeeper          ########")
print("##########################################")
print("------all your passwords in one place-----")
val=-1

while val!=3:

    print("What do you want to do?")
    print("0 --> login")
    print("1 --> Register")
    print("2 --> Display all registered users")
    print("3 --> Delete all users")
    print("4 --> Exit")

    val=int(input("Enter response : "))
    if val==0:
        user_input = get_val()
        login(*user_input)
        val=3
    elif val==1:
        user_input = get_val()
        register(*user_input)
        val=3
    elif val==2:
        display_all_user()
    elif val==3: 
        delete_all_users()
    else:
        break

conn.commit()
conn.close()
