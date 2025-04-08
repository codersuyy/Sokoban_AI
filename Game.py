import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Sokoban")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (40, 40, 200)

font_title = pygame.font.SysFont(None, 60)
font_option = pygame.font.SysFont(None, 36)
font_text = pygame.font.SysFont(None, 28)
font_back = pygame.font.SysFont(None, 32)

menu_items = ["Play", "Instruction", "Quit"]


def render_menu(highlight_index=None):
    screen.fill(WHITE)

    # Title
    title_surface = font_title.render("SOKOBAN", True, BLACK)
    screen.blit(title_surface, (
        screen.get_width() // 2 - title_surface.get_width() // 2, 100))

    # Menu items
    for i, item in enumerate(menu_items):
        color = GRAY if i == highlight_index else BLACK
        text_surface = font_option.render(item, True, color)
        x = screen.get_width() // 2 - text_surface.get_width() // 2
        y = 200 + i * 60
        screen.blit(text_surface, (x, y))

    pygame.display.flip()


def get_hovered_index(pos):
    for i, item in enumerate(menu_items):
        text_surface = font_option.render(item, True, BLACK)
        x = screen.get_width() // 2 - text_surface.get_width() // 2
        y = 200 + i * 60
        w, h = text_surface.get_size()
        rect = pygame.Rect(x, y, w, h)
        if rect.collidepoint(pos):
            return i
    return None


def show_instructions():
    pygame.display.set_caption("Instructions")

    instructions = [
        "How to Play Sokoban:",
        "- Use arrow keys or WASD to move your character.",
        "- Push all the boxes onto the target spots (marked with circles).",
        "- You can only push boxes — not pull them.",
        "- Use the 'U' key to undo your last move.",
        "- Press 'R' to reset the level and try again.",
        "Tip: Think ahead! You can get stuck easily.",
        "Your goal is to place all boxes correctly with the fewest moves.",
    ]

    back_text = "Back"
    back_rect = None

    def render(back_hovered=False):
        screen.fill(WHITE)

        # Title
        title_surf = font_title.render("INSTRUCTIONS", True, BLACK)
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 40))

        # Instruction body
        y = 110
        margin_x = 20
        line_spacing = 28

        for line in instructions:
            if len(line) == 0:
                y += line_spacing
                continue

            words = line.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                test_surface = font_text.render(test_line, True, BLACK)
                if test_surface.get_width() > screen.get_width() - 2 * margin_x:
                    surface = font_text.render(current_line.strip(), True, BLACK)
                    screen.blit(surface, (margin_x, y))
                    y += line_spacing
                    current_line = word + " "
                else:
                    current_line = test_line
            if current_line:
                surface = font_text.render(current_line.strip(), True, BLACK)
                screen.blit(surface, (margin_x, y))
                y += line_spacing

        # Back button
        nonlocal back_rect
        color = BLUE if back_hovered else BLACK
        back_surf = font_back.render(back_text, True, color)
        back_x = 20
        back_y = screen.get_height() - 60
        screen.blit(back_surf, (back_x, back_y))
        back_rect = pygame.Rect(back_x, back_y, back_surf.get_width(), back_surf.get_height())

        pygame.display.flip()

    render()

    # Wait for user to click "Back"
    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            if back_rect and back_rect.collidepoint(event.pos):
                render(back_hovered=True)
            else:
                render(back_hovered=False)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and back_rect and back_rect.collidepoint(event.pos):
                break


def main_menu():
    highlight = None
    render_menu()

    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            hovered = get_hovered_index(event.pos)
            if hovered != highlight:
                highlight = hovered
                render_menu(highlight)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_index = get_hovered_index(event.pos)
            if clicked_index is not None:
                choice = menu_items[clicked_index]
                if choice == "Play":
                    print("➡ Enter level selection (to be implemented)")
                    # You can call show_level_selection() here in future
                elif choice == "Instruction":
                    show_instructions()
                    render_menu(highlight)
                elif choice == "Quit":
                    pygame.quit()
                    sys.exit()


# Start the program
main_menu()
