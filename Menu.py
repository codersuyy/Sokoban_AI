import pygame
import sys

pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LOCKED_COLOR = (150, 150, 150)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font chữ
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 40)

# Danh sách các màn chơi và trạng thái khóa
levels = [True] + [False] * 9  # Chỉ màn đầu tiên được mở khóa

# Bản đồ mẫu cho các màn chơi
level_maps = [
    [
        "#####",
        "#.O.#",
        "#.P.#",
        "#####"
    ],
    [
        "#####",
        "#P O#",
        "#. .#",
        "#####"
    ]
]

# Ký hiệu bản đồ
WALL = "#"
PLAYER = "P"
BOX = "O"
GOAL = "."
EMPTY = " "

def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))

def main_menu():
    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        draw_text("SOKOBAN", font, BLACK, SCREEN_WIDTH // 2, 150)
        
        mouse_pos = pygame.mouse.get_pos()
        
        play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 250, 100, 40)
        instruction_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 350, 150, 40)
        quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 450, 100, 40)
        
        play_color = GRAY if play_rect.collidepoint(mouse_pos) else BLACK
        instruction_color = GRAY if instruction_rect.collidepoint(mouse_pos) else BLACK
        quit_color = GRAY if quit_rect.collidepoint(mouse_pos) else BLACK
        
        draw_text("Play", small_font, play_color, SCREEN_WIDTH // 2, 250)
        draw_text("Instruction", small_font, instruction_color, SCREEN_WIDTH // 2, 350)
        draw_text("Quit", small_font, quit_color, SCREEN_WIDTH // 2, 450)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    level_selection()
                elif instruction_rect.collidepoint(event.pos):
                    instructions()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def level_selection():
    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        draw_text("Select Level", font, BLACK, SCREEN_WIDTH // 2, 80)
        
        mouse_pos = pygame.mouse.get_pos()
        level_buttons = []
        start_x, start_y = 50, 150
        size = 70
        spacing = 20

        for i in range(len(levels)):
            rect = pygame.Rect(start_x + (i % 5) * (size + spacing), 
                               start_y + (i // 5) * (size + spacing), 
                               size, size)
            level_buttons.append(rect)
            color = GREEN if levels[i] else LOCKED_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=10)
            draw_text(str(i + 1), small_font, WHITE, rect.centerx, rect.centery)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(event.pos) and levels[i]:
                        start_level(i)

def start_level(level_index):
    print(f"Starting Level {level_index + 1}")
    play_sokoban(level_maps[level_index])
    levels[min(level_index + 1, len(levels) - 1)] = True

def play_sokoban(level_map):
    running = True
    while running:
        screen.fill(WHITE)
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * 50 + 50, y * 50 + 150, 50, 50)
                if tile == WALL:
                    pygame.draw.rect(screen, BLACK, rect)
                elif tile == PLAYER:
                    pygame.draw.rect(screen, BLUE, rect)
                elif tile == BOX:
                    pygame.draw.rect(screen, BROWN, rect)
                elif tile == GOAL:
                    pygame.draw.rect(screen, RED, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def instructions():
    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        draw_text("Instructions", font, BLACK, SCREEN_WIDTH // 2, 100)
        draw_text("- Use arrow keys to move", small_font, BLACK, SCREEN_WIDTH // 2, 200)
        draw_text("- Push boxes onto goals", small_font, BLACK, SCREEN_WIDTH // 2, 250)
        draw_text("- Press ESC to exit", small_font, BLACK, SCREEN_WIDTH // 2, 300)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

main_menu()
