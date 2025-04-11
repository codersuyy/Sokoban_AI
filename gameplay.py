import pygame
import sys
import os
from astar import astar
from bfs import bfs

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")
FONT = pygame.font.SysFont("Arial", 30)
TILE_SIZE = 60
ICON_SIZE = (40, 40)
SYMBOLS = {
    "#": "wall.png",
    " ": "floor.png",
    ".": "goal.png",
    "@": "player.png",
    "+": "player.png",
    "$": "box.png",
    "*": "box_on_goal.png",
}
current_level = ""

def load_images():
    images = {}
    for symbol, filename in SYMBOLS.items():
        path = os.path.join(os.path.dirname(__file__), "img", filename)
        images[symbol] = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))
    return images

def load_icon(name):
    path = os.path.join(os.path.dirname(__file__), "img", name)
    return pygame.transform.scale(pygame.image.load(path), ICON_SIZE)

def load_levels():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels.txt")
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    unlocked = int(lines[0])
    levels = []
    current = []
    for line in lines[1:]:
        if line == "":
            if current:
                levels.append(current)
                current = []
        else:
            current.append(line)
    if current:
        levels.append(current)
    return unlocked, levels

def letaiplay(path, ai_index, base_map, obj_map, move_history, step_counter):
    move_made = False
    if ai_index < len(path):
        direction = path[ai_index]
        if direction == 'L':
            move_made, move_history = move(base_map, obj_map, -1, 0, move_history)
        elif direction == 'R':
            move_made, move_history = move(base_map, obj_map, 1, 0, move_history)
        elif direction == 'U':
            move_made, move_history = move(base_map, obj_map, 0, -1, move_history)
        elif direction == 'D':
            move_made, move_history = move(base_map, obj_map, 0, 1, move_history)
        if move_made:
            step_counter += 1
            ai_index += 1
    return ai_index, move_history, step_counter, obj_map

def handle_mouse_events(event, menu_rect, undo_rect, restart_rect, AI_rect,
                        move_history, base_map, obj_map, level_data,
                        step_counter, ai_path, ai_index, ai_running):
    if menu_rect.collidepoint(event.pos):
        level_select()
        return obj_map, step_counter, move_history, ai_path, ai_index, False

    elif undo_rect.collidepoint(event.pos) and move_history:
        obj_map = move_history.pop()
        step_counter -= 1

    elif restart_rect.collidepoint(event.pos):
        base_map, obj_map = split_maps(level_data)
        move_history.clear()
        step_counter = 0
        ai_path = []
        ai_index = 0
        ai_running = False

    elif AI_rect.collidepoint(event.pos):
        if not ai_running:
            result = bfs(base_map, obj_map)
            if isinstance(result, list):
                ai_path = [step[2] for step in result]
                ai_index = 0
                ai_running = True
            else:
                print("AI không tìm được đường đi.")

    return obj_map, step_counter, move_history, ai_path, ai_index, ai_running

def handle_key_events(event, base_map, obj_map, step_counter, move_history):
    move_made = False
    if event.key == pygame.K_LEFT:
        move_made, move_history = move(base_map, obj_map, -1, 0, move_history)
    elif event.key == pygame.K_RIGHT:
        move_made, move_history = move(base_map, obj_map, 1, 0, move_history)
    elif event.key == pygame.K_UP:
        move_made, move_history = move(base_map, obj_map, 0, -1, move_history)
    elif event.key == pygame.K_DOWN:
        move_made, move_history = move(base_map, obj_map, 0, 1, move_history)
    if move_made:
        step_counter += 1
    return step_counter, move_history

def move(base_map, obj_map, dx, dy, move_history):
    x, y = find_player(obj_map)
    nx, ny = x + dx, y + dy
    nnx, nny = x + dx*2, y + dy*2
    if obj_map[ny][nx] == " " and base_map[ny][nx] != "#":
        move_history.append([row[:] for row in obj_map]) 
        obj_map[y][x] = " "
        obj_map[ny][nx] = "@"
        return True, move_history
    elif obj_map[ny][nx] == "$" and base_map[nny][nnx] != "#" and obj_map[nny][nnx] == " ":
        move_history.append([row[:] for row in obj_map]) 
        obj_map[y][x] = " "
        obj_map[ny][nx] = "@"
        obj_map[nny][nnx] = "$"
        return True, move_history
    return False, move_history

