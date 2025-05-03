import tkinter as tk
import random
import copy

SIZE = 4
FONT = ("Verdana", 24, "bold")
TILE_COLORS = {
    0: "#ccc0b3", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
    256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
}

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")
        self.grid = [[0]*SIZE for _ in range(SIZE)]
        self.cells = []
        self.prev_state = None
        self.score = 0

        self.make_GUI()
        self.start_game()
        self.window.bind("<Key>", self.key_pressed)
        self.window.mainloop()

    def make_GUI(self):
        top_frame = tk.Frame(self.window)
        top_frame.pack()
        self.score_label = tk.Label(top_frame, text="Score: 0", font=("Verdana", 16, "bold"))
        self.score_label.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()
        tk.Button(self.button_frame, text="Restart", command=self.restart).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Undo", command=self.undo).pack(side="right", padx=10)

        grid_frame = tk.Frame(self.window, bg="#bbada0", bd=5)
        grid_frame.pack()
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                cell = tk.Label(grid_frame, text="", bg=TILE_COLORS[0],
                                width=4, height=2, font=FONT)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

    def start_game(self):
        self.add_tile()
        self.add_tile()
        self.update_GUI()

    def restart(self):
        self.grid = [[0]*SIZE for _ in range(SIZE)]
        self.score = 0
        self.prev_state = None
        self.clear_message()
        self.start_game()

    def undo(self):
        if self.prev_state:
            self.grid, self.score = self.prev_state
            self.prev_state = None
            self.update_GUI()

    def add_tile(self):
        empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_GUI(self):
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.grid[i][j]
                self.cells[i][j].configure(text=str(val) if val else "",
                                           bg=TILE_COLORS.get(val, "#3c3a32"))
        self.score_label.config(text=f"Score: {self.score}")
        if any(2048 in row for row in self.grid):
            self.show_message("You Win!")
        elif self.is_game_over():
            self.show_message("Game Over!")

    def show_message(self, text):
        self.msg_label = tk.Label(self.window, text=text, font=("Verdana", 28, "bold"),
                                  bg="#bbada0", fg="white")
        self.msg_label.pack(pady=10)
        self.window.unbind("<Key>")

    def clear_message(self):
        if hasattr(self, "msg_label"):
            self.msg_label.destroy()
            self.window.bind("<Key>", self.key_pressed)

    def key_pressed(self, event):
        key = event.keysym
        moved = False

        if key in ("Up", "Down", "Left", "Right"):
            self.prev_state = (copy.deepcopy(self.grid), self.score)

        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()

        if moved:
            self.add_tile()
            self.update_GUI()

    def compress(self, row):
        new = [i for i in row if i != 0]
        new += [0] * (SIZE - len(new))
        return new

    def merge(self, row):
        for i in range(SIZE-1):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        moved = False
        new_grid = []
        for row in self.grid:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            if final != row:
                moved = True
            new_grid.append(final)
        self.grid = new_grid
        return moved

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def move_down(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_right()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def is_game_over(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.grid[i][j] == 0:
                    return False
                if j < SIZE-1 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < SIZE-1 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        return True

if __name__ == "__main__":
    Game2048()
