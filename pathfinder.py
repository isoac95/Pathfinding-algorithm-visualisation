import tkinter as tk
import numpy as np
import time


class App:

    def __init__(self):
        self.rows = 30
        self.columns = 60
        self.cell_size = 20
        self.root = tk.Tk()
        self.root.title("Pathfinding algorithms by Ante Culo")
        self.root.configure(bg="gray9")
        self.create_ui()
        self.reset()
        self.root.mainloop()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.columns*self.cell_size,
                                height=self.rows*self.cell_size, bd=0, highlightthickness=0)
        self.instruction = tk.Label(self.root, text="\n\n", bg="gray9", fg="white")
        self.lbl_frame = tk.Frame(self.root, bg="gray9")
        self.status = tk.Label(self.root, text="", bg="gray9")
        self.p0 = tk.Label(self.lbl_frame, text="Create barrier", fg="white", bg="gray9")
        self.p1 = tk.Label(self.lbl_frame, text="Start point", fg="white", bg="gray9")
        self.p2 = tk.Label(self.lbl_frame, text="End point", fg="white", bg="gray9")
        self.p3 = tk.Label(self.lbl_frame, text="Algorithm", fg="white", bg="gray9")
        self.i1 = tk.Label(self.lbl_frame, text="|", fg="white", bg="gray9")
        self.i2 = tk.Label(self.lbl_frame, text="|", fg="white", bg="gray9")
        self.i3 = tk.Label(self.lbl_frame, text="|", fg="white", bg="gray9")
        self.p0.grid(row=0, column=0)
        self.i1.grid(row=0, column=1)
        self.p1.grid(row=0, column=2)
        self.i2.grid(row=0, column=3)
        self.p2.grid(row=0, column=4)
        self.i3.grid(row=0, column=5)
        self.p3.grid(row=0, column=6)
        self.lbl_frame.pack(pady=5)
        self.instruction.pack()
        self.status.pack()
        self.canvas.pack(padx=10)

    def reset(self):
        self.canvas.delete("all")
        self.create_field()
        self.start_point = None
        self.end_point = None
        self.phase = -1
        self.condition = True
        self.change_phase()
        self.barrier = set()
        self.cursor = False

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

    def return_ij(self, str):
        i = int(str[str.find("i")+1: str.find("j")])
        j = int(str[str.find("j")+1:])
        return (i, j)

    def change_phase(self):
        if self.condition:
            self.phase += 1
            self.condition = False
        print("Phase ", self.phase)
        if self.phase == 0:
            self.root.bind("<p>", lambda event: self.change_phase())
            self.root.bind("<space>", lambda event: self.set_cursor())
            self.instruction.configure(text="Press \"space\" to enable/disable cursor"
                                            + "to quick-select"
                                            + "\nPress Left-click/Right-click "
                                            + "to single select/deselect"
                                            + "\nPress \"P\" when done")
            self.status.configure(text="Disabled cursor", fg="red")
            self.p0.configure(bg="gray25")
            self.condition = True
        elif self.phase == 1:
            print(self.barrier, len(self.barrier))
            for node in self.barrier:
                self.canvas.itemconfig(self.canvas.find_withtag(node), fill="gray9", outline="")
            self.instruction.configure(text="Left-click to select a start point"
                                       + "\nRight-click on it to deselect it"
                                       + "\nPress \"P\" when start point is selected")
            self.status.configure(text="Start point is not selected", fg="red")
            self.p0.configure(bg="gray9")
            self.p1.configure(bg="gray25")
            self.create_matrix()
            self.remove_node()
        elif self.phase == 2:
            self.instruction.configure(text="Left-click to select an end point"
                                       + "\nRight-click on it to deselect it"
                                       + "\nPress \"P\" when end point is selected")
            self.status.configure(text="End point is not selected", fg="red")
            self.p1.configure(bg="gray9")
            self.p2.configure(bg="gray25")
        elif self.phase == 3:
            self.instruction.configure(text="Press \"D\" to run Dijkstra's algorithm or"
                                       + "\nPress \"A\" to run A* algorithm"
                                       + "\n")
            self.status.configure(text="")
            self.p2.configure(bg="gray9")
            self.p3.configure(bg="gray25")
            self.root.bind("<d>", lambda event: self.run_dijkstra())
            self.root.bind("<a>", lambda event: self.run_a_star())
        elif self.phase == 4:
            self.instruction.configure(text="\nEnjoy simulation :)\n")
        elif self.phase == 5:
            self.root.bind("<r>", lambda event: self.reset())
            self.p3.configure(bg="gray9")
            self.instruction.configure(text="\nPress \"R\" to restart\n")

    def add_barrier(self, arg):
        if self.phase == 0:
            if self.cursor:
                self.barrier.add(arg)
                self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="red")

    def left_click(self, arg):
        if self.phase == 0:
            self.barrier.add(arg)
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="red")
        elif self.phase == 1 and self.start_point is None and arg not in self.barrier:
            self.start_point = arg
            print("Start point is:", self.start_point)
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="green")
            self.status.configure(text="Start point is selected", fg="green")
            self.condition = True
        elif (self.phase == 2 and self.end_point is None and arg not in self.barrier
              and arg != self.start_point):
            self.end_point = arg
            print("End point is:", self.end_point)
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="yellow")
            self.status.configure(text="End point is selected", fg="green")
            self.condition = True

    def right_click(self, arg):
        if self.phase == 0:
            if arg in self.barrier:
                self.barrier.remove(arg)
                self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
        elif self.phase == 1 and self.start_point == arg:
            self.start_point = None
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
            self.status.configure(text="Start point is not selected", fg="red")
            self.condition = False
        elif self.phase == 2 and self.end_point == arg:
            self.end_point = None
            self.canvas.itemconfig(self.canvas.find_withtag(arg), fill="gray25")
            self.status.configure(text="End point is not selected", fg="red")
            self.condition = False

    def set_cursor(self):
        if self.phase == 0:
            if self.cursor is False:
                self.cursor = True
                self.status.configure(text="Active cursor", fg="green")
            else:
                self.cursor = False
                self.status.configure(text="Disabled cursor", fg="red")

    def create_matrix(self):
        n = self.rows * self.columns
        self.matrix = np.zeros(n**2).reshape(n, n)
        for i in range(self.rows*self.columns):
            if i % self.columns != 0:
                self.matrix[i][i-1] = 10
            if i % self.columns != (self.columns-1):
                self.matrix[i][i+1] = 10
            if i > self.columns-1:
                self.matrix[i][i-self.columns] = 10
            if i < self.columns*self.rows - self.columns:
                self.matrix[i][i+self.columns] = 10
            if i > self.columns-1 and i % self.columns != 0:
                self.matrix[i][i-self.columns-1] = 14
            if i > self.columns-1 and i % self.columns != (self.columns-1):
                self.matrix[i][i-self.columns+1] = 14
            if i < self.columns*self.rows - self.columns and i % self.columns != 0:
                self.matrix[i][i+self.columns-1] = 14
            if i < self.columns*self.rows - self.columns and i % self.columns != (self.columns-1):
                self.matrix[i][i+self.columns+1] = 14
        return self.matrix

    def remove_node(self):
        for node in self.barrier:
            n = self.to_number(node)
            self.matrix[n] = 0
            self.matrix[:, n] = 0

    def run_dijkstra(self):
        if self.phase == 3:
            self.condition = True
            self.change_phase()
            self.dijkstra(self.start_point, self.end_point)
            self.condition = True
            self.change_phase()

    def run_a_star(self):
        if self.phase == 3:
            self.condition = True
            self.change_phase()
            self.hcost_matrix = self.create_hcost_matrix(self.end_point)
            self.a_star(self.start_point, self.end_point)
            self.condition = True
            self.change_phase()

    def dijkstra(self, start, end):
        self.status.configure(text="Dijkstra's algorithm is running!", fg="green")
        frontier = dict()
        visited = dict()
        frontier = {start: [0, "starting index"]}
        while end not in visited:
            if len(frontier) == 0:
                self.status.configure(text="No path available!", fg="red")
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
        self.status.configure(text="Path found!", fg="green")

    def create_hcost_matrix(self, name):
        matrix = np.zeros(self.rows*self.columns).reshape(self.rows, self.columns)
        srow = int(name[name.find("i")+1: name.find("j")])
        scol = int(name[name.find("j")+1:])
        matrix[srow][scol] = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if i < srow and j < scol:
                    new_i = i
                    new_j = j
                    count = 0
                    while new_i != srow and new_j != scol:
                        new_i += 1
                        new_j += 1
                        count += 1
                    matrix[i][j] = abs(new_i-srow)*10 + abs(new_j - scol)*10 + count*14
                elif i > srow and j < scol:
                    new_i = i
                    new_j = j
                    count = 0
                    while new_i != srow and new_j != scol:
                        new_i -= 1
                        new_j += 1
                        count += 1
                    matrix[i][j] = abs(new_i-srow)*10 + abs(new_j - scol)*10 + count*14
                elif i > srow and j > scol:
                    new_i = i
                    new_j = j
                    count = 0
                    while new_i != srow and new_j != scol:
                        new_i -= 1
                        new_j -= 1
                        count += 1
                    matrix[i][j] = abs(new_i-srow)*10 + abs(new_j - scol)*10 + count*14
                elif i < srow and j > scol:
                    new_i = i
                    new_j = j
                    count = 0
                    while new_i != srow and new_j != scol:
                        new_i += 1
                        new_j -= 1
                        count += 1
                    matrix[i][j] = abs(new_i-srow)*10 + abs(new_j - scol)*10 + count*14
                else:
                    matrix[i][j] = abs(i-srow)*10 + abs(j - scol)*10
        return matrix

    def a_star(self, start, end):
        self.status.configure(text="A* algorithm is running!", fg="green")
        frontier = dict()
        visited = dict()
        start_row = self.return_ij(start)[0]
        start_col = self.return_ij(start)[1]
        start_hcost = self.hcost_matrix[start_row][start_col]
        frontier = {start: [0, "starting index", start_hcost]}
        while end not in visited:
            if len(frontier) == 0:
                self.status.configure(text="No path available!", fg="red")
                return None
            min_dist = float("inf")
            for item in frontier.items():
                key = item[0]
                item_fcost = item[1][0]
                item_hcost = item[1][2]
                dist = item_fcost + item_hcost
                if dist < min_dist:
                    min_dist = dist
                    min_key = key
                    min_fcost = item_fcost
                    min_hcost = item_hcost
                elif dist == min_dist and item_hcost < min_hcost:
                    min_key = key
                    min_fcost = item_fcost
                    min_hcost = item_hcost

            for index, item in enumerate(self.matrix[self.to_number(min_key)]):
                if item != 0:
                    key = self.to_str(index)
                    hcost_row = self.return_ij(key)[0]
                    hcost_col = self.return_ij(key)[1]
                    hcost = self.hcost_matrix[hcost_row][hcost_col]
                    fcost = min_fcost + item
                    if key not in visited:
                        if key not in frontier:
                            frontier[key] = [fcost, min_key, hcost]
                            if key != end:
                                self.canvas.itemconfig(self.canvas.find_withtag(key),
                                                       fill="PaleTurquoise1")
                                self.canvas.update()
                        else:
                            if fcost + hcost < frontier[key][0] + frontier[key][2]:
                                frontier[key] = [fcost, min_key, hcost]
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
        self.status.configure(text="Path found!", fg="green")


if __name__ == "__main__":
    App()
