from src import const

import mysql.connector as connector
host = 'localhost'


def connect_to_db():
    """
    Will create a user
    """
    try:
        mydb = connector.connect(host=host,
                                 user=const.mysql_user,
                                 passwd=const.mysql_passwd)
    
    except connector.errors.ProgrammingError as e:
        create_user()
        

def create_user():
    """
    Will create a user with the name given in the src/const.py file.
    
    This user will be used in the rest of the program instead of the
    root user as sudo won't be required.
    """
    with open(const.files['sqlCreateUserTemplate'], 'r') as f:
        print(f.read())
    print("You need to create a mysql user titled: `%s`" % const.mysql_user)
    print("or change the 'mysql_user' in the src/const.py file")
    raise SystemExit("\n-------------\nMYSQL ERROR |\n-------------\n")


connect_to_db()

