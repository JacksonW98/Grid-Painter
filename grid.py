import tkinter as tk

CANVAS_SIZE = 500
EMPTY_COLOR = "white"
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

cells = []  # cells[row][col] is the canvas ID of that square
cell_size = 0
brush_color = PALETTE[0][1]  # defaults to black


def draw_grid():
    global cells, cell_size
    rows = max(1, rows_var.get())
    cols = max(1, cols_var.get())
    canvas.delete("all")
    # Keep cells square and fit the longer side to CANVAS_SIZE
    cell_size = CANVAS_SIZE / max(rows, cols)
    canvas.config(width=cols * cell_size, height=rows * cell_size)
    cells = []
    for i in range(rows):
        row = []
        for j in range(cols):
            x, y = j * cell_size, i * cell_size
            row.append(canvas.create_rectangle(x, y, x + cell_size, y + cell_size,
                                               outline="black", fill=EMPTY_COLOR))
        cells.append(row)


def paint(event, color):
    # "current" tag doesn't update when a button is held down so figure out current position
    row = int(event.y // cell_size)
    col = int(event.x // cell_size)
    if 0 <= row < len(cells) and 0 <= col < len(cells[0]):
        canvas.itemconfig(cells[row][col], fill=color)


def on_left_click(event):
    paint(event, brush_color)


def on_right_click(event):
    paint(event, EMPTY_COLOR)


def on_swatch_click(event):
    global brush_color
    # event.widget is the swatch that was clicked, its background is its color
    brush_color = event.widget.cget("bg")
    # Show the name of the selected color
    for name, color in PALETTE:
        if color == brush_color:
            color_label.config(text=name)


root = tk.Tk()
root.title("Grid")

controls = tk.Frame(root)
controls.pack(pady=5)

tk.Label(controls, text="Rows:").pack(side=tk.LEFT)
rows_var = tk.IntVar(value=10)
tk.Spinbox(controls, from_=1, to=100, textvariable=rows_var, width=5,
           command=draw_grid).pack(side=tk.LEFT, padx=5)

tk.Label(controls, text="Cols:").pack(side=tk.LEFT)
cols_var = tk.IntVar(value=10)
tk.Spinbox(controls, from_=1, to=100, textvariable=cols_var, width=5,
           command=draw_grid).pack(side=tk.LEFT, padx=5)

palette = tk.Frame(root)
palette.pack()
# macOS ignores the background color of buttons so I just used labels instead
for name, color in PALETTE:
    swatch = tk.Label(palette, bg=color, width=2, height=1)
    swatch.pack(side=tk.LEFT, padx=2)
    swatch.bind("<Button-1>", on_swatch_click)
color_label = tk.Label(palette, text=PALETTE[0][0], width=7, anchor="w")
color_label.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=EMPTY_COLOR,
                   highlightthickness=0)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<B1-Motion>", on_left_click)
canvas.bind("<Button-3>", on_right_click)  # right click (Apparently it's button-3 not 2 on macos)
canvas.bind("<B3-Motion>", on_right_click)

draw_grid()
root.mainloop()
