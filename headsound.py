import os
import tkinter as tk
from idlelib.pyparse import trans

import pygame
import random
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# print(os.environ.get('SDL_AUDIODRIVER'))
# os.environ['SDL_AUDIODRIVER'] = 'alsa'

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

SOUND_PATH = "./random_wav"
AUDIO_EXTENSION = ".wav"

root = tk.Tk()
root.title("Audio Test By LesliesChen 1.0")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 1 / 3)
window_height = int(screen_height * 1 / 5)

root.geometry(f"{window_width}x{window_height}")
root.resizable(True, True)


def play_audio(side, num):
    file_path = os.path.join(SOUND_PATH, f"{side}{num}{AUDIO_EXTENSION}")
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    root.title(f"Audio Test {side.capitalize()} Channel By LesliesChen 1.0")
    while pygame.mixer.music.get_busy():
        root.update_idletasks()
        root.update()


def check_answer(button_num):
    global last_played, game_started, current_side
    if game_started:
        if current_side == "left":
            if button_num == last_played[0]:
                print("Left Correct!")
                current_side = "right"
                play_audio("R", last_played[1])
            else:
                print("Wrong! Replaying left audio.")
                play_audio("L", last_played[0])
        elif current_side == "right":
            if button_num == last_played[1]:
                print("Right Correct!")
                game_started = False
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                root.after(3000, root.destroy)
                sys.exit(0)
            else:
                print("Wrong! Starting over.")
                game_started = False
                start_game()


buttons = []
for i in range(10):
    button = tk.Button(root, text=str(i), width=5, height=2, state=tk.DISABLED, command=lambda num=i: check_answer(num))
    button.grid(row=i // 5, column=(i % 5), padx=20, pady=20)
    buttons.append(button)


def start_game():
    global last_played, game_started, current_side
    left_num = random.randint(0, 9)
    right_num = random.randint(0, 9)
    last_played = (left_num, right_num)
    current_side = "left"
    play_audio("L", left_num)
    game_started = True
    for button in buttons:
        button.config(state=tk.NORMAL)


def on_closing():
    sys.exit(1)


last_played = None
game_started = False
current_side = ""

root.after(100, start_game)
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
