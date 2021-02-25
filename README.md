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
The game is split into the chessboard and a terminal on the right side.

The chessboard is setup with standard chess setup and a board description in red font. Clicking a white meeple highlights it in green and shows you possible moves for this meeple in yellow. Clicking on one of the yellow tiles moves the highlighted meeple. A red marker indicates that the king is check.
The terminal notes the moves performed by the players and has a button to start a new game. The left column is for the white players moves while the right side is for the black players moves. The notation follows the long algebraic scheme found on <a href="https://en.wikipedia.org/wiki/Chess_notation">wikipedia</a>.

When a player is losing the game, a game over screen is rendered over the chessboard. Start a new game by clicking on the new game button at terminal.

![Screenshot 2021-02-25 at 14 40 34](https://user-images.githubusercontent.com/46536619/109161501-6be64a00-7777-11eb-83bb-e3d34a4b37df.png)

![Screenshot 2021-02-25 at 14 49 46](https://user-images.githubusercontent.com/46536619/109162622-b61bfb00-7778-11eb-8338-a02fe0ef86e6.png)

![Screenshot 2021-02-25 at 14 53 02](https://user-images.githubusercontent.com/46536619/109163028-2a569e80-7779-11eb-8b4c-c159f53423e5.png)
