from PIL import Image, ImageDraw, ImageFont

SIDE = 900  # longer side of each grid
MARGIN = 40
GAP = 60
LINE_WIDTH = 3
LABEL_SIZE = 36
LABEL_SPACE = 30  # room above the grids for the size labels


def make_image(grids):
    # grids is a list of color grids, where grid[row][col] is that square's color.
    sizes = [(len(grid[0]), len(grid)) for grid in grids]  # (cols, rows)
    grids_width = sum(SIDE * cols / max(cols, rows) for cols, rows in sizes)
    width = round(grids_width + GAP * (len(sizes) - 1)) + 2 * MARGIN
    top = MARGIN + LABEL_SPACE
    img = Image.new("RGB", (width, top + SIDE + MARGIN), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(LABEL_SIZE)

    # How far a line reaches either side of its position
    before = LINE_WIDTH // 2
    after = LINE_WIDTH - 1 - before

    x0 = MARGIN
    for grid, (cols, rows) in zip(grids, sizes):
        cell = SIDE / max(cols, rows)
        y0 = top + (SIDE - cell * rows) / 2
        xs = [round(x0 + i * cell) for i in range(cols + 1)]
        ys = [round(y0 + i * cell) for i in range(rows + 1)]
        left = xs[0] - before
        right = xs[-1] + after
        upper = ys[0] - before
        lower = ys[-1] + after

        # Fill the squares first, so the grid lines are drawn on top
        for row in range(rows):
            for col in range(cols):
                draw.rectangle([xs[col], ys[row], xs[col + 1], ys[row + 1]], fill=grid[row][col])

        for x in xs:
            draw.rectangle([x - before, upper, x + after, lower], fill="black")
        for y in ys:
            draw.rectangle([left, y - before, right, y + after], fill="black")

        draw.text((left, upper - 12), f"{cols} x {rows}", fill="black", font=font, anchor="ls")
        x0 += cell * cols + GAP

    return img
