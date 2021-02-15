class Tile:

    def __init__(self, x, y, ground_colour, meeple = None):
        self.position_x = x
        self.position_y = y
        self.ground_colour = ground_colour
        self.occupant = meeple
    
    def fieldOccupied(self):
        return True