def is_completed(base_map, obj_map):
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            if base_map[y][x] == "." and obj_map[y][x] != "$":
                return False
    return True

def split_maps(level_data):
    base_map = []
    obj_map = []
    mapping = {
        "#": ("#", " "),
        " ": (" ", " "),
        ".": (".", " "),
        "@": (" ", "@"),
        "+": (".", "@"),
        "$": (" ", "$"),
        "*": (".", "$"),
        "!": ("!", " ")
    }
    for row in level_data:
        base_row = []
        obj_row = []
        for ch in row:
            if ch in mapping:
                base_row.append(mapping[ch][0])
                obj_row.append(mapping[ch][1])
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

def draw_map(screen, base_map, obj_map, images):
    screen.fill((128, 160, 166))
    map_width = len(base_map[0]) * TILE_SIZE
    map_height = len(base_map) * TILE_SIZE
    offset_x = (SCREEN_WIDTH - map_width) // 2
    offset_y = (SCREEN_HEIGHT - map_height) // 2
    
    for y in range(len(base_map)):
        for x in range(len(base_map[0])):
            base = base_map[y][x]
            obj = obj_map[y][x]
            draw_x = offset_x + x * TILE_SIZE
            draw_y = offset_y + y * TILE_SIZE
            if base == "!":
                continue
            draw_x = offset_x + x * TILE_SIZE
            draw_y = offset_y + y * TILE_SIZE
            if base == "#":
                draw_tile(screen, images["#"], draw_x, draw_y)
            else:
                draw_tile(screen, images[" "], draw_x, draw_y)
            if base == ".":
                draw_tile(screen, images["."], draw_x, draw_y)
                if obj == "$":
                    draw_tile(screen, images["*"], draw_x, draw_y)
                elif obj == "@":
                    draw_tile(screen, images["+"], draw_x, draw_y)
            elif obj.strip() != "" and obj in images:
                draw_tile(screen, images[obj], draw_x, draw_y)

def draw_ui(screen, step_counter, menu_icon, undo_icon, reset_icon, AI_icon):
    step_text = FONT.render(f"Steps: {step_counter}", True, (0, 0, 0))
    screen.blit(step_text, (100, 20))
    screen.blit(menu_icon, (20,20))
    screen.blit(AI_icon, (SCREEN_WIDTH-175,17))
    screen.blit(undo_icon, (SCREEN_WIDTH-120,20))
    screen.blit(reset_icon, (SCREEN_WIDTH-60,20))

def draw_tile(screen, image, x, y):
    screen.blit(image, (x, y))

def draw_text_center(text, y, font):
    render = font.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(render, rect)

def draw_button(rect, label):
    pygame.draw.rect(screen, (220, 220, 220), rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=10)
    text = pygame.font.SysFont("Arial", 20).render(label, True, (0, 0, 0))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
    
