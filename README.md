README


This project is a two-player speed game created using sockets. 
The server waits for a user request to play the game, and once a connection is established, it sends a welcome message to the client.
Once two users are connected, the game commences.

The game logic is implemented on the server-side, where the server creates a random number (from 1 to 9) and sends it to player 1. 
Player 1 must type the same number and press send as fast as possible. Upon receipt, the server checks if it is correct and calculates the total Round Trip Time (RTT) from the time it sent the number until it receives the echo back. 
This is repeated for the second Player. 
The player who inputs the correct number faster wins the round and receives 1 point. Players who press the wrong number are disqualified from this round. 
This process is repeated over three rounds, and the scores for each player are displayed on the screen.

The server handles errors gracefully, for example, if a client disconnects unexpectedly. If that happens, the second client will finish the round, receive a message that the other player disconnected, and the server will close the connection.
The cumulative scores of each player are displayed after each round, and after the three rounds, the server declares the winner and closes the connection.
Each player receives a message that he has won, lost, or tied, and the connection is closed.

Thank you for playing the game!
