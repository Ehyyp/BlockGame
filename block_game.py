"""
Defines Graphical User Interface (GUI) for the block game.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
import subprocess

# Initialize window
root = tk.Tk()
root.geometry("400x200")
root.resizable(False, False)
root.title("Palikkapeli")

# Set OS-agnostic game path
game_path = os.path.join('src', 'runGame.py')

# Headline font
custom_font = tkFont.Font(family="Arial", size=25)

# Headline message
message = tk.Label(root, text="Select stage", font=custom_font)

# Slider info
slider_message = tk.Label(root, text="Game speed")

# Slider to choose stage speed
speed_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal')

def run_stage1():
    """
    Run stage 1
    """
    # Get speed from slider and scale to game speeds
    speed = round(speed_slider.get() / 1000, 2)
    # Default speed if slider was not moved
    if speed == 0:
        speed = 0.02

    # Run stage
    subprocess.call(["python", game_path, str(speed), "stage1"])

# Run stage 2
def run_stage2():
    """
    Run stage 2
    """
    # Get speed from slider and scale to game speeds
    speed = round(speed_slider.get() / 1000, 2)
    # Default speed if slider was not moved
    if speed == 0:
        speed = 0.02

    # Run stage
    subprocess.call(["python", game_path, str(speed), "stage2"])

# Stage 1 run button
stage1 = ttk.Button(root, text="Stage 1", command=run_stage1)
# Stage 2 run button
stage2 = ttk.Button(root, text="Stage 2", command=run_stage2)

# Pack message, slider and buttons
message.pack()
slider_message.pack()
speed_slider.pack()
stage1.pack(ipadx=20, ipady=20, expand=True)
stage2.pack(ipadx=20, ipady=20, expand=True)

# Mainloop
root.mainloop()
