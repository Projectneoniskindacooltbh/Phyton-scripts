import tkinter as tk
import random

COLUMNS = 10
ROWS = 20
DEFAULT_CELL_SIZE = 30  # Used for initial window size only

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'L': [[1, 0, 0], [1, 1, 1]],
    'J': [[0, 0, 1], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

COLORS = {
    'I': 'cyan', 'O': 'yellow', 'T': 'purple',
    'L': 'orange', 'J': 'blue', 'S': 'green', 'Z': 'red'
}

class Tetris:
    def __init__(self, root):
        self.root = root
        self.fullscreen = False
        self.paused = False
        self.running = True

        self.canvas = tk.Canvas(root, width=COLUMNS * DEFAULT_CELL_SIZE, height=ROWS * DEFAULT_CELL_SIZE, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = None
        self.shape_pos = [0, 3]

        root.bind("<Key>", self.key_pressed)
        self.new_shape()
        self.update()

    def new_shape(self):
        self.shape_type = random.choice(list(SHAPES))
        self.current_shape = SHAPES[self.shape_type]
        self.shape_pos = [0, COLUMNS // 2 - len(self.current_shape[0]) // 2]

    def key_pressed(self, event):
        if event.keysym == "Left":
            self.move(-1)
        elif event.keysym == "Right":
            self.move(1)
        elif event.keysym == "Down":
            self.fall()
        elif event.keysym == "Up":
            self.rotate()
        elif event.keysym.lower() == "f":
            self.toggle_fullscreen()
        elif event.keysym.lower() == "p":
            self.paused = not self.paused
            self.draw()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.overrideredirect(self.fullscreen)
        self.root.attributes("-fullscreen", self.fullscreen)
        self.root.update_idletasks()

    def move(self, dx):
        self.shape_pos[1] += dx
        if not self.valid_position():
            self.shape_pos[1] -= dx

    def rotate(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.valid_position():
            self.current_shape = [list(row) for row in zip(*self.current_shape)][::-1]

    def fall(self):
        self.shape_pos[0] += 1
        if not self.valid_position():
            self.shape_pos[0] -= 1
            self.lock_shape()
            self.clear_lines()
            self.new_shape()
            if not self.valid_position():
                self.running = False
                self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                                        text="Game Over", fill="white", font=('Arial', 24))

    def valid_position(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    px, py = self.shape_pos[1] + x, self.shape_pos[0] + y
                    if px < 0 or px >= COLUMNS or py >= ROWS:
                        return False
                    if py >= 0 and self.grid[py][px] is not None:
                        return False
        return True

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    px, py = self.shape_pos[1] + x, self.shape_pos[0] + y
                    if py >= 0:
                        self.grid[py][px] = COLORS[self.shape_type]

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0, [None] * COLUMNS)
        self.grid = new_grid

    def draw(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        cell_size = min(canvas_width // COLUMNS, canvas_height // ROWS)

        x_offset = (canvas_width - cell_size * COLUMNS) // 2
        y_offset = (canvas_height - cell_size * ROWS) // 2

        for y in range(ROWS):
            for x in range(COLUMNS):
                color = self.grid[y][x]
                if color:
                    self.canvas.create_rectangle(
                        x_offset + x*cell_size, y_offset + y*cell_size,
                        x_offset + (x+1)*cell_size, y_offset + (y+1)*cell_size,
                        fill=color, outline='black'
                    )

        if self.running and not self.paused:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        px, py = self.shape_pos[1] + x, self.shape_pos[0] + y
                        if py >= 0:
                            self.canvas.create_rectangle(
                                x_offset + px*cell_size, y_offset + py*cell_size,
                                x_offset + (px+1)*cell_size, y_offset + (py+1)*cell_size,
                                fill=COLORS[self.shape_type], outline='black'
                            )

        if self.paused:
            self.canvas.create_text(canvas_width // 2, canvas_height // 2,
                                    text="Paused", fill="white", font=('Arial', 24))

    def update(self):
        if self.running and not self.paused:
            self.fall()
        self.draw()
        self.canvas.after(500, self.update)

root = tk.Tk()
root.title("Tetris")
game = Tetris(root)
root.mainloop()
