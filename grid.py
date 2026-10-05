import tkinter as tk

CANVAS_SIZE = 500
EMPTY_COLOR = "white"
DEFAULT_SIZE = 10  # rows and cols a grid starts with
PALETTE = [
    ("Black", "#000000"),
    ("Red", "#e53935"),
    ("Orange", "#fb8c00"),
    ("Yellow", "#fdd835"),
    ("Green", "#43a047"),
    ("Blue", "#1e88e5"),
    ("Purple", "#8e24aa"),
    ("Pink", "#ec407a"),
    ("Grey", "#9e9e9e"),
]

brush_color = PALETTE[0][1]  # defaults to black


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
        tk.Spinbox(controls, from_=1, to=100, textvariable=self.rows_var, width=5,
                   command=self.draw).pack(side=tk.LEFT, padx=5)

        tk.Label(controls, text="Cols:").pack(side=tk.LEFT)
        self.cols_var = tk.IntVar(value=DEFAULT_SIZE)
        tk.Spinbox(controls, from_=1, to=100, textvariable=self.cols_var, width=5,
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
                                                        outline="black", fill=EMPTY_COLOR))
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

    def on_left_click(self, event):
        self.paint(event, brush_color)

    def on_right_click(self, event):
        self.paint(event, EMPTY_COLOR)


def on_swatch_click(event):
    global brush_color
    # event.widget is the swatch that was clicked, its background is its color
    brush_color = event.widget.cget("bg")
    # Show the name of the selected color
    for name, color in PALETTE:
        if color == brush_color:
            color_label.config(text=name)


def on_grid_count_change():
    # The second grid is hidden rather than deleted
    if grid_count_var.get() == 2:
        grid2.frame.pack(side=tk.LEFT, anchor="n")
        copy_button.pack(side=tk.LEFT, padx=(20, 0))
    else:
        grid2.frame.pack_forget()
        copy_button.pack_forget()


def copy_left_to_right():
    # Copy the left grid (size and colors) to the right
    grid2.rows_var.set(grid1.rows_var.get())
    grid2.cols_var.set(grid1.cols_var.get())
    grid2.draw()
    for row in range(len(grid1.cells)):
        for col in range(len(grid1.cells[row])):
            # Reads the color of the grid on grid1 and copies it over to grid 2
            color = grid1.canvas.itemcget(grid1.cells[row][col], "fill")
            grid2.canvas.itemconfig(grid2.cells[row][col], fill=color)


def reset_grids():
    grid1.reset()
    grid2.reset()


root = tk.Tk()
root.title("Grid")

top = tk.Frame(root)
top.pack(pady=5)

# Grid count radio buttons
tk.Label(top, text="Grids:").pack(side=tk.LEFT)
grid_count_var = tk.IntVar(value=2) # Default to 2 grids
for count in (1, 2):
    tk.Radiobutton(top, text=str(count), variable=grid_count_var, value=count,
                   command=on_grid_count_change).pack(side=tk.LEFT)

palette = tk.Frame(top)
palette.pack(side=tk.LEFT, padx=(20, 0))
# macOS ignores the background color of buttons so I just used labels instead
for name, color in PALETTE:
    swatch = tk.Label(palette, bg=color, width=2, height=1)
    swatch.pack(side=tk.LEFT, padx=2)
    swatch.bind("<Button-1>", on_swatch_click)
color_label = tk.Label(palette, text=PALETTE[0][0], width=7, anchor="w")
color_label.pack(side=tk.LEFT, padx=5)

tk.Button(top, text="Reset", command=reset_grids).pack(side=tk.LEFT, padx=(20, 0))

copy_button = tk.Button(top, text="Copy left -> right", command=copy_left_to_right)  # only packed when 2 is selected

grids = tk.Frame(root)
grids.pack()
grid1 = Grid(grids)
grid1.frame.pack(side=tk.LEFT, anchor="n")
grid2 = Grid(grids)  # only packed when 2 is selected
on_grid_count_change()  # show grid 2 and the copy button

root.mainloop()
