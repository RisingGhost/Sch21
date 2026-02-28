import sys


def function():
    clients = [
        "andrew@gmail.com",
        "jessica@gmail.com",
        "ted@mosby.com",
        "john@snow.is",
        "bill_gates@live.com",
        "mark@facebook.com",
        "elon@paypal.com",
        "jessica@gmail.com",
    ]
    participants = [
        "walter@heisenberg.com",
        "vasily@mail.ru",
        "pinkman@yo.org",
        "jessica@gmail.com",
        "elon@paypal.com",
        "pinkman@yo.org",
        "mr@robot.gov",
        "eleven@yahoo.com",
    ]
    recipients = ["andrew@gmail.com", "jessica@gmail.com", "john@snow.is"]

    if len(sys.argv) != 2:
        raise ValueError("invalid argument count")
    elif sys.argv[1] == "call_center":
        print("Не видели рассылку:", call_center(clients, recipients))
    elif sys.argv[1] == "potential_clients":
        print("Потенциальные клиенты:", potential_clients(participants, clients))
    elif sys.argv[1] == "loyalty_program":
        print("Не участвовали в мероприятии:", loyalty_program(clients, participants))
    else:
        raise ValueError("invalid argument")


def call_center(clients, recipients):
    clients, recipients = set(clients), set(recipients)
    return list(clients - recipients)


def potential_clients(participants, clients):
    participants, clients = set(participants), set(clients)
    return list(participants - clients)


def loyalty_program(clients, participants):
    clients, participants = set(clients), set(participants)
    return list(clients - participants)


if __name__ == "__main__":
    function()
