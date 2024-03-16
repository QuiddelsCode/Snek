import tkinter as tk
import snek

class SnekGUI (tk.Frame):
    def __init__(self, master, *args, size=45, scale=8, **kwargs):
        super().__init__(master, *args, **kwargs)
        # set some constants for later use
        self.size = size
        self.scale = scale
        self.delta = 250
        # Setting up a nice black canvas
        dim = size * scale
        self.disp = tk.Canvas(self, width=dim, height=dim, bg="black")
        self.disp.pack()
        # create and render the initial game state
        self.keys = []
        self.gs = snek.GameState(size=size)
        self.render()
        # bind the keypresses and set up the timer for the game-loop
        self.bind("<KeyPress>", self.key_down)
        self.after(self.delta, self.advance)
        
    def render(self):
        self.disp.delete("all")
        for x in range(self.size):
            for y in range(self.size):
                if self.gs.board[x, y] == 0:
                    continue
                xpos1 = x*self.scale
                ypos1 = y*self.scale
                xpos2 = (x+1)*self.scale
                ypos2 = (y+1)*self.scale
                if self.gs.board[x, y] > 0:
                    # place a piece of our snake
                    self.disp.create_rectangle(xpos1, ypos1, xpos2, ypos2,
                                               fill = "blue")
                if self.gs.board[x, y] == -1:
                    # place the food-token
                    self.disp.create_rectangle(xpos1, ypos1, xpos2, ypos2,
                                               fill = "yellow")

    def advance(self):
        self.gs.handle_input(self.keys)
        self.keys = []
        self.gs.game_tick()
        self.render()
        if self.gs.alive:
            self.after(self.delta, self.advance)

    # one function to handle each button press (use lambdas for argument)
    def key_down(self, e):
        key = e.char
        if key not in self.keys: self.keys.append(key)
                

if __name__ == "__main__":
    root = tk.Tk()
    game = SnekGUI(root)
    game.pack()
    game.focus_set()
    root.mainloop()
