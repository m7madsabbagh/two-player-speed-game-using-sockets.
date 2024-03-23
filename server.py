import socket
import random
import time

HOST = 'localhost'
PORT = 8000

# Set up the server socket (done by the group edited by Mohammed)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

# Send a number to a client and receive a number from the client, as well as the RTT
def send_number(conn, num):  #game logic done by group edited by Majd and Samer
    # Send the number to the client
    conn.send(str(num).encode())
    rtt = float(conn.recv(1024).decode())
    # Receive the number from the client
    data = conn.recv(1024).decode()
    # Return the number received from the client and the RTT
    return rtt, data

# Handle a round of the game  
def play_round(conn1, conn2, round_num, scores):
    # Generate a random number between 1 and 9
    num = random.randint(1, 9)

    print(f"Round {round_num + 1} started.")
    # Send to client 1 & get RTT & data
    rtt1, data1 = send_number(conn1, num)
    # Send to client 2 & get RTT & data
    rtt2, data2 = send_number(conn2, num)
    
    #Print the RTT 
    print(f"Player 1 RTT: {rtt1:.4f} seconds")
    print(f"Player 2 RTT: {rtt2:.4f} seconds")

    # If both clients guessed correctly
    if str(data1) == str(num) and str(data2) == str(num):
        # If client 1 had a faster RTT
        if rtt1 < rtt2:
            scores[0] += 1
        # If client 2 had a faster RTT
        elif rtt2 < rtt1:
            scores[1] += 1
         # else both clients had the same RTT => add 1 to both scores
        else:
            scores[0] += 1
            scores[1] += 1
    # If either client guessed incorrectly
    elif str(data1) != str(num) or str(data2) != str(num):
        # If client 1 guessed incorrectly
        if str(data1) != str(num) and str(data2) == str(num):
            scores[1] += 1
        # If client 2 guessed incorrectly
        elif str(data1) == str(num) and str(data2) != str(num):
            scores[0] += 1
    # else both clients guessed incorrectly => no score change
    score1_str = f"Your score: {scores[0]}\nOpponent Score: {scores[1]}"
    score2_str = f"Your score: {scores[1]}\nOpponent Score: {scores[0]}"

    # Send scores to clients
    conn1.send(score1_str.encode())
    conn2.send(score2_str.encode())

    print(f"Round {round_num + 1} ended.")
    print()

# Handle the game
def play_game(conn1, conn2):
    # Scores
    scores = [0, 0]
    # Play three rounds of the game
    for i in range(3):
        play_round(conn1, conn2, i, scores)
    # If client 1 won
    if scores[0] > scores[1]:
        # Send win/lose messages to clients
        conn1.send("You won the game. Mabrouk!".encode())
        conn2.send("You lost the game :(".encode())
    # If client 2 won
    elif scores[1] > scores[0]:
        # Send win/lose messages to clients
        conn2.send("You won the game. Mabrouk!".encode())
        conn1.send("You lost the game :(".encode())
    # If it's a tie
    else:
        # Send tie messages to clients
        conn1.send("TIE!".encode())
        conn2.send("TIE!".encode())

welcome_str = "Welcome to the game!"


# Keep the server running (error handling done by group edited by Mira)
while True:
    try:
        # Accept connections from clients
        conn1, addr1 = server_socket.accept()
        # Send welcome message to client
        conn1.send(welcome_str.encode())
        print('Connected to', addr1)
        conn2, addr2 = server_socket.accept()
        conn2.send(welcome_str.encode())
        print('Connected to', addr2)

         # Play the game
        play_game(conn1, conn2)

        # Close the connections
        conn1.close()
        conn2.close()

    # If a client disconnects, close the connection with the other client
    # And continue to wait for new connections
    
    except Exception as e:
        print("Client disconnected")
        try:
            conn1.send("Your opponent disconnected".encode())
        except:
           

                pass
        conn1.close()
        conn2.close()
        continue