def level_select():
    unlocked, levels = load_levels()
    buttons = []
    button_size = 65
    gap = 10
    cols = 5
    rows = 4
    total_width = cols * button_size + (cols - 1) * gap 
    total_height = rows * button_size + (rows - 1) * gap
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - total_height) // 2

    for i in range(25):
        x = start_x + (i % cols) * (button_size + gap)
        y = start_y + (i // cols) * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
        buttons.append((rect, i + 1))
    back_rect = pygame.Rect(10, 10, 50, 30)
    while True:
        screen.fill((255, 255, 255))
        draw_text_center("Select Level", 50, FONT)
        for rect, num in buttons:
            color = (180, 180, 180) if num > unlocked else (255, 255, 255)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            label = FONT.render(str(num), True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
        pygame.draw.rect(screen, (200, 200, 200), back_rect)
        pygame.draw.polygon(screen, (0, 0, 0), [(25, 25), (40, 15), (40, 35)])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    main_menu()
                for rect, num in buttons:
                    if rect.collidepoint(event.pos) and num <= unlocked and num <= len(levels):
                        play_level(levels[num - 1], num, unlocked)
                        return

def show_level_complete(level_number):
    popup_width = 320
    popup_height = 220
    popup_rect = pygame.Rect(
        (SCREEN_WIDTH - popup_width) // 2,
        (SCREEN_HEIGHT - popup_height) // 2,
        popup_width,
        popup_height)
    menu_rect = pygame.Rect(popup_rect.left + 20, popup_rect.bottom - 70, 80, 40)
    restart_rect = pygame.Rect(popup_rect.left + 120, popup_rect.bottom - 70, 80, 40)
    next_rect = pygame.Rect(popup_rect.left + 220, popup_rect.bottom - 70, 80, 40)
    while True:
        screen.fill((128, 160, 166)) 
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2, border_radius=15)
        title = FONT.render("LEVEL COMPLETE", True, (0, 128, 0))
        screen.blit(title, (popup_rect.centerx - title.get_width() // 2, popup_rect.top + 30))
        level_text = FONT.render(f"Level {level_number}", True, (0, 0, 0))
        screen.blit(level_text, (popup_rect.centerx - level_text.get_width() // 2, popup_rect.top + 80))
        for rect, label in [(menu_rect, "Menu"), (restart_rect, "Restart"), (next_rect, "Next")]:
            draw_button(rect, label)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    level_select()
                    return
                elif restart_rect.collidepoint(event.pos):
                    unlocked, levels = load_levels()
                    play_level(levels[level_number - 1], level_number, unlocked)
                    return
                elif next_rect.collidepoint(event.pos):
                    unlocked, levels = load_levels()
                    if level_number < len(levels):
                        play_level(levels[level_number], level_number + 1, unlocked)
                    else:
                        level_select()
                    return

def play_level(level_data, level_number, unlocked):
    global current_level
    current_level = level_data
    images = load_images()
    menu_icon = load_icon("menu.png")
    undo_icon = load_icon("undo.png")
    reset_icon = load_icon("reset.png")
    AI_icon = load_icon("AI.png")
    
    base_map, obj_map = split_maps(level_data)
    clock = pygame.time.Clock()

    menu_rect = pygame.Rect(20, 20, *ICON_SIZE)
    AI_rect = pygame.Rect(SCREEN_WIDTH - 175, 20, *ICON_SIZE)
    undo_rect = pygame.Rect(SCREEN_WIDTH - 120, 20, *ICON_SIZE)
    restart_rect = pygame.Rect(SCREEN_WIDTH - 60, 20, *ICON_SIZE)

    move_history, ai_path = [], []
    step_counter = ai_index = complete_time =0
    ai_running = completed = False

    while True:
        draw_map(screen, base_map, obj_map, images)
        draw_ui(screen, step_counter, menu_icon, undo_icon, reset_icon, AI_icon)
        pygame.display.flip()
        clock.tick(60)
        if ai_running and ai_index < len(ai_path):
            pygame.time.delay(100)
            ai_index, move_history, step_counter, obj_map = letaiplay(ai_path, ai_index, base_map, obj_map, move_history, step_counter)
        elif ai_running and ai_index >= len(ai_path):
            ai_running = False
        if completed:
            if pygame.time.get_ticks() - complete_time >= 500:
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels.txt")
                if level_number == unlocked and unlocked < 25:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    lines[0] = str(unlocked + 1) + "\n"
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                show_level_complete(level_number)
                return
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                obj_map, step_counter, move_history, ai_path, ai_index, ai_running = handle_mouse_events(
                event, menu_rect, undo_rect, restart_rect, AI_rect,
                move_history, base_map, obj_map, level_data, step_counter, ai_path, ai_index, ai_running)
                if step_counter == 0:
                    completed = False
            if event.type == pygame.KEYDOWN:
                step_counter, move_history = handle_key_events(event, base_map, obj_map, step_counter, move_history)
            if is_completed(base_map, obj_map) and not completed:
                completed = True
                complete_time = pygame.time.get_ticks()

def instruction_screen():
    back_rect = pygame.Rect(10, 10, 50, 30)
    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (200, 200, 200), back_rect)
        pygame.draw.polygon(screen, (0, 0, 0), [(25, 25), (40, 15), (40, 35)])
        lines = [
            "Use arrow keys to move.",
            "Push all boxes onto goals to win.",
        ]
        for i, line in enumerate(lines):
            draw_text_center(line, 150 + i * 40, FONT)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                
def main_menu():
    BIG_FONT = pygame.font.SysFont("arial", 36)
    while True:
        screen.fill((255, 255, 255))
        draw_text_center("SOKOBAN", 100, BIG_FONT)
        draw_text_center("Play", 200, FONT)
        draw_text_center("Instruction", 260, FONT)
        draw_text_center("Quit", 320, FONT)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 160 < y < 240:
                    level_select()
                elif 240 < y < 280:
                    instruction_screen()
                elif 300 < y < 340:
                    pygame.quit()
                    sys.exit()

main_menu()