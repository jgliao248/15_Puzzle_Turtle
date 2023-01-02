import os

SPLASH_SCREEN = "./Resources/splash_screen.gif"
QUIT_BUTTON = "./Resources/quitbutton.gif"
LOAD_BUTTON = "./Resources/loadbutton.gif"
RESET_BUTTON = "./Resources/resetbutton.gif"
CREDITS = "./Resources/credits.gif"
WARNING = "./Resources/file_warning.gif"
QUIT_MSG = "./Resources/quitmsg.gif"
QUIT = "./Resources/quit.gif"
WINNER = "./Resources/winner.gif"
LEADERBOARD_ERROR = "./Resources/leaderboard_error.gif"
FILE_ERROR = "../Resources/file_error.gif"
LOSE = "./Resources/Lose.gif"

BACKGROUND = "./Resources/mario_background.gif"

BUTTON_WIDTH = 80
RESET_BUTTON_HEIGHT = 80
LOAD_BUTTON_HEIGHT = 76
QUIT_BUTTON_HEIGHT = 75

if __name__ == '__main__':
    for path in os.listdir("../Resources"):
        print(path)