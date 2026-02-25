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
gamePath = os.path.join('src', 'gameGraphics.py')

# Headline font
custom_font = tkFont.Font(family="Arial", size=25)

# Headline message
message = tk.Label(root, text="Select stage", font=custom_font)

# Slider info
sliderMessage = tk.Label(root, text="Game speed")

# Slider to choose stage speed
speedSlider = ttk.Scale(root, from_=0, to=100, orient='horizontal')

# Run stage 1
def runStage1():
    # Get speed from slider and scale to game speeds
    speed = round(speedSlider.get() / 1000, 2)
    # Default speed if slider was not moved
    if speed == 0:
        speed = 0.02

    # Run stage
    subprocess.call(["python", gamePath, str(speed), "stage1"])

# Run stage 2
def runStage2():
    # Get speed from slider and scale to game speeds
    speed = round(speedSlider.get() / 1000, 2)
    # Default speed if slider was not moved
    if speed == 0:
        speed = 0.02

    # Run stage
    subprocess.call(["python", gamePath, str(speed), "stage2"])

# Stage 1 run button
stage1 = ttk.Button(root, text="Stage 1", command=runStage1)
# Stage 2 run button
stage2 = ttk.Button(root, text="Stage 2", command=runStage2)

# Pack message, slider and buttons
message.pack()
sliderMessage.pack()
speedSlider.pack()
stage1.pack(ipadx=20, ipady=20, expand=True)
stage2.pack(ipadx=20, ipady=20, expand=True)

# Mainloop
root.mainloop()