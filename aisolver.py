import heapq
from collections import deque
import copy

# ======== Helper functions ===========
def read_levels(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return [level.splitlines() for level in content.strip().split('\n\n')]

def parse_map(raw_map):
    base_map = []
    obj_map = []
    for line in raw_map:
        base_line = ""
        obj_line = ""
        for ch in line:
            if ch in "# ":
                base_line += ch
                obj_line += ' '
            elif ch == ".":
                base_line += '.'
                obj_line += ' '
            elif ch == "@":
                base_line += ' '
                obj_line += '@'
            elif ch == "+":
                base_line += '.'
                obj_line += '@'
            elif ch == "$":
                base_line += ' '
                obj_line += '$'
            elif ch == "*":
                base_line += '.'
                obj_line += '$'
            else:
                base_line += ' '
                obj_line += ' '
        base_map.append(base_line)
        obj_map.append(obj_line)
    return base_map, obj_map

def find_player_and_boxes(obj_map):
    boxes = set()
    for y, row in enumerate(obj_map):
        for x, ch in enumerate(row):
            if ch == '@':
                player = (y, x)
            elif ch == '$':
                boxes.add((y, x))
    return player, boxes

def is_goal(boxes, base_map):
    for y, row in enumerate(base_map):
        for x, ch in enumerate(row):
            if ch == '.' and (y, x) not in boxes:
                return False
    return True

def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic(boxes, base_map):
    goals = [(y, x) for y, row in enumerate(base_map) for x, ch in enumerate(row) if ch == '.']
    total = 0
    for box in boxes:
        dists = [manhattan_dist(box, goal) for goal in goals]
        total += min(dists)
    return total

def get_neighbors(pos):
    y, x = pos
    return [(y-1, x, 'U'), (y+1, x, 'D'), (y, x-1, 'L'), (y, x+1, 'R')]

def is_free(y, x, base_map, boxes):
    return base_map[y][x] != '#' and (y, x) not in boxes

# ========= A* Solver =============
def a_star_solver(base_map, obj_map):
    start_player, start_boxes = find_player_and_boxes(obj_map)
    visited = set()
    heap = []
    heapq.heappush(heap, (0 + heuristic(start_boxes, base_map), 0, start_player, frozenset(start_boxes), ""))

    while heap:
        f, g, player, boxes, path = heapq.heappop(heap)
        if (player, boxes) in visited:
            continue
        visited.add((player, boxes))

        if is_goal(boxes, base_map):
            return path

        for dy, dx, move in get_neighbors(player):
            new_player = (dy, dx)

            if new_player in boxes:
                # box move
                by, bx = dy + (dy - player[0]), dx + (dx - player[1])
                if is_free(by, bx, base_map, boxes):
                    new_boxes = set(boxes)
                    new_boxes.remove(new_player)
                    new_boxes.add((by, bx))
                    if (new_player, frozenset(new_boxes)) not in visited:
                        cost = g + 1
                        h = heuristic(new_boxes, base_map)
                        heapq.heappush(heap, (cost + h, cost, new_player, frozenset(new_boxes), path + move))
            else:
                # normal move
                if is_free(dy, dx, base_map, boxes):
                    if (new_player, boxes) not in visited:
                        cost = g + 1
                        h = heuristic(boxes, base_map)
                        heapq.heappush(heap, (cost + h, cost, new_player, boxes, path + move))
    return "No solution"

# ========= MAIN TEST ============
if __name__ == "__main__":
    level_list = read_levels("AI/Sokoban_AI/levels.txt")
    level_index = 8  # bạn có thể đổi số level ở đây

    base_map, obj_map = parse_map(level_list[level_index])
    solution = a_star_solver(base_map, obj_map)
    print("Giải pháp:", solution)
