import pygame
import os

TILE_SIZE = 48

SYMBOLS = {
    "#": "wall.png",
    " ": "floor.png",
    ".": "goal.png",
    "@": "player.png",
    "+": "player.png",
    "$": "box.png",
    "*": "box_on_goal.png"
}

def load_images():
    images = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    for symbol, filename in SYMBOLS.items():
        path = os.path.join(base_path, "img", filename)
        try:
            images[symbol] = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))
        except pygame.error:
            images[symbol] = pygame.Surface((TILE_SIZE, TILE_SIZE))
    return images


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
        for x, cell in enumerate(row):
            if cell == "@":
                return x, y
    return -1, -1

def move(base_map, obj_map, dx, dy):
    x, y = find_player(obj_map)
    nx, ny = x + dx, y + dy
    nnx, nny = x + dx*2, y + dy*2
    if 0 <= ny < len(obj_map) and 0 <= nx < len(obj_map[0]):
        if obj_map[ny][nx] == " " and base_map[ny][nx] != "#":
            obj_map[y][x] = " "
            obj_map[ny][nx] = "@"
        elif obj_map[ny][nx] == "$":
            if 0 <= nny < len(obj_map) and 0 <= nnx < len(obj_map[0]):
                if base_map[nny][nnx] != "#" and obj_map[nny][nnx] == " ":
                    obj_map[y][x] = " "
                    obj_map[ny][nx] = "@"
                    obj_map[nny][nnx] = "$"

def is_completed(base_map, obj_map):
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            if base_map[y][x] == "." and obj_map[y][x] != "$":
                return False
    return True

def draw_map(screen, base_map, obj_map, images):
    screen.fill((128, 160, 166))
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            base = base_map[y][x]
            obj = obj_map[y][x]

            if base != "#":
                screen.blit(images[" "], (x * TILE_SIZE, y * TILE_SIZE))
            else:
                screen.blit(images["#"], (x * TILE_SIZE, y * TILE_SIZE))

            if base == ".":
                screen.blit(images["."], (x * TILE_SIZE, y * TILE_SIZE))

            if base == "." and obj == "$":
                screen.blit(images["*"], (x * TILE_SIZE, y * TILE_SIZE))
            elif base == "." and obj == "@":
                screen.blit(images["+"], (x * TILE_SIZE, y * TILE_SIZE))
            elif obj.strip() != "" and obj in images:
                screen.blit(images[obj], (x * TILE_SIZE, y * TILE_SIZE))


pygame.init()

level_data = [
    "#####",
    "# @ #",
    "# $ #",
    "# . #",
    "#####"
]

base_map, obj_map = split_maps(level_data)
images = load_images()

WIDTH = len(base_map[0]) * TILE_SIZE
HEIGHT = len(base_map) * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(base_map, obj_map, 0, -1)
            elif event.key == pygame.K_DOWN:
                move(base_map, obj_map, 0, 1)
            elif event.key == pygame.K_LEFT:
                move(base_map, obj_map, -1, 0)
            elif event.key == pygame.K_RIGHT:
                move(base_map, obj_map, 1, 0)

    screen.fill((0, 0, 0))
    draw_map(screen, base_map, obj_map, images)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()