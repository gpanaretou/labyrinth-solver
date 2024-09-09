from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.__root = Tk()
        Tk.title = "Maze Solver v0.1"

        self.canvas = Canvas()
        self.canvas.pack()

        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True

        while self.running is True:
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color=fill_color)

class Pointer:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Pointer, point2: Pointer):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, 
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self, pointer1: Pointer, pointer2: Pointer, window: Window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = pointer1.x
        self._y1 = pointer1.y
        self._x2 = pointer2.x
        self._y2 = pointer2.y

        self.__assign_coordinates()
        self._win = window

    def __assign_coordinates(self):
        if self._x1 > self._x2:
            self._x1, self._x2 = self._x2, self._x1
        if self._y1 > self._y2:
            self._y1, self._y2 = self._y2, self._y1
        return
    
    def get_center(self):
        x = self._x1 + (self._x2 - self._x1) // 2
        y = self._y1 + (self._y2 - self._y1) // 2

        return Pointer(x, y)


    def draw(self):
        self._win.draw_line(
            Line(
                Pointer(self._x1, self._y1),
                Pointer(self._x1, self._y2)),
            fill_color=None if self.has_left_wall else "#d9d9d9"
        )
        self._win.draw_line(
            Line(
                Pointer(self._x2, self._y1),
                Pointer(self._x2, self._y2)),
            fill_color=None if self.has_right_wall else "#d9d9d9"

        )
        self._win.draw_line(
            Line(
                Pointer(self._x1, self._y2),
                Pointer(self._x2, self._y2)),
            fill_color=None if self.has_bottom_wall else "#d9d9d9"
        )
        self._win.draw_line(
            Line(
                Pointer(self._x1, self._y1),
                Pointer(self._x2, self._y1)),
            fill_color=None if self.has_top_wall else "#d9d9d9"
        )
        return

    def draw_move(self, to_cell, undo=False):
        if undo is True:
            fill_color = "gray"
        else:
            fill_color = "red"

        start_point = self.get_center()
        end_point = to_cell.get_center()
        
        line = Line(start_point, end_point)
        self._win.draw_line(line, fill_color)

class Maze():
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win: Window = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self._cells = []
        
        for i in range(0, self.num_cols):
            self._cells.append([])
            for j in range(0, self.num_rows):
                self._cells[i].append(self._draw_cell(i, j))

    def _draw_cell(self, i: int, j: int):
        maze_offset_x = self.cell_size_x
        maze_offset_y = self.cell_size_y
        c = Cell(
                    Pointer((i+1)*self.cell_size_x + maze_offset_x, (j+1)*self.cell_size_y + maze_offset_y), 
                    Pointer((i+2)*self.cell_size_x + maze_offset_x, (j+2)*self.cell_size_y + maze_offset_y),
                    window=self.win
                )
        if self.win is not None:
            c.draw()
            self._animate()

        return c

    def _animate(self):
        self.win.redraw()
        time.sleep(0.1)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_left_wall = False

        exit = self._cells[-1][-1]
        exit.has_right_wall = False
        
        if self.win is not None:
            entrance.draw()
            exit.draw()