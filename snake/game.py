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


class Controller:
    def __init__(self, root):
        self.new_direction = "Right"
        self.root = root

        def handle_keypress(event):
            if event.keysym in ["Up", "Down", "Left", "Right"]:
                self.new_direction = event.keysym

        self.root.bind("<KeyPress>", handle_keypress)

    def get_direction(self):
        return self.new_direction


class Board:
    def __init__(self, grid_size, grid_count):
        self.painter = Painter()
        self.painter.create_canvas(grid_size=grid_size, grid_count=grid_count)
        self.painter.add_canvas_to_window()
        self.canvas = self.painter.canvas


class Food:
    def __init__(self, canvas, grid_size, grid_count):
        self.position = (
            random.randint(0, grid_count - 1),
            random.randint(0, grid_count - 1),
        )
        self.canvas = canvas
        self.grid_count = grid_count
        self.grid_size = grid_size
        self.draw_food()

    def draw_food(self):
        self.canvas.delete("food")
        x = self.position[0]
        y = self.position[1]

        self.canvas.create_rectangle(
            x * self.grid_size,
            y * self.grid_size,
            (x + 1) * self.grid_size,
            (y + 1) * self.grid_size,
            fill="blue",
            tags="food",
        )

    def update_food_position(self, snake_positions):
        # Keep generating random positions until one is free (not intersecting with snake)
        while True:
            new_x = random.randint(0, self.grid_count - 1)
            new_y = random.randint(0, self.grid_count - 1)
            if (new_x, new_y) not in snake_positions:
                break

        self.position = (new_x, new_y)
        self.draw_food()


class Snake:
    def __init__(self, canvas, grid_size, grid_count):
        self.positions = [(5, 5)]
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.canvas = canvas
        self.direction = "Right"
        self.draw_snake()

    def has_self_collision(self):
        # Check if the head collides with the body
        head = self.positions[0]
        return head in self.positions[1:]

    def is_colliding_with_food(self, position_of_food):
        return self.positions[0] == position_of_food

    def eat(self, eating_position):
        self.positions.append(eating_position)

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.positions:
            self.canvas.create_rectangle(
                x * self.grid_size,
                y * self.grid_size,
                (x + 1) * self.grid_size,
                (y + 1) * self.grid_size,
                fill="green",
                tags="snake",
            )

    def update_direction(self, new_direction):
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if opposites.get(new_direction) != self.direction:
            self.direction = new_direction

    def update_positions(self):
        for i in range(len(self.positions) - 1, 0, -1):
            self.positions[i] = self.positions[i - 1]

        head_x, head_y = self.positions[0]

        if self.direction == "Up":
            head_y = (head_y - 1) % self.grid_count
        elif self.direction == "Right":
            head_x = (head_x + 1) % self.grid_count
        elif self.direction == "Down":
            head_y = (head_y + 1) % self.grid_count
        elif self.direction == "Left":
            head_x = (head_x - 1) % self.grid_count

        self.positions[0] = (head_x, head_y)


class Game:
    def __init__(self, grid_size=20, grid_count=20):
        grid_count = 20
        self.board = Board(grid_size, grid_count)
        self.snake = Snake(self.board.canvas, grid_size, grid_count)
        self.food = Food(self.board.canvas, grid_size, grid_count)
        self.controller = Controller(self.board.painter.root)
        self.running = True  # New flag to stop the game on collision

        self.update_game()
        self.board.painter.start_loop()

    def update_game(self):
        if not self.running:
            self.board.canvas.create_text(
                200, 200, text="Game Over!", fill="red", font=("Helvetica", 24)
            )
            return  # Stop the game loop if collision occurs

        new_direction = self.controller.get_direction()
        self.snake.update_direction(new_direction)
        self.snake.update_positions()

        # Check for self-collision
        if self.snake.has_self_collision():
            print("GAME OVER")
            self.running = False  # Stop the game loop
            return

        self.snake.draw_snake()

        # Check if the snake eats food
        if self.snake.is_colliding_with_food(self.food.position):
            self.snake.eat(self.food.position)
            self.food.update_food_position(self.snake.positions)

        self.board.painter.root.after(200, self.update_game)


if __name__ == "__main__":
    game = Game()
