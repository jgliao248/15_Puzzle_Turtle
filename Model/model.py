"""
model.py
This file contains the logic for the fifteen puzzle game.
"""

from random import shuffle
from math import sqrt
from datetime import datetime
from Model.puzzle_validater import is_solvable


class Model:
    """
    Model
    This class contains the logic of the fifteen puzzle game. It maintains the rules of which tiles can be moved
    in the game. It tracks the number of moves that the player has made. It tracks the duration of the current game.
    """

    # data schema for storing tile location [space: tile (location)]

    def __init__(self, num_of_tiles: int) -> None:
        """
        __init__
        Initializes the Model class with the given number of tiles
        :param num_of_tiles: The number of tiles in the game in perfect integer squared values
        """

        self.validate(num_of_tiles)

        self.tiles = []
        self.num_of_tiles = num_of_tiles

        # length X length = number of tiles
        self.length = int(sqrt(self.num_of_tiles))
        self.create_board()
        self.play_count = 0
        self.time = 0

    def validate(self, num_of_tiles) -> None:
        """
        This function validates the num_of_tiles to ensure that it is a value greater than 1 and is a perfect squared
        value to construct a length by length square
        :param num_of_tiles: the number to be checked
        :return: None
        """
        if num_of_tiles < 1:
            raise ValueError("size of board cannot be less than 1")

        quotient_1 = int(sqrt(num_of_tiles))
        quotient_2 = int(num_of_tiles / quotient_1)

        # must be equal to be a perfect square
        if quotient_1 != quotient_2:
            raise ValueError("size of board must be a perfect squared value")


    def set_puzzle(self, puzzle: list[int]) -> None:
        """
        This function sets a new puzzle list
        :param puzzle: The puzzle list to be set.
        :return: None
        """
        self.tiles = puzzle

    def get_puzzle(self) -> list[int]:
        """
        This function returns a copy of the list of integers representing the puzzle.
        :return: a copy of the list of integers representing the puzzle
        """
        return self.tiles.copy()

    def create_board(self) -> None:
        """
        This creates the list of shuffled numbers that represents a solvable puzzle
        :return: None
        """

        # A puzzle is numbered 1 to n where n is a perfect square
        self.tiles = list(range(1, self.num_of_tiles + 1))
        shuffle(self.tiles)

        # keep shuffling until the list is solvable
        while not is_solvable(self.tiles) and not self.is_done():
            shuffle(self.tiles)

    def is_done(self):
        """
        Checks if the puzzle is solved
        :return: True if the puzzle is solved. False otherwise
        """
        for i in range(1, len(self.tiles) + 1):
            # need to check with -1 offset because the tiles are numbered 1 to n
            if self.tiles[i - 1] != i:
                return False
        return True

    # need to expand to count combination moves
    def get_moves(self) -> list[int]:
        # retrieve the space where the space it
        blank_space = self.tiles.index(self.num_of_tiles)

        # get the possible locations without restrictions to board dimensions

        possible_pos = [blank_space + 1, blank_space - 1, blank_space + self.length, blank_space - self.length]

        # filter illegal moves and retrieve the corresponding tile in that current position
        movable_tiles = []
        for pos in possible_pos:
            if 0 <= pos <= self.num_of_tiles - 1:
                if pos // self.length == blank_space // self.length:
                    movable_tiles.append(self.tiles[pos])
                if pos % self.length == blank_space % self.length:
                    movable_tiles.append(self.tiles[pos])

        return movable_tiles

    def move_tile(self, tile: int) -> bool:
        if tile in self.get_moves():
            # switch the positions
            tile_pos = self.tiles.index(tile)
            space_pose = self.tiles.index(self.num_of_tiles)

            self.tiles[space_pose], self.tiles[tile_pos] = tile, self.num_of_tiles
            self.play_count += 1

            if self.play_count == 1:
                self.start_timer()
            return True
        return False


    def get_play_count(self):
        return self.play_count

    def __str__(self):

        tile = 0
        puzzle_str = ""
        for i in range(self.length):
            for j in range(self.length):
                if j == 0:
                    puzzle_str = puzzle_str + str(self.tiles[tile])
                else:
                    puzzle_str = puzzle_str + "\t" + str(self.tiles[tile])
                tile += 1
            puzzle_str = puzzle_str + "\n"
        return puzzle_str

    def start_timer(self):
        self.time = datetime.now()

    def end_timer(self) -> int:

        return (datetime.now() - self.time).total_seconds()

if __name__ == "__main__":
    model = Model(4)
    puzzle1 = [
        7, 11, 4, 14,
        5, 16, 9, 15,
        8, 13, 6, 3,
        12, 1, 10, 2]

    print(model.is_solvable(puzzle1))

    puzzle2 = [
        13, 2, 10, 3,
        1, 12, 8, 4,
        5, 16, 9, 6,
        15, 14, 11, 7]

    print(model.is_solvable(puzzle2))

    puzzle3 = [
        3, 9, 1, 15,
        14, 11, 4, 6,
        13, 16, 10, 12,
        2, 7, 8, 5]

    print(model.is_solvable(puzzle3))

    puzzle4 = [
        1, 8, 2,
        9, 4, 3,
        7, 6, 5]

    print(model.is_solvable(puzzle4))
    ''' print(model)
    move = 0
    while not model.is_done():
        print(model)
        model.get_moves()
        move = int(input("enter move"))
        model.move_tile(move)
    '''
