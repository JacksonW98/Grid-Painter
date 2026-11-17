from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 900  # longer side of each grid
MARGIN = 40
GAP = 60
LINE_WIDTH = 3
LINE_COLOR = "#555555"  # grey, so lines show up on the black (0) background
LABEL_SIZE = 36
LABEL_SPACE = 30  # room above the grids for the size labels


BOX = 400  # each grid is scaled to fit a BOX x BOX square
NAME_WIDTH = 200  # room on the left for the pair names
ARROW_WIDTH = 140  # room between the input and output for the arrow
ROW_GAP = 70  # space between pairs
ARROW_PATH = Path(__file__).parent / "assets" / "arrow.png"


def pair_name(task, section, index):
    if section == "test" and len(task["test"]) == 1:
        return "Test"
    return f"{section.title()} {index + 1}"


def paste_arrow(img, x0, x1, y):
    # Paste the arrow image, scaled to fit between x0 and x1
    arrow = Image.open(ARROW_PATH)
    width = round(x1 - x0)
    height = round(arrow.height * width / arrow.width)
    arrow = arrow.resize((width, height))
    img.paste(arrow, (round(x0), round(y - height / 2)), arrow)


def draw_grid(draw, grid, x0, y0, cell, font):
    # Draw a color grid with its top left corner at (x0, y0)
    rows, cols = len(grid), len(grid[0])

    # How far a line reaches either side of its position
    before = LINE_WIDTH // 2
    after = LINE_WIDTH - 1 - before

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
        draw.rectangle([x - before, upper, x + after, lower], fill=LINE_COLOR)
    for y in ys:
        draw.rectangle([left, y - before, right, y + after], fill=LINE_COLOR)

    draw.text((left, upper - 12), f"{cols} x {rows}", fill="black", font=font, anchor="ls")


def make_image(grids):
    sizes = [(len(grid[0]), len(grid)) for grid in grids]  # (cols, rows)
    grids_width = sum(SIDE * cols / max(cols, rows) for cols, rows in sizes)
    width = round(grids_width + GAP * (len(sizes) - 1)) + 2 * MARGIN
    top = MARGIN + LABEL_SPACE
    img = Image.new("RGB", (width, top + SIDE + MARGIN), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(LABEL_SIZE)

    x0 = MARGIN
    for grid, (cols, rows) in zip(grids, sizes):
        cell = SIDE / max(cols, rows)
        draw_grid(draw, grid, x0, top + (SIDE - cell * rows) / 2, cell, font)
        x0 += cell * cols + GAP

    return img


def make_task_image(task, palette, hide_test_output=False):
    # Draw every grid pair. With hide_test_output, test outputs are left blank
    pairs = [(pair_name(task, section, i), section, pair) for section in ("train", "test")
             for i, pair in enumerate(task[section])]

    def hidden(section, key):
        return hide_test_output and section == "test" and key == "output"

    def grid_height(grid):
        # Height of the grid once it is scaled to fit a BOX x BOX square
        return BOX * len(grid) / max(len(grid), len(grid[0]))

    # Each row is only as tall as its tallest grid, so wide grids don't leave gaps
    # (a hidden output doesn't count, so the row doesn't give away its size)
    box_heights = [max(grid_height(pair[key]) for key in ("input", "output") if not hidden(section, key))
                   for _, section, pair in pairs]
    width = 2 * MARGIN + NAME_WIDTH + 2 * BOX + ARROW_WIDTH
    height = round(2 * MARGIN + sum(LABEL_SPACE + h for h in box_heights) + (len(pairs) - 1) * ROW_GAP)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(LABEL_SIZE)

    y = MARGIN
    for number, ((name, section, pair), box_height) in enumerate(zip(pairs, box_heights)):
        if number == len(task["train"]) and number > 0:
            # Line between the trai and test pairs
            line_y = round(y - ROW_GAP / 2)
            draw.rectangle([MARGIN, line_y - 1, width - MARGIN, line_y + 1], fill=LINE_COLOR)

        box_top = y + LABEL_SPACE
        middle = box_top + box_height / 2
        draw.text((MARGIN, middle), name, fill="black", font=font, anchor="lm")

        x = MARGIN + NAME_WIDTH
        for key in ("input", "output"):
            if not hidden(section, key):  # a hidden test output is left blank TODO add a question mark symbol or something
                grid = [[palette[value] for value in row] for row in pair[key]]
                rows, cols = len(grid), len(grid[0])
                cell = BOX / max(rows, cols)
                # Centre the grid in its box
                draw_grid(draw, grid, x + (BOX - cell * cols) / 2, box_top + (box_height - cell * rows) / 2, cell, font)
            x += BOX + ARROW_WIDTH

        # Arrow from the input to the output
        start = MARGIN + NAME_WIDTH + BOX + 30
        paste_arrow(img, start, start + ARROW_WIDTH - 60, middle)

        y += LABEL_SPACE + box_height + ROW_GAP

    return img
