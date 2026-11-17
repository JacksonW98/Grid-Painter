import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from export import LINE_COLOR, make_image
from tasks import load_task, save_task

CANVAS_SIZE = 500
DEFAULT_SIZE = 10  # rows and cols a grid starts with
PALETTE = [
    "#000000",  # 0 black
    "#0074D9",  # 1 blue
    "#FF4136",  # 2 red
    "#2ECC40",  # 3 green
    "#FFDC00",  # 4 yellow
    "#AAAAAA",  # 5 gray
    "#F012BE",  # 6 fuchsia
    "#FF851B",  # 7 orange
    "#7FDBFF",  # 8 teal
    "#870C25",  # 9 brown
]
EMPTY_COLOR = PALETTE[0]  # default to 0 (black)

brush_color = PALETTE[1]  # defaults to blue


class Grid:
    # Grid class so it can be reused

    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.cells = []  # cells[row][col] is the canvas ID of that square
        self.cell_size = 0

        controls = tk.Frame(self.frame)
        controls.pack(pady=5)

        tk.Label(controls, text="Rows:").pack(side=tk.LEFT)
        self.rows_var = tk.IntVar(value=DEFAULT_SIZE)
        tk.Spinbox(controls, from_=1, to=30, textvariable=self.rows_var, width=5,
                   command=self.draw).pack(side=tk.LEFT, padx=5)

        tk.Label(controls, text="Cols:").pack(side=tk.LEFT)
        self.cols_var = tk.IntVar(value=DEFAULT_SIZE)
        tk.Spinbox(controls, from_=1, to=30, textvariable=self.cols_var, width=5,
                   command=self.draw).pack(side=tk.LEFT, padx=5)


        self.canvas = tk.Canvas(self.frame, width=CANVAS_SIZE, height=CANVAS_SIZE,
                                bg=EMPTY_COLOR, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)  # right click (Apparently it's button-3 not 2 on macos)
        self.canvas.bind("<B3-Motion>", self.on_right_click)

        self.draw()

    def draw(self):
        rows = max(1, self.rows_var.get())
        cols = max(1, self.cols_var.get())
        self.canvas.delete("all")
        # Keep cells square and fit the longer side to CANVAS_SIZE
        self.cell_size = CANVAS_SIZE / max(rows, cols)
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)
        self.cells = []
        for i in range(rows):
            row = []
            for j in range(cols):
                x, y = j * self.cell_size, i * self.cell_size
                row.append(self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                        outline=LINE_COLOR, fill=EMPTY_COLOR))
            self.cells.append(row)

    def reset(self):
        # Set the size back to the default (10x10) and clear all the colors
        self.rows_var.set(DEFAULT_SIZE)
        self.cols_var.set(DEFAULT_SIZE)
        self.draw()

    def paint(self, event, color):
        # "current" tag doesn't update when a button is held down so figure out current position
        row = int(event.y // self.cell_size)
        col = int(event.x // self.cell_size)
        if 0 <= row < len(self.cells) and 0 <= col < len(self.cells[0]):
            self.canvas.itemconfig(self.cells[row][col], fill=color)

    def get_colors(self):
        # colors[row][col] is the color of that square
        return [[self.canvas.itemcget(cell, "fill") for cell in row] for row in self.cells]

    def get_values(self):
        # values[row][col] is that square's ARC value (0-9)
        return [[PALETTE.index(color) for color in row] for row in self.get_colors()]

    def set_values(self, values):
        # Resize the grid to fit values and color each square
        self.rows_var.set(len(values))
        self.cols_var.set(len(values[0]))
        self.draw()
        for row in range(len(values)):
            for col in range(len(values[row])):
                self.canvas.itemconfig(self.cells[row][col], fill=PALETTE[values[row][col]])

    def on_left_click(self, event):
        self.paint(event, brush_color)

    def on_right_click(self, event):
        self.paint(event, EMPTY_COLOR)


def blank_grid():
    return [[0] * DEFAULT_SIZE for _ in range(DEFAULT_SIZE)]


def new_pair():
    return {"input": blank_grid(), "output": blank_grid()}


# The task being made. The two grids show (and edit) one pair of it at a time
task = {"train": [new_pair()], "test": []}
current = ("train", 0)  # (section, index) of the pair on the grids


def store_current_pair():
    # Copy what is on the grids back into the task
    section, index = current
    task[section][index] = {"input": grid1.get_values(), "output": grid2.get_values()}


def load_pair(section, index):
    # Put the pair task[section][index] on the grids (without storing the old one)
    global current
    current = (section, index)
    pair = task[section][index]
    grid1.set_values(pair["input"])
    grid2.set_values(pair["output"])
    pair_label.config(text=f"{section.title()} {index + 1}")
    refresh_pair_list()


def show_pair(section, index):
    # Store the pair on the grids, then switch to task[section][index]
    store_current_pair()
    load_pair(section, index)


def pair_order():
    # Every pair in the order it is listed: train pairs, then test pairs
    return [(section, index) for section in ("train", "test") for index in range(len(task[section]))]


def refresh_pair_list():
    pair_list.delete(0, tk.END)
    for section, index in pair_order():
        pair_list.insert(tk.END, f"{section.title()} {index + 1}")
    pair_list.selection_set(pair_order().index(current))


def open_task():
    # Replace the task with one from a JSON file and show its first pair
    global task
    path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if not path:
        return  # cancelled
    task = load_task(path)
    load_pair(*pair_order()[0])


def save_task_as():
    # Save the whole task to a JSON file
    store_current_pair()
    path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
    if not path:
        return  # cancelled
    save_task(task, path)
    print(f"Saved {path}")


def on_pair_select(event):
    selected = pair_list.curselection()
    if selected:
        show_pair(*pair_order()[selected[0]])


def add_pair(section):
    # Add a blank pair to the end of the section and switch to it
    store_current_pair()
    task[section].append(new_pair())
    load_pair(section, len(task[section]) - 1)


def remove_pair():
    # Remove the pair on the grids and show the one listed after it (or before, if it was last)
    order = pair_order()
    if len(order) == 1:
        return  # keep at least one pair to show on the grids
    position = order.index(current)
    section, index = current
    del task[section][index]
    order = pair_order()
    load_pair(*order[min(position, len(order) - 1)])


def on_swatch_click(event):
    global brush_color
    # event.widget is the swatch that was clicked, its background is its color
    brush_color = event.widget.cget("bg")
    # Show the value of the selected color
    color_label.config(text=PALETTE.index(brush_color))


def copy_left_to_right():
    # Copy the left grid (size and colors) to the right
    grid2.set_values(grid1.get_values())


def reset_grids():
    grid1.reset()
    grid2.reset()


def save_image():
    # Use the export module to make an image (should be the same as the old tool)
    grids = [grid1.get_colors(), grid2.get_colors()]

    names = [f"{len(colors[0])}x{len(colors)}" for colors in grids]
    name = "grid_" + "+".join(names)
    folder = Path("images")

    folder.mkdir(exist_ok=True)
    path = folder / f"{name}.png"

    # Prevent overwriting existing files
    number = 1
    while path.exists():
        path = folder / f"{name} ({number}).png"
        number += 1
    make_image(grids).save(path)
    print(f"Saved {path}")


root = tk.Tk()
root.title("Grid")

top = tk.Frame(root)
top.pack(pady=5)

# Which pair of the task is on the grids
pair_label = tk.Label(top, text="Train 1", width=8, anchor="w", font=("TkDefaultFont", 14, "bold"))
pair_label.pack(side=tk.LEFT, padx=(0, 20))

palette = tk.Frame(top)
palette.pack(side=tk.LEFT)
# macOS ignores the background color of buttons so I just used labels instead
for color in PALETTE:
    swatch = tk.Label(palette, bg=color, width=2, height=1)
    swatch.pack(side=tk.LEFT, padx=2)
    swatch.bind("<Button-1>", on_swatch_click)
color_label = tk.Label(palette, text=1, width=2, anchor="w")
color_label.pack(side=tk.LEFT, padx=5)

tk.Button(top, text="Open task", command=open_task).pack(side=tk.LEFT, padx=(20, 0))
tk.Button(top, text="Save task", command=save_task_as).pack(side=tk.LEFT, padx=(5, 0))
tk.Button(top, text="Reset", command=reset_grids).pack(side=tk.LEFT, padx=(20, 0))
tk.Button(top, text="Make image", command=save_image).pack(side=tk.LEFT, padx=(5, 0))

tk.Button(top, text="Copy input -> output", command=copy_left_to_right).pack(side=tk.LEFT, padx=(20, 0))

grids = tk.Frame(root)
grids.pack()

# Listbox of the task's pairs
sidebar = tk.Frame(grids)
sidebar.pack(side=tk.LEFT, anchor="n", padx=(10, 0), pady=5)
tk.Label(sidebar, text="Pairs", font=("TkDefaultFont", 14, "bold")).pack()
pair_list = tk.Listbox(sidebar, width=10, height=12, exportselection=False, activestyle="none")
pair_list.pack(pady=5)
pair_list.bind("<<ListboxSelect>>", on_pair_select)
tk.Button(sidebar, text="+ Train", command=lambda: add_pair("train")).pack(fill=tk.X)
tk.Button(sidebar, text="+ Test", command=lambda: add_pair("test")).pack(fill=tk.X)
tk.Button(sidebar, text="Remove", command=remove_pair).pack(fill=tk.X)
grid1 = Grid(grids)
grid1.frame.pack(side=tk.LEFT, anchor="n")
grid2 = Grid(grids)
grid2.frame.pack(side=tk.LEFT, anchor="n")
refresh_pair_list()

root.mainloop()
