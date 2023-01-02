from View.border import Border
from Controller.error_logger import log_error

LEADERBOARD_PATH = "./leaderboard.txt"
MAX_NUM_LEADERS = 10
OFFSET = 20
FONT_SIZE = 36
TITLE_FONT = ('Arial', FONT_SIZE, 'normal')
ENTRY_FONT = ('Arial', FONT_SIZE // 3, 'normal')

class Leaderboard(Border):
    """
    Leaderboard
    This class is a Border turtle class that is able to parse and display previous leaderboard data of the puzzles
    """

    def __init__(self, width, height, x=0, y=0):
        """
        Initializes the Border class at (0,0)
        :param width: The width of the Leaderboard
        :param height: The height of the Leaderboard
        :param x: the center point x coordinate of the Leaderboard instance
        :param y: the center point y coordinate of the Leaderboard instance
        """
        super().__init__(width, height, x=x, y=y)

        self.puzzle_leader_data = {}
        self.load_data()

    def load_data(self) -> None:

        # each entry is stored as [puzzle name, player_name, play count, time]
        try:
            with open(LEADERBOARD_PATH, mode="r", encoding='utf-8') as raw_data:
                for entry in raw_data:
                    l = entry.split()
                    if l[0] not in self.puzzle_leader_data.keys():
                        self.puzzle_leader_data[l[0]] = []
                    # append the name
                    self.puzzle_leader_data[l[0]].append([l[1], int(l[2]), float(l[3])])
            print(self.puzzle_leader_data)
        except FileNotFoundError as err:
            print("error")
            log_error(f"{err} \t {LEADERBOARD_PATH} not found.")

    def add_entry(self, entry: list) -> None:
        print(entry)
        # ensure that the puzzle is within the data structure
        if entry[0] not in self.puzzle_leader_data.keys():
            print("new entry")
            self.puzzle_leader_data[entry[0]] = []

        # create a working copy
        current_puzzle_leaders = self.puzzle_leader_data[entry[0]].copy()

        if len(current_puzzle_leaders) == 0:
            self.puzzle_leader_data[entry[0]].append(entry[1:])
            self.export_data()
            return
        count = 0
        for leader in range(len(current_puzzle_leaders)):
            # only change the current data if it is a new record

            if current_puzzle_leaders[leader][1] >= entry[2] and current_puzzle_leaders[leader][2] >= entry[3]:
                self.puzzle_leader_data[entry[0]] = current_puzzle_leaders[:leader]
                self.puzzle_leader_data[entry[0]].append(entry[1:])
                self.puzzle_leader_data[entry[0]].extend(current_puzzle_leaders[leader:MAX_NUM_LEADERS - 1])
                self.export_data()
                return
            count += 1

        if count < 10:
            self.puzzle_leader_data[entry[0]].append(entry[1:])
            self.export_data()

    def export_data(self):
        with open(LEADERBOARD_PATH, mode="w", encoding='utf-8') as raw_data:
            for puzzle in self.puzzle_leader_data.keys():
                for entry in self.puzzle_leader_data[puzzle]:
                    raw_data.write('\t'.join([puzzle, str(entry[0]), str(entry[1]), str(round(entry[2], 2))]) + "\n")

    def show_leaderboard(self, puzzle):
        x, y = self.get_point("top-left", -OFFSET, -2 * OFFSET)
        self.setpos(x, y)
        self.write("Leaderboard", font=TITLE_FONT)
        if puzzle not in self.puzzle_leader_data.keys():
            return
        for entry in self.puzzle_leader_data[puzzle]:
            y = y - OFFSET
            self.setpos(x, y)
            text = '\t'.join([str(entry[0]), str(entry[1]), str(entry[2])])
            self.write(text, font=ENTRY_FONT)

if __name__ == '__main__':
    l = Leaderboard(10, 10)
    print(l.puzzle_leader_data)

    l.add_entry(["test", "justin", 50, 40])
    print(l.puzzle_leader_data)
    l.export_data()

