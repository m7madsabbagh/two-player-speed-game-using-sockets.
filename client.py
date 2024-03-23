import socket
import time

HOST = 'localhost'
PORT = 8000

# Connect to the server (done by the group edited by Mohammed)
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Failed to connect to the server.")
    exit(1)


def print_separator(): #Majd's idea
    print("-----------------------------------")

#Checking for connectivity errors (done by the group edited by Mira
try:
    welcome = client_socket.recv(1024).decode()
    print_separator()
    print(welcome)
    print_separator()
    print("\n")
except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
    
    print("Connection to the server lost unexpectedly.")
    exit(1)


# Play three rounds of the game
for i in range(3):
    #error handling
    try:
        # Receive the random number from the server
        data = client_socket.recv(1024).decode()
        if data == "Your opponent disconnected":
            print_separator()
            print(data)
            print_separator()
            client_socket.close()
            exit(0)
        # Receive the round number from the server
        print('Round', i+1)
        print_separator()
        print('Received number:', data)
    except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
        print("Connection to the server lost unexpectedly.")
        exit(1)
        
    #calculating the RTT
    start_time = time.time()
    num = input('Enter the number: ')
    end_time = time.time()
    rtt = end_time - start_time
    client_socket.send(f"{rtt}".encode())
    client_socket.send(num.encode())

    
    try: #error handling for disconnection (done by the group edited by Samer)
        scores = client_socket.recv(1024).decode()
        if scores == "Your opponent disconnected":
            print_separator()
            print(scores)
            print_separator()
            client_socket.close()
            exit(0)
        print("\nScores: ")
        print_separator()
        print(scores)
        print("\n")
    except ConnectionResetError:
        print("Connection to the server lost unexpectedly.")
        exit(1)

try:
    final_winner = client_socket.recv(1024).decode()
    print_separator()
    print(final_winner)
    print_separator()
except ConnectionResetError:
    print("Connection to the server lost unexpectedly.")
    exit(1)

# Close the connection
client_socket.close()