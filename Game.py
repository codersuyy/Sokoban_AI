import pygame

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 400, 600
TILE_SIZE = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Sokoban")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load hình ảnh
player_img = pygame.image.load(r"Sokoban_AI/character.png")  # Nhân vật
box_img = pygame.image.load(r"Sokoban_AI/box.png")  # Hộp
tile_img = pygame.image.load(r"Sokoban_AI/tile.png")  # Gạch nền
wall_img = pygame.image.load(r"Sokoban_AI/wall.png")  # Tường
target_img = pygame.image.load(r"Sokoban_AI/goal.png")  # Điểm đích
box_target_img = pygame.image.load(r"Sokoban_AI/box.png")  # Hộp trên điểm đích

# Điều chỉnh kích thước ảnh
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
box_img = pygame.transform.scale(box_img, (TILE_SIZE, TILE_SIZE))
tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
target_img = pygame.transform.scale(target_img, (TILE_SIZE, TILE_SIZE))
box_target_img = pygame.transform.scale(box_target_img, (TILE_SIZE, TILE_SIZE))

# Cập nhật bản đồ có điểm đích "T"
level_map = [
    ["W", "W", "W", "W", "W"],
    ["W", ".", ".", "T", "W"],
    ["W", ".", "B", ".", "W"],
    ["W", ".", "P", ".", "W"],
    ["W", "W", "W", "W", "W"],
]

# Hàm vẽ thanh điều khiển
def draw_top_bar():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    font = pygame.font.Font(None, 30)
    text = font.render("LEVEL 1", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 40, 15))

# Hàm vẽ bàn chơi
def draw_board():
    for row in range(len(level_map)):
        for col in range(len(level_map[row])):
            x, y = col * TILE_SIZE, row * TILE_SIZE + 50
            if level_map[row][col] == "W":
                screen.blit(wall_img, (x, y))
            elif level_map[row][col] == ".":
                screen.blit(tile_img, (x, y))
            elif level_map[row][col] == "T":
                screen.blit(target_img, (x, y))
            elif level_map[row][col] == "B":
                screen.blit(tile_img, (x, y))
                screen.blit(box_img, (x, y))
            elif level_map[row][col] == "P":
                screen.blit(tile_img, (x, y))
                screen.blit(player_img, (x, y))

# Vòng lặp game
running = True
while running:
    screen.fill(WHITE)
    draw_top_bar()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
