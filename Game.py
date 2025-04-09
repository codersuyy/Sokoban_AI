import pygame
import sys

TILE_SIZE = 48
FONT_NAME = "freesansbold.ttf"

SYMBOLS = {
    "#": "wall.png",
    " ": "floor.png",
    ".": "goal.png",
    "@": "player.png",
    "+": "player_on_goal.png",
    "$": "box.png",
    "*": "box_on_goal.png"
}

def load_levels(filename):
    with open(filename, "r") as f:
        raw = f.read()
    raw_levels = raw.strip().split("--")
    levels = []
    for level in raw_levels:
        rows = level.strip().splitlines()
        max_len = max(len(row) for row in rows)
        rows = [row.ljust(max_len) for row in rows]
        levels.append(rows)
    return levels

def split_maps(level_data):
    base_map = []
    obj_map = []
    for row in level_data:
        base_row = []
        obj_row = []
        for ch in row:
            if ch == "#":
                base_row.append("#")
                obj_row.append(" ")
            elif ch == ".":
                base_row.append(".")
                obj_row.append(" ")
            elif ch == "@":
                base_row.append(" ")
                obj_row.append("@")
            elif ch == "+":
                base_row.append(".")
                obj_row.append("@")
            elif ch == "$":
                base_row.append(" ")
                obj_row.append("$")
            elif ch == "*":
                base_row.append(".")
                obj_row.append("$")
            else:
                base_row.append(" ")
                obj_row.append(" ")
        base_map.append(base_row)
        obj_map.append(obj_row)
    return base_map, obj_map

def find_player(obj_map):
    for y, row in enumerate(obj_map):
        for x, val in enumerate(row):
            if val == "@":
                return x, y
    return -1, -1

def is_completed(base_map, obj_map):
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            if base_map[y][x] == "." and obj_map[y][x] != "$":
                return False
    return True

def draw_map(screen, base_map, obj_map, images):
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            base = base_map[y][x]
            obj = obj_map[y][x]
            if base == "." and obj == "$":
                img = images["*"]
            elif base == "." and obj == "@":
                img = images["+"]
            elif obj in images:
                img = images[obj]
            else:
                img = images.get(base, images[" "])
            screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

def move_player(base_map, obj_map, dx, dy):
    x, y = find_player(obj_map)
    nx, ny = x + dx, y + dy
    nnx, nny = x + dx * 2, y + dy * 2
    target = obj_map[ny][nx]
    if target == " ":
        obj_map[y][x] = " "
        obj_map[ny][nx] = "@"
    elif target == "$":
        if obj_map[nny][nnx] == " " and base_map[nny][nnx] != "#":
            obj_map[y][x] = " "
            obj_map[ny][nx] = "@"
            obj_map[nny][nnx] = "$"

def play_level(level_data):
    pygame.init()
    base_map, obj_map = split_maps(level_data)
    width, height = len(base_map[0]), len(base_map)
    screen = pygame.display.set_mode((width * TILE_SIZE, height * TILE_SIZE))
    pygame.display.set_caption("Sokoban")
    clock = pygame.time.Clock()

    images = {}
    for k, filename in SYMBOLS.items():
        path = "img/" + filename
        images[k] = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_map(screen, base_map, obj_map, images)
        pygame.display.flip()

        if is_completed(base_map, obj_map):
            pygame.time.wait(500)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    move_player(base_map, obj_map, -1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    move_player(base_map, obj_map, 1, 0)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    move_player(base_map, obj_map, 0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    move_player(base_map, obj_map, 0, 1)
        clock.tick(60)

if __name__ == "__main__":
    levels = load_levels("levels.txt")
    play_level(levels[0])
