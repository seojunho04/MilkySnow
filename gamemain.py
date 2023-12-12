import tkinter as tk
from tkinter import *
import subprocess

def open_game_fightparty():
    root.destroy()
    subprocess.run(["python", "fightparty.py"])

def open_game_firegame():
    root.destroy()
    subprocess.run(["python", "CDTS.py"])

def open_game_tetris():
    root.destroy()
    subprocess.run(["python", "tetris.py"])

def quit_maingame():
    root.destroy()
    

root = tk.Tk()
root.title("Milky Snow")

windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()

center_width = (windows_width / 2) - 400
center_height = (windows_height / 2) - 400

main_width = 800
main_height = 800

root.geometry(f"{main_width}x{main_height}+{int(center_width)}+{int(center_height)}")

main_bg = tk.PhotoImage(file="main_background.png")

game_1_icon = PhotoImage(file = "game_1_icon.png")
game_2_icon = PhotoImage(file = "game_2_icon.png")
game_3_icon = PhotoImage(file = "game_3_icon.png")
btn_quit = PhotoImage(file = "quit.png")

canvas = tk.Canvas(root, width = 800, height=800, highlightthickness=0)
main_background = canvas.create_image(400, 400, image=main_bg, tags = "main_background")
main_title = canvas.create_text(400,220,text="Milky Snow",font=("Black Han Sans",70),fill = "White", tags = "TT")
main_subtitle = canvas.create_text(400,282,text="mini game",font=("Black Han Sans",20),fill = "black", tags = "TsT")
canvas.itemconfig(main_subtitle)
canvas.itemconfig(main_title)
canvas.itemconfig(main_background)
canvas.pack()

def create_CTS():
    canvas.create_text(400,400,text="Click to Start",font=("System",30),fill = "lightgreen", tags = "CTS")

def delete_CTS():
    canvas.delete("CTS")

def CTS():
    create_CTS()
    root.after(600,delete_CTS)
    root.after(1200,CTS)

CTS()

button_1 = tk.Button(root, image = game_1_icon, command=open_game_fightparty)
button_1.place(x=70, y=475)

button_2 = tk.Button(root, image = game_2_icon, command=open_game_firegame)
button_2.place(x=300, y=475)

button_3 = tk.Button(root, image = game_3_icon, command=open_game_tetris)
button_3.place(x=530, y=475)

button_quit = tk.Button(root, image = btn_quit, command=quit_maingame)
button_quit.place(x=610, y=730)

root.mainloop()