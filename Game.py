import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Sokoban")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (90, 90, 90)
GREEN = (100, 200, 100)
BLUE = (40, 40, 200)

font_title = pygame.font.SysFont(None, 40)
font_number = pygame.font.SysFont(None, 28)
font_back = pygame.font.SysFont(None, 30)

level_rects = []
unlocked_levels = 1
total_levels = 0
levels_data = []

if os.path.exists("levels.txt"):
    with open("levels.txt", "r") as f:
        levels_data = [line.strip() for line in f if line.strip()]
    total_levels = len(levels_data)
else:
    print("Missing levels.txt")
    pygame.quit()
    sys.exit()

def draw_level_selection(highlighted=None, back_hover=False):
    screen.fill(WHITE)
    title = font_title.render("Select Level", True, BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))
    level_rects.clear()
    start_x = 40
    start_y = 100
    size = 50
    margin = 10
    cols = 5
    for i in range(total_levels):
        row = i // cols
        col = i % cols
        x = start_x + col * (size + margin)
        y = start_y + row * (size + margin)
        if i + 1 <= unlocked_levels:
            color = GREEN if i == highlighted else WHITE
            border = BLACK
        else:
            color = GRAY
            border = DARK_GRAY
        pygame.draw.rect(screen, color, (x, y, size, size))
        pygame.draw.rect(screen, border, (x, y, size, size), 2)
        label = font_number.render(str(i + 1), True, BLACK)
        screen.blit(label, (x + size // 2 - label.get_width() // 2, y + size // 2 - label.get_height() // 2))
        level_rects.append(pygame.Rect(x, y, size, size))
    back_text = font_back.render("← Back", True, BLUE if back_hover else BLACK)
    screen.blit(back_text, (20, screen.get_height() - 50))
    global back_rect
    back_rect = pygame.Rect(20, screen.get_height() - 50, back_text.get_width(), back_text.get_height())
    pygame.display.flip()

def select_level():
    current_hover = None
    back_hover = False
    draw_level_selection()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            hover_index = None
            for i, rect in enumerate(level_rects):
                if rect.collidepoint(event.pos):
                    hover_index = i if i + 1 <= unlocked_levels else None
                    break
            back_hover = back_rect.collidepoint(event.pos)
            if hover_index != current_hover:
                current_hover = hover_index
                draw_level_selection(current_hover, back_hover)
            elif back_rect.collidepoint(event.pos) != back_hover:
                draw_level_selection(current_hover, back_hover)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if back_rect.collidepoint(event.pos):
                    break
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(event.pos) and i + 1 <= unlocked_levels:
                        print(f"Playing level {i + 1}: {levels_data[i]}")
                        complete_level(i)

def complete_level(index):
    global unlocked_levels
    if index + 2 > unlocked_levels and index + 1 < total_levels:
        unlocked_levels = index + 2
    select_level()

select_level()
