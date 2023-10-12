import json
from socket import *
import threading
import random

# Funktion til at håndtere klienten
def handleClient(connectionSocket, address):
    while True:
        try:
            data = connectionSocket.recv(1024)  # Modtager data fra klienten(op til 1024 bytes)
            if not data:
                break

            request = json.loads(data.decode())  # Decoder JSON-dataen til et Python-dictionary

            
            if "method" not in request or "Tal1" not in request or "Tal2" not in request:
                response = {"error": "Invalid request format"}
            else:
                method = request["method"]
                num1 = request["Tal1"]
                num2 = request["Tal2"]
                result = 0

                
                if method == "+":
                    result = num1 + num2
                elif method == "-":
                    result = num1 - num2
                elif method == "*":
                    result = num1 * num2
                elif method == "random":
                    result = random.randint(num1,num2)
                elif method == "/":
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        response = {"error": "Division by zero"}
                        connectionSocket.send(json.dumps(response).encode())
                        continue

                response = {"result": result}

            connectionSocket.send(json.dumps(response).encode())  # encoder dataen og sender den som JSON

        except json.JSONDecodeError:
            response = {"error": "Invalid JSON format"}
            connectionSocket.send(json.dumps(response).encode())

        except Exception as e:
            response = {"error": str(e)}
            connectionSocket.send(json.dumps(response).encode())

    connectionSocket.close()

# Serverkonfiguration
serverName = "127.0.0.1"  # Localhost IP-adresse
serverPort = 12000  # Port 
serverSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4. SOCK_STREAM = en TCP-socket
serverSocket.bind((serverName, serverPort))  
serverSocket.listen(5)  # Leder efter maksimal clients
print('Server is ready to listen')


while True:
    connectionSocket, addr = serverSocket.accept()  # Accepter forbindelser
    threading.Thread(target=handleClient, args=(connectionSocket, addr)).start()  # Starter en ny thread til at håndtere klienten