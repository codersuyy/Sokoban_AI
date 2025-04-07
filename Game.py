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
player_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/character.png"), (TILE_SIZE, TILE_SIZE))
box_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/box.png"), (TILE_SIZE, TILE_SIZE))
tile_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/tile.png"), (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/wall.png"), (TILE_SIZE, TILE_SIZE))
target_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/goal.png"), (TILE_SIZE, TILE_SIZE))
box_target_img = box_img  # Nếu có hình riêng cho box + goal thì thay ở đây

# Bản đồ nền để nhớ ô gốc (".", "T", "W")
level_map_base = [
    ["W", "W", "W", "W", "W"],
    ["W", ".", ".", "T", "W"],
    ["W", ".", ".", ".", "W"],
    ["W", ".", ".", ".", "W"],
    ["W", "W", "W", "W", "W"],
]

# Bản đồ động hiển thị vật thể (người, hộp)
level_map = [
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "B", "", ""],
    ["", "", "P", "", ""],
    ["", "", "", "", ""],
]

# Tìm vị trí người chơi
def find_player():
    for r in range(len(level_map)):
        for c in range(len(level_map[r])):
            if level_map[r][c] == "P":
                return r, c
    return None

# Di chuyển người chơi
def move(dx, dy):
    px, py = find_player()
    nx, ny = px + dy, py + dx
    bx, by = nx + dy, ny + dx

    if level_map_base[nx][ny] == "W":
        return  # Không đi vào tường

    if level_map[nx][ny] == "B":
        if level_map_base[bx][by] != "W" and level_map[bx][by] == "":
            level_map[bx][by] = "B"
            level_map[nx][ny] = "P"
            level_map[px][py] = ""
    elif level_map[nx][ny] == "":
        level_map[nx][ny] = "P"
        level_map[px][py] = ""

# Vẽ thanh tiêu đề
def draw_top_bar():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    font = pygame.font.Font(None, 30)
    text = font.render("LEVEL 1", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 40, 15))

# Vẽ bàn chơi
def draw_board():
    for r in range(len(level_map_base)):
        for c in range(len(level_map_base[r])):
            x, y = c * TILE_SIZE, r * TILE_SIZE + 50

            base_tile = level_map_base[r][c]
            if base_tile == "W":
                screen.blit(wall_img, (x, y))
            elif base_tile == ".":
                screen.blit(tile_img, (x, y))
            elif base_tile == "T":
                screen.blit(target_img, (x, y))

            obj = level_map[r][c]
            if obj == "B":
                if base_tile == "T":
                    screen.blit(box_target_img, (x, y))
                else:
                    screen.blit(box_img, (x, y))
            elif obj == "P":
                screen.blit(player_img, (x, y))

# Kiểm tra thắng game
def check_win():
    for r in range(len(level_map)):
        for c in range(len(level_map[r])):
            if level_map_base[r][c] == "T" and level_map[r][c] != "B":
                return False
    return True

# Vòng lặp chính
running = True
won = False
while running:
    screen.fill(WHITE)
    draw_top_bar()
    draw_board()

    if check_win():
        font = pygame.font.Font(None, 40)
        text = font.render("YOU WIN!", True, (0, 200, 0))
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))
        won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not won:
            if event.key == pygame.K_LEFT:
                move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move(1, 0)
            elif event.key == pygame.K_UP:
                move(0, -1)
            elif event.key == pygame.K_DOWN:
                move(0, 1)

    pygame.display.update()

pygame.quit()
