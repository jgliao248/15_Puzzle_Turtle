import math
import turtle
from View.button import Button
from View.border import Border
from View.leaderboard import Leaderboard
import View.resource_file_constants as rfc
import os

# Spacing constants
WIDTH = 1000
HEIGHT = 900
PADDING = 10
BORDER = 40
GAME_AREA_LENGTH_RATIO = 0.70
SPACING = 5

# Design constants
AREA_COLOR = "#e64040"
FONT_SIZE = 50
FONT = ('Arial', FONT_SIZE, 'normal')


class View:
    def __init__(self) -> None:

        self.puz_data = None

        self.tiles = {}
        self.tile_locations = []
        self.tile_utility = None
        self.tile_size = None
        self.thumbnail_area = None
        self.control_area = None
        self.game_area = None
        self.leaderboard_area = None

        self.thumbnail_button = None
        self.quit_button = None
        self.reset_button = None
        self.load_button = None

        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)

        self.load_resources()

    def get_player_name(self) -> str:
        """
        This function prompts the user to enter their name. If no name is given, "UNKNOWN" is returned.
        :return: The name of the player.
        """
        name = turtle.textinput("Enter Name", "Your name: ")
        if name == "":
            return "UNKNOWN"
        return name


    def setup(self):
        self.screen.bgpic(rfc.BACKGROUND)
        self.draw_boarders()
        self.add_buttons()
        self.update_move_count(0, True)

    def draw_boarders(self):
        board_width = WIDTH - 2 * BORDER
        board_height = HEIGHT - 2 * BORDER
        game_area_length = board_width * GAME_AREA_LENGTH_RATIO
        self.game_area = Border(game_area_length, game_area_length)
        self.game_area.set_point((-WIDTH / 2 + BORDER + PADDING, HEIGHT / 2 - BORDER - PADDING))
        self.game_area.draw_rectangle(fillcolor=AREA_COLOR)

        thumbnail_length = board_width - (4 * PADDING + game_area_length)
        self.thumbnail_area = Border(thumbnail_length, thumbnail_length)
        self.thumbnail_area.set_point(self.game_area.get_point(point="top-right", x_offset=2 * PADDING))
        self.thumbnail_area.draw_rectangle(fillcolor=AREA_COLOR)

        control_height = board_height - (4 * PADDING + game_area_length)
        self.control_area = Border(board_width - 2 * PADDING, control_height)
        self.control_area.set_point(self.game_area.get_point(point="bottom-left", y_offset=2 * PADDING))
        self.control_area.draw_rectangle(fillcolor=AREA_COLOR)

        leaderboard_height = board_height - (6 * PADDING + control_height + thumbnail_length)
        self.leaderboard_area = Leaderboard(thumbnail_length, leaderboard_height)
        self.leaderboard_area.set_point(self.thumbnail_area.get_point(point="bottom-left", y_offset=2 * PADDING))
        self.leaderboard_area.draw_rectangle(fillcolor=AREA_COLOR)

        turtle.update()

    def load_resources(self):
        for resource in os.listdir("./Resources"):
            if ".gif" in resource:
                self.screen.addshape("./Resources/" + resource)

    def add_buttons(self):

        # get reference point of control area
        x, y = self.control_area.get_point("top-right")

        # calculate quit button position
        y = y - self.control_area.get_height() / 2
        x = x - PADDING - rfc.BUTTON_WIDTH / 2
        self.quit_button = Button(rfc.BUTTON_WIDTH, rfc.QUIT_BUTTON_HEIGHT, x, y,
                                  shape=rfc.QUIT_BUTTON, visible=False)
        self.quit_button.showturtle()
        self.quit_button.bind_function(turtle.bye)

        # calculate reset button position
        x = x - PADDING - rfc.BUTTON_WIDTH
        self.reset_button = Button(rfc.BUTTON_WIDTH, rfc.RESET_BUTTON_HEIGHT, x, y,
                                   shape=rfc.RESET_BUTTON, visible=False)
        self.reset_button.showturtle()
        self.reset_button.bind_function(self.return_home)

        # calculate load button position
        x = x - PADDING - rfc.BUTTON_WIDTH
        self.load_button = Button(rfc.BUTTON_WIDTH, rfc.LOAD_BUTTON_HEIGHT, x, y,
                                  shape=rfc.LOAD_BUTTON, visible=False)
        self.load_button.showturtle()

    def set_puzzle(self, puz_data: dict):
        self.puz_data = puz_data
        self.tile_size = puz_data["size"]
        self.tile_utility = Border(self.tile_size + SPACING / 2, self.tile_size + SPACING / 2)

        x, y = self.thumbnail_area.get_point("center")
        self.screen.addshape(self.puz_data["thumbnail"])
        self.thumbnail_button = Button(self.tile_size, self.tile_size, x, y,
                                       shape=self.puz_data["thumbnail"], visible=False)

        self.thumbnail_button.showturtle()

    def create_tile_locations(self):
        self.tile_locations = []
        x, y = self.game_area.get_point(point="top-left")

        n = int(math.sqrt(self.puz_data["number"]))

        increments = ((WIDTH - 2 * BORDER) * GAME_AREA_LENGTH_RATIO - n * self.tile_size - (n - 1) * SPACING) / 2

        x = x + increments + self.tile_size / 2
        y = y - increments - self.tile_size / 2

        for i in range(n):
            for j in range(n):
                self.tile_locations.append((x + (SPACING + self.tile_size) * j, y - (SPACING + self.tile_size) * i))

    def create_tiles(self, gameboard: list[int]):

        self.create_tile_locations()
        self.tiles = {}

        for image in range(len(gameboard)):
            x, y, = self.tile_locations[image]
            self.tile_utility.set_point((x, y), "center")
            self.tile_utility.draw_rectangle(fillcolor=None)

            if gameboard[image] == len(self.puz_data["images"].values()):
                t = Button(self.tile_size, self.tile_size, x, y, visible=False)
            else:
                self.screen.addshape(self.puz_data["images"].get(gameboard[image]))
                t = Button(self.tile_size, self.tile_size, x, y, self.puz_data["images"].get(gameboard[image]),
                           visible=False)
                t.showturtle()
            self.tiles[gameboard[image]] = t
            turtle.update()

    def return_home(self):
        for tile_num in self.tiles.keys():
            self.tiles[tile_num].setpos(*self.tile_locations[tile_num - 1])

    def update_move_count(self, count, initial=False):
        if not initial:
            self.control_area.undo()
        self.control_area.setpos(*self.control_area.get_point("top-left",
                                                              x_offset=-2 * SPACING,
                                                              y_offset=(-self.control_area.get_height() - FONT_SIZE) / 2
                                                              )
                                 )
        self.control_area.write(f"Moves: {count}", font=FONT)

    def win(self):
        self.tile_utility.setpos(0, 0)
        self.tile_utility.shape(rfc.WINNER)
        self.tile_utility.showturtle()


    def process_clicks(self, x, y, moves):
        if self.quit_button.is_clicked(x, y):
            self.quit_button.funct()
            return "quit"
        if self.load_button.is_clicked(x, y):
            self.load_button.funct()
            return "load"
        if self.reset_button.is_clicked(x, y):
            self.reset_button.funct()
            return "reset"
        if self.thumbnail_button.is_clicked(x, y):
            return "replay"
        for tile in moves:
            if self.tiles[tile].is_clicked(x, y):
                blank_x, blank_y = self.tiles[len(self.tiles)].pos()
                tile_x, tile_y = self.tiles[tile].pos()
                self.tiles[tile].goto(blank_x, blank_y)
                self.tiles[len(self.tiles)].goto(tile_x, tile_y)

                turtle.update()
                return tile
        return None


if __name__ == "__main__":
    view = View()
    view.screen.onscreenclick(view.process_clicks)

    turtle.done()
    # view.create_tiles(4)
