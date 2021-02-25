### Python Chess Game
Chess implementation with pygame for local machine where you play versus a stupid bot.

### Install
Install <a href="https://github.com/pygame/pygame">pygame</a> with pip:
```sh
pip install pygame
```

### Start
```sh
python main.py
```

### The Game
The game is split into the chessboard and a terminal on the right side. The chessboard is setup with standard chess setup and a board description in red font. The terminal notes the moves performed by the players and has a button to start a new game.
![Screenshot 2021-02-25 at 14 40 34](https://user-images.githubusercontent.com/46536619/109161501-6be64a00-7777-11eb-83bb-e3d34a4b37df.png)

When a player is losing the game, a game over screen is rendered over the chessboard. Start a new game... 
![Screenshot 2021-02-25 at 14 49 46](https://user-images.githubusercontent.com/46536619/109162622-b61bfb00-7778-11eb-8338-a02fe0ef86e6.png)

Clicking a meeple highlights it in green and show you possible moves for this meeple in yellow. A red marker indicates that the king is check.
![Screenshot 2021-02-25 at 14 53 02](https://user-images.githubusercontent.com/46536619/109163028-2a569e80-7779-11eb-8b4c-c159f53423e5.png)

