import sys


def function():
    emails = open(sys.argv[1], "r")
    employees = open("employees.tsv", "w")
    employees.write(f"Name\tSurname\tEmail\n")
    for email in emails:
        name_surname = email.split("@")
        name, surname = name_surname[0].split(".")
        employees.write(f"{name.title()}\t{surname.title()}\t{email}")
    emails.close()
    employees.close()


if __name__ == "__main__":
    function()
