from typing import *
import random
from src.meeple import Meeple

class Bot:

    def __init__(self) -> None:
        pass

    # chooses a black meeple that has more than 1 possible move => completly stupid bot
    def run(self, chessboard) -> Meeple:
        meeples = [meeple for row in chessboard.array for meeple in row if meeple != None and meeple.colour == "b"]

        meeple = None
        while True:
            meeple = random.choice(meeples)
            if len(meeple.possible_moves) > 0:
                break
        
        return meeple