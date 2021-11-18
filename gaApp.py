from tkinter import Tk, Frame, BOTH
from drawings import getBounds, getObs
from gaCanvas import GACanvas

class App(Frame):

    def __init__(self, master, bounds, obs):
        super().__init__(master)
        self.initialize(bounds, obs)

    def initialize(self, bounds, obs):
        self.master.title("2D PGA")
        self.master.geometry('800x800+0+0')
        self.master.update()
        self.pack(fill=BOTH, expand=1)
        self.canvas = GACanvas(self, bounds, obs, 10)
        self.canvas.pack(fill=BOTH, expand=1)

        self.canvas.drawObjects(0)
        self.canvas.animate()


def main(bounds, obs):
    root = Tk()
    App(root, bounds, obs)
    root.mainloop()

if __name__ == '__main__':
    main(getBounds(), getObs())
