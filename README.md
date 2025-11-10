# Snakes-and-Ladders
I still haven't finished it, but you can give it a try at any time
just download the file and run main to experience the game. 
Currently, the overall playability is complete, and the details can be further optimized


Main. py (or main file):
Function: Initialize Pygame. Create a Game class instance and run the main loop. Handle all mouse inputs and state switches (menu, run, end).

constants.py:
Function: Define all fixed values such as screen size, color (such as BLACK, WHITE), chessboard size and position. For reference by other modules.


Board.by (Board class):
Function: Draw game chessboard. Store and manage the connection information between snakes and ladders. Convert logical positions (1-100) to screen pixel coordinates.


Player.py (Player class):
Function: Store the name, ID, and current location of individual players. Perform movement operations based on the number of dice points. Check and handle whether the player has stepped on a snake or ladder.


Dice.py (Dice class):
Function: Generate random numbers from 1 to 6. Draw the appearance and current point count of the dice. Handle click events in the dice area.


Chess. py (ChessManager class):
Function: Responsible for loading all chess piece images. Draw corresponding chess pieces on the screen based on player ID and coordinates.
