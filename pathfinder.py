import tkinter as tk
import numpy as np
import time


class App:

    def __init__(self):
        self.rows = 20
        self.columns = 20
        self.cell_size = 20
        self.phase = 0
        self.condition = True
        self.barrier = set()
        self.start_point = None
        self.end_point = None
        self.root = tk.Tk()
        self.root.title("Pathfinding algorithms by Ante Culo")
        self.root.configure(bg="gray9")
        self.cursor = False
        self.create_ui()
        self.create_field()
        self.root.mainloop()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.columns*self.cell_size,
                                height=self.rows*self.cell_size, bd=0, highlightthickness=0)
        self.root.bind("<p>", lambda event: self.change_phase())
        self.root.bind("<space>", lambda event: self.set_cursor())
        self.instruction = tk.Label(self.root, text="Press space to enable/disable cursor,"
                                    + "\nRight-click to deselect", bg="gray9", fg="white")
        self.phase_status = tk.Label(self.root, text="Disabled cursor", fg="red", bg="gray9")
        self.next_label = tk.Label(self.root, text="Press \"P\" when done", fg="white", bg="gray9")
        self.current = tk.Label(self.root, text="")
        self.instruction.pack()
        self.phase_status.pack()
        self.canvas.pack(padx=10)
        self.next_label.pack()
        self.current.pack()

    def create_field(self):
        y = 0
        for i in range(self.rows):
            x = 0
            for j in range(self.columns):
                name = "i" + str(i) + "j" + str(j)
                cell = self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                    tag=name, fill="gray25")
                self.canvas.tag_bind(cell, "<Enter>", lambda event, arg=name: self.add_barrier(arg))
                self.canvas.tag_bind(cell, "<1>", lambda event, arg=name: self.left_click(arg))
                self.canvas.tag_bind(cell, "<3>", lambda event, arg=name: self.right_click(arg))
                x += self.cell_size
            y += self.cell_size

    def to_number(self, str):
        i = int(str[str.find("i") + 1:str.find("j")])
        j = int(str[str.find("j") + 1:])
        number = i * self.columns + j
        return number

    def to_str(self, num):
        return "i" + str(num // self.columns) + "j" + str(num % self.columns)

    def change_phase(self):
        if self.condition:
            self.phase += 1
            self.condition = False
        print(self.phase)
        if self.phase == 1:
            for node in self.barrier:
                self.canvas.itemconfig(self.canvas.find_withtag(node), fill="gray9", outline="")
            self.instruction.configure(text="Left-click to select a start point"
                                       + "\nRight-click on it to deselect it")
            self.phase_status.configure(text="Start point", fg="green")
            self.create_matrix()
            self.remove_node()
        elif self.phase == 2:
            self.instruction.configure(text="Left-click to select an end point"
                                       + "\nRight-click on it to deselect it")
            self.phase_status.configure(text="End point", fg="yellow")
        elif self.phase == 3:
            self.instruction.configure(text="Press \"D\" to run Dijkstra's algorithm or"
                                       + "\nPress \"A\" to run A* algorithm")
            self.next_label.configure(text="")
            self.phase_status.configure(text="")
            self.root.bind("<d>", lambda event: self.dijkstra(self.start_point, self.end_point))

    def add_barrier(self, arg):
        self.current.configure(text=arg)
        if self.phase == 0:
            if self.cursor:
                self.barrier.add(arg)
                self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="red")
                print(self.barrier, len(self.barrier))

    def left_click(self, arg):
        if self.phase == 1 and self.start_point is None and arg not in self.barrier:
            self.start_point = arg
            print("Start point is:", self.start_point)
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="green")
            self.condition = True
        elif (self.phase == 2 and self.end_point is None and arg not in self.barrier
              and arg != self.start_point):
            self.end_point = arg
            print("End point is:", self.start_point)
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="yellow")
            self.condition = True

    def right_click(self, arg):
        if self.phase == 0:
            if arg in self.barrier:
                self.barrier.remove(arg)
                self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
                print(self.barrier, len(self.barrier))
        elif self.phase == 1 and self.start_point == arg:
            self.start_point = None
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
            self.condition = False
        elif self.phase == 2 and self.end_point == arg:
            self.end_point = None
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
            self.condition = False

    def set_cursor(self):
        if self.phase == 0:
            if self.cursor is False:
                self.cursor = True
                self.phase_status.configure(text="Active cursor", fg="green")
            else:
                self.cursor = False
                self.phase_status.configure(text="Disabled cursor", fg="red")

    def create_matrix(self):
        n = self.rows * self.columns
        self.matrix = np.zeros(n**2).reshape(n, n)
        for i in range(self.rows*self.columns):
            if i % self.columns != 0:
                self.matrix[i][i-1] = 1
            if i % self.columns != (self.columns-1):
                self.matrix[i][i+1] = 1
            if i > self.columns-1:
                self.matrix[i][i-self.columns] = 1
            if i < self.columns*self.rows - self.columns:
                self.matrix[i][i+self.columns] = 1
        return self.matrix

    def remove_node(self):
        for node in self.barrier:
            n = self.to_number(node)
            self.matrix[n] = 0
            self.matrix[:, n] = 0

    def dijkstra(self, start, end):
        self.phase_status.configure(text="Dijkstra's algorithm is running!", fg="green")
        frontier = dict()
        visited = dict()
        frontier = {start: [0, "starting index"]}
        while end not in visited:
            if len(frontier) == 0:
                self.phase_status.configure(text="No path available!", fg="red")
                return None
            min_dist = float("inf")
            for item in frontier.items():
                key = item[0]
                dist = item[1][0]
                if dist < min_dist:
                    min_dist = dist
                    min_key = key
            for index, item in enumerate(self.matrix[self.to_number(min_key)]):
                if item != 0:
                    key = self.to_str(index)
                    dist = min_dist + item
                    if key not in visited:
                        if key not in frontier:
                            frontier[key] = [dist, min_key]
                            if key != end:
                                self.canvas.itemconfig(self.canvas.find_withtag(key),
                                                       fill="PaleTurquoise1")
                                self.canvas.update()
                        else:
                            if dist < frontier[key][0]:
                                frontier[key] = [dist, min_key]
            time.sleep(0.01)
            visited[min_key] = frontier.pop(min_key)
            if min_key != start and min_key != end:
                self.canvas.itemconfig(self.canvas.find_withtag(min_key), fill="DodgerBlue3")
                self.canvas.update()
        path = [visited[end][1]]
        while path[0] != start:
            path.insert(0, visited[path[0]][1])
        for node in path:
            if node != start:
                self.canvas.itemconfig(self.canvas.find_withtag(node), fill="goldenrod")
        self.phase_status.configure(text="Path found!", fg="green")
        # return path, visited


if __name__ == "__main__":
    App()
