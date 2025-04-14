from collections import deque
import time
import copy
import os

def is_completed(base_map, obj_map):
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            if base_map[y][x] == "." and obj_map[y][x] != "$":
                return False
    return True

def find_player(obj_map):
    for y, row in enumerate(obj_map):
        for x, cell in enumerate(row):
            if cell == "@":
                return x, y
    return -1, -1

def move(base_map, obj_map, dx, dy):
    x, y = find_player(obj_map)
    nx, ny = x + dx, y + dy
    nnx, nny = x + dx*2, y + dy*2
    if obj_map[ny][nx] == " " and base_map[ny][nx] != "#":
        obj_map[y][x] = " "
        obj_map[ny][nx] = "@"
        return True
    elif obj_map[ny][nx] == "$" and base_map[nny][nnx] != "#" and obj_map[nny][nnx] == " ":
        obj_map[y][x] = " "
        obj_map[ny][nx] = "@"
        obj_map[nny][nnx] = "$"
        return True
    return False

def bfs(base_map, obj_map):
    def serialize(obj_map):
        return tuple(tuple(row) for row in obj_map)

    def get_moves():
        return [(-1, 0, "L"), (1, 0, "R"), (0, -1, "U"), (0, 1, "D")]

    visited = set()
    queue = deque()
    start_time = time.time()

    initial_state = copy.deepcopy(obj_map)
    queue.append((initial_state, []))
    visited.add(serialize(initial_state))

    node_generated = 1
    node_repeated = 0

    while queue:
        state, path = queue.popleft()
        if is_completed(base_map, state):
            duration = time.time() - start_time
            write_bfs_output(path, node_generated, node_repeated, duration)
            return path

        for dx, dy, move_char in get_moves():
            new_state = copy.deepcopy(state)
            moved = move(base_map, new_state, dx, dy)
            if moved:
                s = serialize(new_state)
                if s not in visited:
                    visited.add(s)
                    queue.append((new_state, path + [(dx, dy, move_char)]))
                    node_generated += 1
                else:
                    node_repeated += 1

    duration = time.time() - start_time
    return None

def write_bfs_output(path, node_generated, node_repeated, duration):
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("===== BFS Result =====\n")
        f.write("Solution: {}\n".format("".join(move for _, _, move in path)))
        f.write("Steps: {}\n".format(len(path)))
        f.write("Nodes Generated: {}\n".format(node_generated))
        f.write("Nodes Repeated: {}\n".format(node_repeated))
        f.write("Duration: {:.6f} seconds\n".format(duration))
