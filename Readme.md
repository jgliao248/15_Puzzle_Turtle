#Mario Fifteen Puzzle

## Description
This program is a Python turtle [15 puzzle game](https://en.wikipedia.org/wiki/15_puzzle). The game was written to show case the turtle library and act as a reference tool to aid students developing their own versions. At the time of creating this game, it served as a way to reinforce my understanding of some basic Python and programming concepts to help students as a teaching assistant. 

Though this is based on the 15 puzzle game, it is not limited to just 15 pieces. Other sizes of perfect squared valued grids are available (e.g. 2x2, 3x3, etc)

### Design
The program is written in a model-view-controller (MVC) design to create better separation between the game logic, user interface and the controller. Object orientated design was heavily used to develop different objects on the screen and divide smaller tasks.

The model handles the game's logic which included creating the data structure to hold the current game, move counting, and time counting. A new instance of the puzzle is created per game

The view handles user inputs by mouse clicks and is where the user actually plays the game. When a new puzzle is loaded, the view is redrawn. 

The controller handles the communication between the model and the view and dictates the flow of the program. The controller is initialized once upon the game starting.

The game is able to load new puzzles as long as a `.puz` file is created (a text file that contains the metadata and data needed to construct the puzzle) as well as all the necessary `.gif` images needed to construct the puzzle. 

The game also tracks the leaderboard for each puzzle with the player's name, number of moves made to win, and the time they took to complete the game in seconds. 

The program also has a simple error logger that identifies when a reference  file is malformed or missing.

### Challenges

Since this project is primarily utilizing the Python turtle library, this program lacks smooth animations and optimization. A major constraint of the project is to strictly use turtle and not tkinter directly. 

The major challenge with this project is the usage of the turtle library greatly limits the functionality that is available. For instance, there is no generic popup window that allows for displaying images of the puzzles and have the player select them by clicking it. 

Initially, the goal was to adapt the turtle.Screen class directly as the view but it proved to be a challenge. Since it is not simply a window class, creating a child class was difficult. 

There also appears to be some performance issues with the game when running on Apple Silicon on battery power. This is noticed by other user as well [here](https://developer.apple.com/forums/thread/695963). 

### Future Improvements 

If tkinter was available at the time of developing this program, the code would be written with that library to clean up the flow of the code. In addition, a smaller applet could be developed to allow users to select an image from their local storage and position the image (similar to setting a profile picture in social media apps) to create new puzzles. 

There are some UI improvements with the game's design could be improved upon. The current puzzles could be updated with cleaner images. The leaderboard information could be formatted better. The animations could be improved upon by making them more dynamic instead of a simple linear motion from the current position to the final position. 

## How to use

### Installation
The installation of this program only involves two steps:
- install the latest version of Python 3 (the program is written in Python 3.11)
- download the Github repository to your local drive

### Playing the game
To play the game, simply run the `main.py` file from an IDE or from the terminal. 

Once the game opens, it will prompt the player to enter their name. If no name if given, then a default "UNKNOWN" will be used instead. 
![startup](https://github.com/jgliao248/15_Puzzle_Turtle/blob/main/Readme%20Files/startup.gif)

The Mario puzzle is loaded by default. To start playing, use the mouse to click on a tile that is adjacent to the empty space. Continuously do this until the tiles match the thumbnail image to the top right of the screen. The first move of the automatically starts the timer of the game. 

If the game is won, the player's result will be processed. If the score is within the top ten of the leaderboard, it will be saved to locally. The next time the puzzle is loaded, this result will shown. The scores are ordered from least number of moves to most. If the number of moves are the same, then the score with the lower game duration in seconds is ahead. 

To replay the current game, click on the current puzzle's thumbnail. 

To load a new game, click on `load more` and type in one of the listed available puzzles. 

![load](https://github.com/jgliao248/15_Puzzle_Turtle/blob/main/Readme%20Files/load.gif)

To bring the pieces back to their correct places, press reset. The game count will remain the same. This button serves as a "cheat" to finish the puzzle quickly. 

![reset](https://github.com/jgliao248/15_Puzzle_Turtle/blob/main/Readme%20Files/reset.gif)

To quit the game, click on the `quit` button. 
