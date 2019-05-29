from src import const

import os
import subprocess
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

    return mydb


def get_folder_from_filepath(filepath, raiseError=True):
    """
    Get the folder path from the filepath, e.g. 
    if filepath = "/xxx/yyy/zzz.txt" then the folderpath is
    /xxx/yyy.

    Inputs:
        * filepath = [str] the filepath
    """
    lastSlash = filepath.rfind("/")
    if lastSlash == -1:
        folder = filepath
    else:
        folder = filepath[:lastSlash]

    if raiseError and not os.path.isdir(folder):
        raise SystemExit("The folder `%s` doesn't exist" % folder)

    return folder


def create_user():
    """
    Will create a user with the name given in the src/const.py file.
    
    This user will be used in the rest of the program instead of the
    root user so sudo won't be required when running everytime.
    """
    # Only root can run the code
    if os.getuid() != 0:
        msg ="\n########\n"
        msg += "You need sudo permissions to run this file initially."
        msg += "\nThis is only to set up a new user for mysql and to give"
        msg += " this new user non-root permissions.\n\n"
        print(msg)
        raise SystemExit("ROOT PERMISSIONS REQUIRED\n#########")
    
    # Delete previous files
    for f in ['mysqlCreateUser', 'mysqlCreateUserSH']:
        os.remove(const.files[f])

    # Open and create the filetxt
    with open(const.files['mysqlCreateUserTemplate'], 'r') as f:
        fTxt = f.read()
        fTxt = fTxt.replace("$MYSQL_USER$", const.mysql_user)
    with open(const.files['mysqlCreateUser'], 'w') as f:
        f.write(fTxt)

    # Open and write
    with open(const.files['mysqlCreateUserSHTemplate'], 'r') as f:
        fTxt = f.read()
        fTxt = fTxt.replace("$mysqlCreateUserFile$",
                            const.files['mysqlCreateUser'])
    with open(const.files['mysqlCreateUserSH'], 'w') as f:
        f.write(fTxt)

    # Run the new bash script to create a user
    mysql_folder = get_folder_from_filepath(const.files['mysqlCreateUser'])
    os.chmod(os.path.abspath(const.files['mysqlCreateUserSH']), 755)
    os.system(const.files['mysqlCreateUserSH'])
    print("Created new mysql user named `%s'" % const.mysql_user)

    # Delete previous files
    for f in ['mysqlCreateUser', 'mysqlCreateUserSH']:
        os.remove(const.files[f])


dataBase = connect_to_db()

