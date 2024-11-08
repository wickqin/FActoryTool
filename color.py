import glob
import os
import random
import pygame
import sys
import tkinter as TK


def initialize_pygame(width, height):
    pygame.init()
    display_surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    return display_surface


def random_block(display_surface, width, height, color):
    block_x_location = random.randint(0, width - 100)
    block_y_location = random.randint(0, height - 100)
    block_rect = pygame.draw.rect(display_surface, color, (block_x_location, block_y_location, 100, 100))
    return block_rect


def get_deeper_color(color):
    r, g, b = color
    new_r = max(r - 50, 0)
    new_g = max(g - 50, 0)
    new_b = max(b - 50, 0)
    return new_r, new_g, new_b


def main_loop(screen, colors):
    current_color_index = 0
    running = True
    block_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    with open('filed.txt', 'w') as f:
                        f.write('filed')
                    pygame.quit()
                    sys.exit(1)
                elif event.key == pygame.K_RETURN or event.keycode == 13:
                    current_color_index = (current_color_index + 1) % len(colors)
                    if current_color_index == 1:
                        screen.fill(colors[current_color_index])
                        deeper_color = get_deeper_color(colors[current_color_index])
                        block_rect = random_block(screen, screen.get_width(), screen.get_height(), deeper_color)
            elif event.type == pygame.MOUSEBUTTONDOWN and block_rect and block_rect.collidepoint(event.pos):
                current_color_index = (current_color_index + 1) % len(colors)
                if current_color_index == 0:
                    with open('pass.txt', 'w') as f:
                        f.write('pass')
                    pygame.time.wait(1000)
                    pygame.quit()
                    sys.exit(0)
                else:
                    screen.fill(colors[current_color_index])
                    deeper_color = get_deeper_color(colors[current_color_index])
                    block_rect = random_block(screen, screen.get_width(), screen.get_height(), deeper_color)

        if not block_rect:
            screen.fill(colors[current_color_index])
            if current_color_index == 0:
                font = pygame.font.SysFont(None, 55)
                text_surface = font.render("Click Color_Block To Test. Press ESC To Exit.", True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(text_surface, text_rect)
            deeper_color = get_deeper_color(colors[current_color_index])
            block_rect = random_block(screen, screen.get_width(), screen.get_height(), deeper_color)

        pygame.display.flip()


if __name__ == "__main__":
    for txt_file in glob.glob('*.txt'):
        os.remove(txt_file)

    root = TK.Tk()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    screen = initialize_pygame(screen_width, screen_height)

    colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    main_loop(screen, colors)
