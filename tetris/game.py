import random
import tkinter as tk


class Painter:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = None

    def create_canvas(self, grid_size=20, grid_count=20):
        self.canvas = tk.Canvas(
            self.root,
            width=grid_size * grid_count,
            height=grid_size * grid_count,
            bg="white",
        )

    def add_canvas_to_window(self):
        if not self.canvas:
            self.create_canvas()

        self.canvas.pack()

    def start_loop(self):
        self.root.mainloop()


class Board:
    def __init__(self, grid_size=20, grid_count=20):
        self.painter = Painter()
        self.painter.create_canvas(grid_size, grid_count)
        self.painter.add_canvas_to_window()
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.canvas = self.painter.canvas


class Cube:
    def __init__(self, canvas, grid_size, x, y):
        self.canvas = canvas
        self.grid_size = grid_size
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.create_rectangle(
            self.x * self.grid_size,
            self.y * self.grid_size,
            (self.x + 1) * self.grid_size,
            (self.y + 1) * self.grid_size,
            fill="blue",
        )


class Shape:
    SHAPES = {
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "T": [(0, 0), (1, 0), (2, 0), (1, 1)],
        "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
    }

    def __init__(self, canvas, grid_size, x=0, y=0):
        self.canvas = canvas
        self.grid_size = grid_size
        self.x = x
        self.y = y
        self.shape = random.choice(list(self.SHAPES.values()))
        self.tag = f"shape_{id(self)}"

    def draw(self):
        self.canvas.delete(self.tag)
        for offset_x, offset_y in self.shape:
            self.canvas.create_rectangle(
                (self.x + offset_x) * self.grid_size,
                (self.y + offset_y) * self.grid_size,
                (self.x + offset_x + 1) * self.grid_size,
                (self.y + offset_y + 1) * self.grid_size,
                fill="blue",
                tags=self.tag,
            )

    def drop(self):
        if (
            self.y + max(y for _, y in self.shape)
            < (self.canvas.winfo_height() // self.grid_size) - 1
        ):
            self.y += 1
            self.draw()
            self.canvas.after(500, self.drop)


class Controller:
    def __init__(self, board, shape):
        self.board = board
        self.shape = shape
        self.bind_keys()

    def bind_keys(self):
        self.board.painter.root.bind("<Left>", self.move_left)
        self.board.painter.root.bind("<Right>", self.move_right)
        self.board.painter.root.bind("<Down>", self.move_down)
        self.board.painter.root.bind("<Up>", self.rotate_shape)

    def move_left(self, event):
        if self.shape.x + min(x for x, y in self.shape.shape) <= 0:
            return
        self.shape.x -= 1
        self.shape.draw()

    def move_right(self, event):
        if (
            self.shape.x + max(x for x, y in self.shape.shape)
            >= self.board.grid_count - 1
        ):
            return
        self.shape.x += 1
        self.shape.draw()

    def move_down(self, event):
        if (
            self.shape.y + max(y for x, y in self.shape.shape)
            >= self.board.grid_count - 1
        ):
            return
        self.shape.y += 1
        self.shape.draw()

    def rotate_shape(self, event):
        rotated_shape = [(y, -x) for x, y in self.shape.shape]
        if all(0 <= self.shape.x + x < self.board.grid_count for x, y in rotated_shape):
            self.shape.shape = rotated_shape
            self.shape.draw()


class Game:
    def __init__(self, grid_size=20, grid_count=20):
        self.board = Board(grid_size, grid_count)

        self.shape = Shape(self.board.canvas, grid_size, 0, 0)

        min_x = min(x for x, _ in self.shape.shape)
        max_x = max(x for x, _ in self.shape.shape)

        center_x = grid_count // 2 - (max_x - min_x + 1) // 2
        center_y = 0

        self.shape.x = center_x
        self.shape.y = center_y

        self.controller = Controller(self.board, self.shape)
        self.shape.draw()
        self.board.painter.root.update()
        self.shape.drop()
        self.board.painter.start_loop()


if __name__ == "__main__":
    game = Game()
