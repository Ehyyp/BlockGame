import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os

root = tk.Tk()
root.geometry("400x200")
root.resizable(False, False)
root.title("Palikkapeli")

custom_font = tkFont.Font(family="Arial", size=25)

message = tk.Label(root, text="Select stage", font=custom_font)
speedSlider = ttk.Scale(root, from_=0, to=100, orient='horizontal')

def run():
    speed = speedSlider.get() / 1000
    if speed == 0:
        speed = 0.02
    os.system(f"python dodging_game.py {speed:.2f}")

stage1 = ttk.Button(root, text="Stage 1", command=run)

message.pack()
speedSlider.pack()
stage1.pack(ipadx=20, ipady=20, expand=True)

root.mainloop()