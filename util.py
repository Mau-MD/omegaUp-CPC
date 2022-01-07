import os.path


def get_credentials_from_file(file_name: str):
    """
    Reads the login credentials from the file. If they are not there, then it will ask for them and write them to the file.
    """
    if os.path.isfile(file_name):
        with open("login.txt", "r") as f:
            username = f.readline().strip()
            password = f.readline().strip()
    else:
        username = input("Username: ")
        password = input("Password: ")
        with open(file_name, "w") as f:
            f.write(username + "\n")
            f.write(password + "\n")
    return username, password


def print_table(rows: list[str]):
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
