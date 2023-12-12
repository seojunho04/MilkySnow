import tkinter as tk
from tkinter import *
import subprocess

root = tk.Tk()
root.title("난이도 설정")

button_easy = PhotoImage(file = "Easy.png")
button_normal = PhotoImage(file = "Normal.png")
button_hard = PhotoImage(file = "Hard.png")

windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()

center_width = (windows_width / 2) - 400
center_height = (windows_height / 2) - 400

main_width = 800
main_height = 800

root.geometry(f"{main_width}x{main_height}+{int(center_width)}+{int(center_height)}")

canvas = tk.Canvas(root, width = 800, height=800, highlightthickness=0)

def easy_c():
    root.destroy()
    subprocess.run(["python", "firegame.py", "easy"])

def normal_c():
    root.destroy()
    subprocess.run(["python", "firegame.py", "normal"])

def hard_c():
    root.destroy()
    subprocess.run(["python", "firegame.py", "hard"])

btn_easy = tk.Button(root, image = button_easy, command=easy_c)
btn_easy.place(x=300, y=250)

btn_normal = tk.Button(root, image = button_normal, command=normal_c)
btn_normal.place(x=300, y=400)

btn_hard = tk.Button(root, image = button_hard, command=hard_c)
btn_hard.place(x=300, y=550)

root.mainloop()