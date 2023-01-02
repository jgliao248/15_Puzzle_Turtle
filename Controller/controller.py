"""
controller.py
This file contains the Controller class that dictates the flow of the overall game.
"""
from Model.model import Model
from View.view import View
import os
from error_logger import log_error
import turtle

PUZZLES_PATH = "./Puzzles/"  # directory where the puzzle data is stored
IMAGES_PATH = "./Images/"  # directory where the puzzle data is stored


class Controller:
    """
    Controller
    This class facilitates the communication between the view and the model.
    The Controller dictates the flow of the game based on the inputs from the view and results from the model.
    """

    def __init__(self) -> None:
        """
        Initializes the Controller. The game starts with mario as the initial game
        """
        self.model = None
        self.is_playing = True

        self.puzzle_data = {}

        self.selected_puzzle = "mario"
        self.max_moves = 5  # might not need depending on the type of play
        self.get_all_puzzle_info()

        self.view = View()
        self.player_name = self.view.get_player_name()
        self.new_game(self.selected_puzzle)

    def import_meta_data(self, puzzle_meta_data: list) -> bool:
        """
        This function extracts the metadata regarding each puzzle: name, number of pieces, the size of the pieces and
        the thumbnail of the actual puzzle. It returns True if the metadata format matches. False otherwise
        :param puzzle_meta_data: The metadata of the puzzles
        :return: True if the metadata format matches. False otherwise
        """
        # print(tuple([data[0] for data in puzzle_meta_data]))
        if tuple([data[0] for data in puzzle_meta_data]) != ("name", "number", "size", "thumbnail"):
            return False
        else:
            self.puzzle_data[puzzle_meta_data[0][1]] = {"number": int(puzzle_meta_data[1][1]),
                                                        "size": int(puzzle_meta_data[2][1]),
                                                        "thumbnail": "./" + puzzle_meta_data[3][1], "images": {}}
            return True

    def import_image_data(self, puzzle_image_data, puzzle_name: str) -> None:
        """
        This function extracts all the image paths for the tile pieces from the puzzle data and the puzzle name. The
        data is kept if all the images are exists. If the data does not exist, the puzzle entry is removed from the
        main dictionary data structure that holds all the puzzle information
        :param puzzle_image_data: the raw data of all the puzzles
        :param puzzle_name: the name of the puzzle
        :return: None
        """
        # image_data is stored as [number, path]
        image_dict = {}
        count = 0
        for image_data in puzzle_image_data:
            count += 1
            image_path = f"./{image_data[1]}"
            if os.path.exists(f"./{image_data[1]}"):
                image_dict[int(image_data[0])] = image_path
            else:
                log_error(f"{FileNotFoundError} \t {image_data[1]} not found")
                # remove the entry so that it cannot be loaded
                self.puzzle_data.pop(puzzle_name)
                return

        # check to make sure num of image paths match the reported metadata 
        if count < self.puzzle_data[puzzle_name]['number'] - 1:
            self.puzzle_data.pop(puzzle_name)
            return

        self.puzzle_data[puzzle_name]["images"] = image_dict

    def open_puzzle(self, puzzle_path) -> None:
        """
        This function opens .puz files with the given path. If the file does not exist, the error is logged.
        The data is parsed and extracted to the instance's dictionary of all puzzle data
        :param puzzle_path: The path of the .puz file
        :return: None
        """
        try:
            # create  a temp list to hold data before processing
            puzzle_data_list = []
            with open(puzzle_path, mode="r", encoding="utf-8") as puzzle_file:

                for line in puzzle_file:
                    line = line.replace(":", "").split()
                    puzzle_data_list.append(line)
            # process raw data list to dictionary

            # first processing metadata regarding a puzzle
            if self.import_meta_data(puzzle_data_list[:4]):
                self.import_image_data(puzzle_data_list[4:], puzzle_data_list[0][1])

        except FileNotFoundError as err:
            log_error(f"{err} \t {puzzle_path} not found.")

    def get_all_puzzle_info(self) -> None:
        """
        This function parses all the puzzles available in the game to load the metadata
        :return: None
        """
        for path in os.listdir(PUZZLES_PATH):
            if path.find(".puz") > -1:
                self.open_puzzle(PUZZLES_PATH + path)

    def new_game(self, puzzle_name: str) -> None:
        """
        creates a new game based on the name that has been passed
        :param puzzle_name: the name of the puzzle
        :return: None
        """

        selected_puz = self.puzzle_data[puzzle_name]
        self.model = Model(selected_puz['number'])
        self.view.setup()
        self.view.leaderboard_area.show_leaderboard(puzzle_name)
        self.view.set_puzzle(selected_puz)
        self.view.create_tiles(self.model.get_puzzle())
        self.view.screen.onscreenclick(self.run)

    def set_max_moves(self, max_moves: int) -> None:
        """
        Sets the max plays for the game with the given integer
        :param max_moves: the max moves of the game
        :return: None
        """
        if max_moves < 0:
            return ValueError("the maximum number of plays must be a positive number")
        self.max_moves = max_moves

    def load_puzzle(self) -> None:
        """
        This function prompts the user with an input window to get the puzzle name to be played
        :return: None
        """
        selected_puzzle = ""  # initially set to empty sting to enter the loop
        puzzles = [puzzle_name for puzzle_name in self.puzzle_data.keys()]
        while selected_puzzle not in puzzles and selected_puzzle is not None:
            selected_puzzle = turtle.textinput("Enter puzzle name", "\n".join(puzzles))
        # case where the user enters nothing or cancels
        if selected_puzzle is None:
            return

        else:
            self.selected_puzzle = selected_puzzle
            self.is_playing = True
            self.new_game(selected_puzzle)

    def win(self):
        self.view.win()
        self.is_playing = False
        self.view.leaderboard_area.add_entry([self.selected_puzzle,
                                              self.player_name,
                                              self.model.get_play_count(),
                                              self.model.end_timer()])

    def run(self, x, y) -> None:
        """
        This function runs the game with a given x, y coordinates representing a click on the game window
        :param x: the x coordinate of the mouse click
        :param y: the y coordinate of the mouse click
        :return: None
        """

        # if the game is won, there are no moves available
        if not self.is_playing:
            moves = []
        else:
            moves = self.model.get_moves()

        command = self.view.process_clicks(x, y, moves)

        match command:
            case 'load':
                print("load pressed")
                self.load_puzzle()
            case 'reset':
                self.model.set_puzzle([x for x in range(1, self.puzzle_data[self.selected_puzzle]["number"] + 1)])
            case 'quit':
                print("quit pressed")
            case 'replay':
                self.new_game(self.selected_puzzle)
            case _:
                if command is not None:
                    self.model.move_tile(command)
                    self.view.update_move_count(self.model.get_play_count())
                    if self.model.is_done():
                        self.win()


if __name__ == "__main__":
    controller = Controller()
    turtle.done()
