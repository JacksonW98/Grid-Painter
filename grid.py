import tkinter as tk

CANVAS_SIZE = 500
EMPTY_COLOR = "white"

cells = []  # cells[row][col] is the canvas ID of that square
cell_size = 0


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
    paint(event, brush_color.get())


def on_right_click(event):
    paint(event, EMPTY_COLOR)


root = tk.Tk()
root.title("Grid")

brush_color = tk.StringVar(value="black")

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

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=EMPTY_COLOR,
                   highlightthickness=0)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<B1-Motion>", on_left_click)
canvas.bind("<Button-3>", on_right_click)  # right click (Apparently it's button-3 not 2 on macos)
canvas.bind("<B3-Motion>", on_right_click)

draw_grid()
root.mainloop()
