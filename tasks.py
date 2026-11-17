"""Load and save tasks in JSON format

{"train": [pair, ...], "test": [pair, ...]}, where a pair is
{"input": grid, "output": grid} and a grid is a list of rows of ints 0-9
"""
import json
from pathlib import Path

def load_task(path):
    return json.loads(Path(path).read_text())

def save_task(task, path):
    Path(path).write_text(json.dumps(task))

# TODO add validation