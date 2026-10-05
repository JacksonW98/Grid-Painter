import tkinter as tk

CANVAS_SIZE = 500


def draw_grid():
    rows = max(1, rows_var.get())
    cols = max(1, cols_var.get())
    canvas.delete("all")
    # Keep cells square and fit the longer side to CANVAS_SIZE
    cell = CANVAS_SIZE / max(rows, cols)
    canvas.config(width=cols * cell, height=rows * cell)
    for i in range(rows):
        for j in range(cols):
            x, y = j * cell, i * cell
            canvas.create_rectangle(x, y, x + cell, y + cell, outline="black", fill="white")


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

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white",
                   highlightthickness=0)
canvas.pack(padx=10, pady=10)

draw_grid()
root.mainloop()
