import tkinter as tk

CANVAS_SIZE = 500


def draw_grid():
    n = max(1, size_var.get())
    canvas.delete("all")
    cell = CANVAS_SIZE / n
    for i in range(n):
        for j in range(n):
            x, y = j * cell, i * cell
            canvas.create_rectangle(x, y, x + cell, y + cell, outline="black", fill="white")


root = tk.Tk()
root.title("Grid")

controls = tk.Frame(root)
controls.pack(pady=5)

tk.Label(controls, text="Size (n):").pack(side=tk.LEFT)
size_var = tk.IntVar(value=10)
tk.Spinbox(controls, from_=1, to=100, textvariable=size_var, width=5,
           command=draw_grid).pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack(padx=10, pady=10)

draw_grid()
root.mainloop()
