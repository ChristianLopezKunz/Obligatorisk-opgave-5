import json
from socket import *

# Serverkonfiguration
serverName = "127.0.0.1"  # Localhost IP-adresse
serverPort = 12000  # Port
client = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4. SOCK_STREAM = en TCP-socket
client.connect((serverName, serverPort))  # Opretter forbindelse til serveren

# Velkomstbesked
print("Welcome to my calculator\n")

while True:
    oprnd1 = input("Enter a number: ")
    operation = input("Enter operation (+, -, *, /,random): ")
    oprnd2 = input("Enter a second number: ")

    # Opretter en JSON-anmodningsobjekt
    request = {
        "method": operation,
        "Tal1": int(oprnd1),
        "Tal2": int(oprnd2)
    }

    client.send(json.dumps(request).encode())  # encoder og sender JSON-anmodningen til serveren
    respons = client.recv(1024)  # prøver at modtage data(op til 1024 bytes)

    try:
        respons_data = json.loads(respons.decode())  # Decode, når man modtager data. JSON-respons bliver sendt over til et Python-dictionary
        if "error" in respons_data:
            print("Error:", respons_data["error"])
        else:
            print("Answer is", respons_data["result"])
    except json.JSONDecodeError:
        print("Invalid JSON response from server")

    exit_choice = input("Type 'Exit' to terminate or press Enter to continue: ")
    if exit_choice.lower() == "exit":
        break

client.close()