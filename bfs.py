from collections import deque

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
    queue.append((obj_map, []))
    visited.add(serialize(obj_map))

    while queue:
        state, path = queue.popleft()
        if is_completed(base_map, state):
            return path

        for dx, dy, move_char in get_moves():
            new_state = [row[:] for row in state]
            moved = move(base_map, new_state, dx, dy)
            if moved:
                s = serialize(new_state)
                if s not in visited:
                    visited.add(s)
                    queue.append((new_state, path + [(dx, dy, move_char)]))
    return "No Solution"