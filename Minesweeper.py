import random

class BoardSize:
    SMALL = (8,10)
    MEDIUM = (16,40)
    LARGE = (24,99)


class CellType:
    SAFE = 0
    MINE = -1

class MoveResult:
    CONTINUE = 0
    GAMEOVER = 1

class Minesweeper:
    def __init__(self, size):
        if size == 'S':
            self.size = BoardSize.SMALL
        elif size == 'M':
            self.size = BoardSize.MEDIUM
        else:
            self.size = BoardSize.LARGE
        self.opened = set()
        self.flagged = set()
        self.mines = set()
        self.board = [[CellType.SAFE for _ in range(self.size[0])] for _ in range(self.size[0])]
        self.generate_mines()
        self.start_game()

    def start_game(self):
        while True:
            self.print_board()
            action_str = input("Next move (O = open, F = flag e.g. \"F 1 2\"): ")
            action = action_str.split()
            if len(action) != 3:
                continue
            r, c = int(action[1]) - 1, int(action[2]) - 1

            if action[0] == 'O':
                if (r, c) not in self.opened:
                    result = self.open_cell(r, c)
                    if result == MoveResult.GAMEOVER:
                        print("\nBOOM!!! Game Over:(\n")
                        self.print_board(True)
                        break
            elif action[0] == 'F':
                if (r, c) not in self.opened and (r, c) not in self.flagged:
                    self.flagged.add((r, c))

            if self.flagged == self.mines:
                print("\n You won!")
                ""
                self.print_board()
                break

    def open_cell(self, r, c):
        if self.size[0] > r >= 0 and self.size[0] > c >= 0 and self.board[r][c] == CellType.MINE:
            return MoveResult.GAMEOVER

        if (r, c) in self.opened or r < 0 or r > self.size[0] - 1 or c < 0 or c > self.size[0] - 1 or self.board[r][c] != 0:
            self.opened.add((r, c))
            return MoveResult.CONTINUE

        self.opened.add((r, c))
        for a, b in [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]:
            self.open_cell(a, b)

    def generate_mines(self):
        for _ in range(self.size[1]):
            r, c = random.randrange(self.size[0]), random.randrange(self.size[0])
            while self.board[r][c] == CellType.MINE:
                r, c = random.randrange(self.size[0]), random.randrange(self.size[0])
            self.board[r][c] = CellType.MINE
            self.mines.add((r, c))
            # add 1 to surrounding cells
            if r > 0: self.add_mine(r - 1, c)
            if r > 0 and c > 0: self.add_mine(r - 1, c - 1)
            if r > 0 and c < self.size[0] - 1: self.add_mine(r - 1, c + 1)
            if c > 0: self.add_mine(r, c - 1)
            if c < self.size[0] - 1: self.add_mine(r, c + 1)
            if r < self.size[0] - 1 and c > 0: self.add_mine(r + 1, c - 1)
            if r < self.size[0] - 1: self.add_mine(r + 1, c)
            if r < self.size[0] - 1 and c < self.size[0] - 1: self.add_mine(r + 1, c + 1)

    def add_mine(self, r, c):
        if self.board[r][c] == CellType.MINE:
            return
        self.board[r][c] += 1

    def print_board(self, full=False):
        print("", end="    ")
        for c in range(self.size[0]):
            if c < 9:
                print(c+1, end="  ")
            else:
                print(c + 1, end=" ")
        print("\n   " + '-' * self.size[0] * 3)
        for r, row in enumerate(self.board):
            if r < 9:
                print(r+1, end=" | ")
            else:
                print(r + 1, end="| ")
            for c, cell in enumerate(row):
                if not full and (r, c) not in self.opened:
                    if (r, c) in self.flagged:
                        print("▶", end="  ")
                    else:
                        print("--", end=" ")
                else:
                    if self.board[r][c] == CellType.MINE:
                        print("☀", end="  ")
                    else:
                        print(self.board[r][c], end="  ")
            print()


def main():
    while True:
        new_game = input("\nNew game?(Y/N): ")
        if new_game == 'Y':
            difficulty = input("Choose board size (S/M/L): ")
            Minesweeper(difficulty)
        elif new_game == 'N':
            print("Thanks for playing, goodbye!")
            exit(1)


main()
