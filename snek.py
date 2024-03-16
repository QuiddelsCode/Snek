import numpy as np
import tkinter as tk
import random
from enum import Enum

class direct (Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 4

class GameState:
    def __init__(self, size=45):
        # set up the board
        self.board = np.zeros((size, size))
        center = int(size / 2)
        self.board[center][center] = 3
        self.direction = direct.DOWN
        self.place_food()
        self.alive = True

    def handle_input(self, keys):
        # This takes a Set of Strings associated with keys on the keyboard
        if "w" in keys and self.direction != direct.DOWN:
            self.direction = direct.UP
        elif "a" in keys and self.direction != direct.RIGHT:
            self.direction = direct.LEFT
        elif "s" in keys and self.direction != direct.UP:
            self.direction = direct.DOWN
        elif "d" in keys and self.direction != direct.LEFT:
            self.direction = direct.RIGHT

    def place_food(self):
        # place a food marker on an empty space
        candidates = np.argwhere(self.board == 0)
        chosen = random.choice(candidates)
        x = chosen[0]
        y = chosen[1]
        self.board[(x, y)] = -1

    def game_tick(self):
        # First find the maximum entry on the board
        # (This is where the snake's "head" is located)
        head = np.unravel_index(np.argmax(self.board), self.board.shape)
        val = self.board[head]
        # Lower every cell on the board with the sanke on them by 1 as the snake moves forward
        self.board[self.board > 0] -= 1
        # find the new head position
        try:
            x, y = head
            if self.direction == direct.UP:
                y -= 1
            elif self.direction == direct.DOWN:
                y += 1
            elif self.direction == direct.LEFT:
                x -= 1
            elif self.direction == direct.RIGHT:
                x += 1
            if x < 0 or y < 0:
                self.alive = False
                return
            if self.board[(x, y)] > 0:
                self.alive = False
                return
            if self.board[(x, y)] == -1:
                # We found food, increase size of snake and place new food
                self.board[self.board > 0] += 2
                self.board[(x, y)] = val + 2
                self.place_food()
                return
            self.board[(x, y)] = val
        except IndexError:
            self.alive = False

    def print_display(self):
        # print the game state into stdout
        rows, cols = self.board.shape
        for i in range(rows):
            line = ""
            for j in range(cols):
                line += str(int(self.board[(j, i)])) + "\t"
            print(line)

if __name__ == "__main__":
    g = GameState(size=5)
    g.print_display()
    while g.alive:
        keys = input("?").split(" ")
        keys = [key.strip() for key in keys]
        g.handle_input(keys)
        g.game_tick()
        g.print_display()
        
