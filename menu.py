import pygame
import os
import sys

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")
FONT = pygame.font.SysFont("arial", 24)


def draw_text_center(text, y, font, color=(0, 0, 0)):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)



def load_levels():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    
def level_select():
    levels = load_levels()
    unlocked = 1
    try:
        with open("progress.txt", "r") as f:
            unlocked = int(f.read().strip())
    except:
        pass
    buttons = []
    for i in range(20):
        x = 50 + (i % 5) * 60
        y = 100 + (i // 5) * 60
        rect = pygame.Rect(x, y, 50, 50)
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
                    return
                for rect, num in buttons:
                    if rect.collidepoint(event.pos) and num <= unlocked and num <= len(levels):
                        play_level(levels[num - 1], num, unlocked)
                        return

def play_level(level_str, level_num, unlocked):
    while True:
        screen.fill((255, 255, 255))
        draw_text_center(f"Level {level_num} complete!", HEIGHT // 2 - 30, FONT)
        draw_text_center("Click to return to level select", HEIGHT // 2 + 30, FONT)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
