import pygame
import sys
from game import run_game, load_levels_from_file

# Cấu hình
pygame.init()
WIDTH, HEIGHT = 500, 600
WHITE, BLACK, GRAY, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 102, 204)
FONT = pygame.font.SysFont(None, 32)

# Cửa sổ chính
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chọn Level")

# Load level từ file
levels = load_levels_from_file("Sokoban_AI/maps.txt")

# Tạo nút
def create_buttons():
    buttons = []
    margin = 20
    button_width = WIDTH - 2 * margin
    button_height = 50
    spacing = 15
    for i in range(len(levels)):
        x = margin
        y = 100 + i * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((rect, f"Level {i+1}"))
    return buttons

def draw_menu(buttons, mouse_pos):
    screen.fill(WHITE)
    title = FONT.render("CHỌN LEVEL", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    for rect, label in buttons:
        color = BLUE if rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text = FONT.render(label, True, WHITE)
        screen.blit(text, (rect.x + 20, rect.y + 10))

    pygame.display.flip()

def main_menu():
    buttons = create_buttons()
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        draw_menu(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(mouse_pos):
                        run_game(i)
                        pygame.display.set_mode((WIDTH, HEIGHT))  # Quay lại menu sau game

if __name__ == "__main__":
    main_menu()
