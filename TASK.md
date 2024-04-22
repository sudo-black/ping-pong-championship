# Ping Pong Champiuonship

Implement a virtual Ping-Pong championship, which features n(for now 8) players and 1 referee. The 8 players will be instances of the same app, with different attributes, defined in an external file.


## The Championship
- The Referee program starts and waits for all 8 players to join the championship.
- When all players have joined, the referee draws the 4 initial games and notifies the players about their game id, opponent and their order of play (first, second).
- All games are knock-out and supervised by the referee. After all 4 games have ended, the referee informs the defeated players to shut down, draws the second round (semi finals),
informs the players about their new game id and opponents.
- In a similar fashion, the process continues to the final game and cup winner


## The game
- The game starts with the first (offensive) player picking one random number (from 1 to 10) and informing the referee about it.
- The defending player creates a defense array of random numbers (from 1 to 10). The length of the defense array is preset for each player (see players matrix at the end of this document) and defined in their individual configuration files.
- If the number picked by the offensive player does not exist in the defense array, then the player gets one point and plays again. If it exists, the defender gets the point and they switch roles (defender attacks).
- The first player to get 5 points wins the game.


## Technical Specifications
- All transactions between the referee and the players should be implemented as a REST API or via function calls.
- All 8 Players and the Referee have to run as autonomous applications; able to communicate with each other via REST API calls.
- Pay attention to the proper definition of the REST API routes, implementation, status codes etc.
- Pay attention to each player identification/authentication (during both joining and game processes).
- At the end of the championship the Referee should export a report, which lists all the games, the final scores and the Champion.

## The Players
| Player No. | Name    | Defence Set Length |
|------------|---------|--------------------|
| 1          | Eliud   | 8                  |
| 2          | Mo      | 8                  |
| 3          | Mary    | 7                  |
| 4          | Usain   | 7                  |
| 5          | Paula   | 6                  |
| 6          | Galen   | 6                  |
| 7          | Shalane | 5                  |
| 8          | Halie   | 5                  |
