import pygame

# ====== Đọc file bản đồ từ maps.txt ======
def load_levels_from_file(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    levels = []
    current_level = []
    max_cols = 0

    for line in lines:
        if line.strip() == "":
            if current_level:
                # Chuẩn hóa độ dài dòng
                for row in current_level:
                    row.extend(['.'] * (max_cols - len(row)))
                levels.append(current_level)
                current_level = []
                max_cols = 0
        else:
            row = list(line)
            max_cols = max(max_cols, len(row))
            current_level.append(row)

    if current_level:
        for row in current_level:
            row.extend(['.'] * (max_cols - len(row)))
        levels.append(current_level)

    return levels


# ====== Menu chọn level ======
def show_level_menu(level_count):
    print("Chọn level để chơi:")
    for i in range(level_count):
        print(f"{i + 1}. Level {i + 1}")
    while True:
        try:
            choice = int(input("Nhập số level: "))
            if 1 <= choice <= level_count:
                return choice - 1
        except:
            pass
        print("Vui lòng nhập lại.")

# ====== Game chính ======
def run_game(level_map_raw):
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    # Kích thước bản đồ
    rows = len(level_map_raw)
    cols = len(level_map_raw[0])

    # Tính TILE_SIZE trước, rồi suy ra WIDTH/HEIGHT dựa vào số dòng và cột
    TILE_SIZE = min(80, 600 // rows, 400 // cols)  # giới hạn kích thước ô để không quá to
    WIDTH = cols * TILE_SIZE
    HEIGHT = rows * TILE_SIZE + 50  # thêm khoảng top bar 50px

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sokoban")

    # Tải và điều chỉnh kích thước hình ảnh
    player_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/character.png"), (TILE_SIZE, TILE_SIZE))
    box_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/box.png"), (TILE_SIZE, TILE_SIZE))
    tile_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/tile.png"), (TILE_SIZE, TILE_SIZE))
    wall_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/wall.png"), (TILE_SIZE, TILE_SIZE))
    target_img = pygame.transform.scale(pygame.image.load(r"Sokoban_AI/img/goal.png"), (TILE_SIZE, TILE_SIZE))

    # Tạo bản đồ nền & bản đồ đối tượng
    level_map_base = []
    level_map = []
    for row in level_map_raw:
        base_row = []
        obj_row = []
        for cell in row:
            if cell == "W":
                base_row.append("W")
                obj_row.append("")
            elif cell == "T":
                base_row.append("T")
                obj_row.append("")
            elif cell == ".":
                base_row.append(".")
                obj_row.append("")
            elif cell == "B":
                base_row.append(".")
                obj_row.append("B")
            elif cell == "P":
                base_row.append(".")
                obj_row.append("P")
        level_map_base.append(base_row)
        level_map.append(obj_row)

    def find_player():
        for r in range(len(level_map)):
            for c in range(len(level_map[r])):
                if level_map[r][c] == "P":
                    return r, c
        return None

    def move(dx, dy):
        px, py = find_player()
        nx, ny = px + dx, py + dy         # đúng trục (x là hàng, y là cột)
        bx, by = px + 2*dx, py + 2*dy     # vị trí sau thùng

    # Kiểm tra ra ngoài bản đồ
        if not (0 <= nx < len(level_map) and 0 <= ny < len(level_map[0])):
            return
        if level_map_base[nx][ny] == "W":
            return

        if level_map[nx][ny] == "B":
            if not (0 <= bx < len(level_map) and 0 <= by < len(level_map[0])):
                return
            if level_map_base[bx][by] != "W" and level_map[bx][by] == "":
                level_map[bx][by] = "B"
                level_map[nx][ny] = "P"
                level_map[px][py] = ""
        elif level_map[nx][ny] == "":
            level_map[nx][ny] = "P"
            level_map[px][py] = ""

    def draw_top_bar():
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
        font = pygame.font.Font(None, 30)
        text = font.render("SOKOBAN", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 50, 15))

    def draw_board():
        for r in range(len(level_map_base)):
            for c in range(len(level_map_base[r])):
                x, y = c * TILE_SIZE, r * TILE_SIZE + 50
                base = level_map_base[r][c]
                if base == "W":
                    screen.blit(wall_img, (x, y))
                elif base == ".":
                    screen.blit(tile_img, (x, y))
                elif base == "T":
                    screen.blit(target_img, (x, y))

                obj = level_map[r][c]
                if obj == "B":
                    screen.blit(box_img, (x, y))
                elif obj == "P":
                    screen.blit(player_img, (x, y))

    def check_win():
        for r in range(len(level_map)):
            for c in range(len(level_map[r])):
                if level_map_base[r][c] == "T" and level_map[r][c] != "B":
                    return False
        return True

    running, won = True, False
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
                    move(0, -1)    # đi sang trái
                elif event.key == pygame.K_RIGHT:
                    move(0, 1)     # đi sang phải
                elif event.key == pygame.K_UP:
                    move(-1, 0)    # đi lên (giảm hàng)
                elif event.key == pygame.K_DOWN:
                    move(1, 0)     # đi xuống (tăng hàng)


        pygame.display.update()

    pygame.quit()

# ====== Main chạy chương trình ======
if __name__ == "__main__":
    levels = load_levels_from_file("Sokoban_AI/maps.txt")
    level_index = show_level_menu(len(levels))
    run_game(levels[level_index])
