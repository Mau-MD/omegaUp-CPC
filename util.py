import os.path

from mosspy import moss


def get_credentials_from_file(file_name):
    """
    Reads the login credentials from the file. If they are not there, then it will ask for them and write them to the file.
    """
    if os.path.isfile(file_name):
        with open("login.txt", "r") as f:
            username = f.readline().strip()
            password = f.readline().strip()
            moss_user_id = f.readline().strip()
    else:
        username = input("Username: ")
        password = input("Password: ")
        moss_user_id = input(
            "Moss User ID: (If you don't have one, please visit https://theory.stanford.edu/~aiken/moss/)"
        )
        with open(file_name, "w") as f:
            f.write(username + "\n")
            f.write(password + "\n")
            f.write(moss_user_id + "\n")
    return username, password, moss_user_id


def print_table(rows):
    """
    Prints a table with the given columns.
    """
    col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
    total_width = sum(col_widths) + 6
    print("-" * total_width)
    for row in rows:
        print("| ", end="")
        for i in range(len(row)):
            print(str(row[i]).ljust(col_widths[i]), end=" | ")
        print("")
    print("-" * total_width)


def path_exists(*args):
    return os.path.exists(os.path.join(*args))
