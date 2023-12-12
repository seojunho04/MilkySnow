import tkinter as tk
from tkinter import *
import random
import time
import math
import subprocess
import sys

# 난이도
Difficulty = ""

#체력
health = 0
health_bar = ""

#캐릭터 속도
speed = 0
Dtn = 0

# 게임 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# 캐릭터 크기
CHARACTER_SIZE = 60

# 불덩이 크기
FIRE_SIZE = 28

start_time = 0

# 게임 진행 상태
GAME_START = False
GAME_OVER = False

COUNT_DONE = False

# 캐릭터 위치
CHARACTER_X = SCREEN_WIDTH / 2
CHARACTER_Y = SCREEN_HEIGHT / 2

# 불덩이 위치
FIRE_X = []
FIRE_Y = []
FIRE_DX = []
FIRE_DY = []
CFIRE_X = [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]
CFIRE_Y = [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]

direction = 0

# 게임 화면 생성
root = tk.Tk()
root.title("불덩이 피하기")

windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()

center_width = (windows_width / 2) - 400
center_height = (windows_height / 2) - 400

root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{int(center_width)}+{int(center_height)}")

# 캐릭터 이미지 설정
character = tk.PhotoImage(file="character.png")

# 불덩이 이미지 설정
fire = tk.PhotoImage(file="fire.png")

# 인게임 배경 이미지 설정
ingame_bg = tk.PhotoImage(file="ingame_background.png")

# 체력바 이미지 설정
heart_5_5 = tk.PhotoImage(file="heart_5_5.png")
heart_4_5 = tk.PhotoImage(file="heart_4_5.png")
heart_3_5 = tk.PhotoImage(file="heart_3_5.png")
heart_2_5 = tk.PhotoImage(file="heart_2_5.png")
heart_1_5 = tk.PhotoImage(file="heart_1_5.png")
heart_0_5 = tk.PhotoImage(file="heart_0_5.png")

heart_3_3 = tk.PhotoImage(file="heart_3_3.png")
heart_2_3 = tk.PhotoImage(file="heart_2_3.png")
heart_1_3 = tk.PhotoImage(file="heart_1_3.png")
heart_0_3 = tk.PhotoImage(file="heart_0_3.png")

heart_1_1 = tk.PhotoImage(file="heart_1_1.png")
heart_0_1 = tk.PhotoImage(file="heart_0_1.png")

# retry와 menu 버튼 이미지 설정
button_retry = PhotoImage(file = "retry.png")
button_menu = PhotoImage(file = "menu.png")


# 게임 화면 그리기
def draw_screen():

    global GAME_START, GAME_OVER, health, Difficulty, canvas, COUNT_DONE, health_bar, background_p

    canvas.delete("draw_screen")
    # 배경 이미지 그리기
    canvas.delete("char")
    background_p = canvas.create_image(400, 400, image=ingame_bg, tags = ("ingame_bg", "draw_screen"))
    canvas.itemconfig(background_p)

    # 캐릭터 전체 지우기
    canvas.delete("char")
    canvas.delete("fire")
    
    # 캐릭터 그리기
    canvas.create_image(CHARACTER_X, CHARACTER_Y, image=character, tags = "char")

    if Difficulty == "easy":
        if health == 20:
            health_bar = canvas.create_image(100, 20, image=heart_5_5, tags = ("heart_5_5", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 16:
            health_bar = canvas.create_image(100, 20, image=heart_4_5, tags = ("heart_4_5", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 12:
            health_bar = canvas.create_image(100, 20, image=heart_3_5, tags = ("heart_3_5", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 8:
            health_bar = canvas.create_image(100, 20, image=heart_2_5, tags = ("heart_2_5", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 4:
            health_bar = canvas.create_image(100, 20, image=heart_1_5, tags = ("heart_1_5", "draw_screen"))
            canvas.itemconfig(health_bar)
        else:
            return

    elif Difficulty == "normal":
        if health == 12:
            health_bar = canvas.create_image(100, 20, image=heart_3_3, tags = ("heart_3_3", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 8:
            health_bar = canvas.create_image(100, 20, image=heart_2_3, tags = ("heart_2_3", "draw_screen"))
            canvas.itemconfig(health_bar)
        elif health == 4:
            health_bar = canvas.create_image(100, 20, image=heart_1_3, tags = ("heart_1_3", "draw_screen"))
            canvas.itemconfig(health_bar)
        else:
            return
        
    elif Difficulty == "hard":
        if health == 4:
            health_bar = canvas.create_image(100, 20, image=heart_1_1, tags = ("heart_1_1", "draw_screen"))
            canvas.itemconfig(health_bar)
        else:
            return
    else:
        return
    
    # 불덩이 그리기
    for i in range(len(FIRE_X)):
        canvas.create_image(FIRE_X[i], FIRE_Y[i], image=fire, tags = "fire")

    for i in range(8):
        canvas.create_image(CFIRE_X[i], CFIRE_Y[i], image=fire, tags = "fire")

    # 가장 앞으로 옮기기
    canvas.tag_raise(count_text)   


# 키보드 이벤트 처리
def key_event(event):
    global CHARACTER_X, CHARACTER_Y, speed

    # 방향키 입력에 따라 캐릭터 이동
    if event.keysym == "Left":
        CHARACTER_X -= CHARACTER_SIZE * speed
    if event.keysym == "Right":
        CHARACTER_X += CHARACTER_SIZE * speed
    if event.keysym == "Up":
        CHARACTER_Y -= CHARACTER_SIZE * speed
    if event.keysym == "Down":
        CHARACTER_Y += CHARACTER_SIZE * speed
    

# 게임 시작
def start_game():
    global GAME_START, GAME_OVER, canvas, time_text, start_time, count_text, Difficulty, direction

    # 게임 시작 상태 설정
    GAME_START = True
    GAME_OVER = False

    root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

    # 캔버스 생성
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.pack()
    count_text = canvas.create_text(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,text=str(count),font=("Black Han Sans",50),fill = "red")
    Countdown()
    
    # 게임 시작 이벤트 처리
    root.bind("<KeyPress>", key_event)

    game_loop()

    start_time = time.time()

    # 3000ms 뒤에 불덩이 첫 생성
    root.after(3000, add_fire)

    #root.after(9000, add_circle_fire)

    # 불덩이 위치 초기화
    for i in range(len(FIRE_X)):
        FIRE_X[i] = random.randint(0, SCREEN_WIDTH - FIRE_SIZE)
        FIRE_Y[i] = random.randint(0, SCREEN_HEIGHT - FIRE_SIZE)

    if Difficulty == "hard":
        root.after(9000, set_location)


# 게임 시작 직전 3초 카운트 다운
count = 4

def Countdown():
    global count_text, count, COUNT_DONE

    count -= 1
    canvas.itemconfig(count_text, text=str(count))

    if count == -1:
        canvas.delete(count_text)
    elif count == 0:
        canvas.itemconfig(count_text, font=("Black Han Sans",60), fill="red")
        canvas.itemconfig(count_text, font=("Black Han Sans",40), text="START!")
        COUNT_DONE = True
    elif count == 1:
        canvas.itemconfig(count_text, font=("Black Han Sans",60), fill="red")
    elif count == 2:
        canvas.itemconfig(count_text, font=("Black Han Sans",60), fill="orange")
    else:
        canvas.itemconfig(count_text, font=("Black Han Sans",60), fill="green")

    if count >= 0:
        root.after(1000, Countdown)


# 게임 종료
def end_game():
    global GAME_START, GAME_OVER
    
    # 게임 종료 상태 설정
    GAME_START = False
    GAME_OVER = True

    canvas.create_text(SCREEN_WIDTH/2,250,text="GAME OVER",font=("Black Han Sans",60),fill = "black")

    btn_retry = tk.Button(root, image = button_retry, command=retry)
    btn_retry.place(x=325, y=450)

    btn_menu = tk.Button(root, image = button_menu, command=menu)
    btn_menu.place(x=325, y=525)


def retry():
    root.destroy()
    subprocess.run(["python", "firegame.py", sys.argv[1]])


def menu():
    root.destroy()
    subprocess.run(["python", "gamemain.py"])


# 불덩이가 생성되는 위치 랜덤 설정 및 속도
def add_fire_up():
    global Dtn, Dt, COUNT_DONE

    while COUNT_DONE is True:
        Dtn_X = random.randint(-Dt, Dt)
        Dtn_Y = random.randint(-Dt, Dt)
        if -Dt <= Dtn_X <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_X <= Dt or -Dt <= Dtn_Y <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_Y <= Dt:
            FIRE_X.append(random.randint(1,800))
            FIRE_Y.append(0)
            FIRE_DX.append(Dtn_X)
            FIRE_DY.append(Dtn_Y)
        else:
            return

def add_fire_down():
    global Dtn, Dt, COUNT_DONE

    while COUNT_DONE is True:
        Dtn_X = random.randint(-Dt, Dt)
        Dtn_Y = random.randint(-Dt, Dt)
        if -Dt <= Dtn_X <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_X <= Dt or -Dt <= Dtn_Y <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_Y <= Dt:
            FIRE_X.append(800)
            FIRE_Y.append(random.randint(1,800))
            FIRE_DX.append(Dtn_X)
            FIRE_DY.append(Dtn_Y)
        else:
            return 

def add_fire_right():
    global Dtn, Dt, COUNT_DONE

    while COUNT_DONE is True:
        Dtn_X = random.randint(-Dt, Dt)
        Dtn_Y = random.randint(-Dt, Dt)
        if -Dt <= Dtn_X <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_X <= Dt or -Dt <= Dtn_Y <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_Y <= Dt:
            FIRE_X.append(0)
            FIRE_Y.append(random.randint(1,800))
            FIRE_DX.append(Dtn_X)
            FIRE_DY.append(Dtn_Y)
        else:
            return 

def add_fire_left():
    global Dtn, Dt, COUNT_DONE

    while COUNT_DONE is True:
        Dtn_X = random.randint(-Dt, Dt)
        Dtn_Y = random.randint(-Dt, Dt)
        if -Dt <= Dtn_X <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_X <= Dt or -Dt <= Dtn_Y <= -Dt + Dt//6 or Dt-Dt//6 <= Dtn_Y <= Dt:
            FIRE_X.append(random.randint(1,800))
            FIRE_Y.append(800)
            FIRE_DX.append(Dtn_X)
            FIRE_DY.append(Dtn_Y)
        else:
            return
       

# 불덩이 추가 
def add_fire():   
    global delay
    
    add_fire_up()
    add_fire_down()
    add_fire_left()
    add_fire_right() 

    #delay ms 간격으로 불덩이 추가 생성 루프 재실행
    root.after(delay, add_fire)


# 8방향으로 퍼져나가는 불덩이의 소환 위치를 랜덤으로 지정
def set_location():
    global CFIRE_X, CFIRE_Y, direction

    C_X = random.randint(300, 500)
    C_Y = random.randint(300, 500)

    for direction in range(8):
        CFIRE_X[direction] = C_X
        CFIRE_Y[direction] = C_Y
    
    root.after(6000, set_location)
 

# 8방향으로 퍼져나가는 불덩이 충돌 확인 루프
def circle_smash_loop():
    global CFIRE_X, CFIRE_Y, health

    # 게임 시작 상태가 아닐 때는 게임 루프 종료
    if not GAME_START:
        return
    
    # 불덩이 충돌     
    if Difficulty == "hard":   
        j = 0
        while j < 8:
            if CHARACTER_X >= CFIRE_X[j] and CHARACTER_X <= CFIRE_X[j] + FIRE_SIZE and CHARACTER_Y >= CFIRE_Y[j] and CHARACTER_Y <= CFIRE_Y[j] + FIRE_SIZE:
                CFIRE_X[j] = 99999
                CFIRE_Y[j] = 99999
                health -= 4
                canvas.delete(heart_1_1)
                canvas.create_image(100, 20, image=heart_0_1, tags = "heart_0_1")
                end_game()
            j += 1

    root.after(10, circle_smash_loop)


# 충돌 확인 루프 
def smash_loop():
    global GAME_START, GAME_OVER, health, Difficulty, canvas

    # 게임 시작 상태가 아닐 때는 게임 루프 종료
    if not GAME_START:
        return
    
    # 불덩이와 캐릭터와 충돌했는지 확인 후 데미지 감소 및 충돌한 불덩이 삭제
    i = 0
    
    while i < len(FIRE_X):
        if CHARACTER_X >= FIRE_X[i] and CHARACTER_X <= FIRE_X[i] + FIRE_SIZE and CHARACTER_Y >= FIRE_Y[i] and CHARACTER_Y <= FIRE_Y[i] + FIRE_SIZE:
            FIRE_X.pop(i)
            FIRE_Y.pop(i)
            FIRE_DX.pop(i)
            FIRE_DY.pop(i)
            health -= 4 
            if health != 0:
                pass
            else:
                if Difficulty == "easy":
                    canvas.delete(heart_1_5)
                    canvas.create_image(100, 20, image=heart_0_5, tags = "heart_0_5")
                elif Difficulty == "normal":
                    canvas.delete(heart_1_3)
                    canvas.create_image(100, 20, image=heart_0_3, tags = "heart_0_3")
                elif Difficulty == "hard":
                    canvas.delete(heart_1_1)
                    canvas.create_image(100, 20, image=heart_0_1, tags = "heart_0_1")
                else:
                    pass
                end_game()

        i += 1  

    # 10ms 간격으로 충돌 확인 루프 재실행
    root.after(10, smash_loop)


# 경과 시간 루프
def update_time():
    global now, start_time, play_time, time_text

    # 게임 시작 상태가 아닐 때는 게임 루프 종료
    if not GAME_START:
        return

    # 현재 시간을 구한다.
    now = time.time()

    # 경과 시간을 구한다.
    play_time = now - 3 - start_time
    
    canvas.itemconfig(time_text, font=("Black Han Sans",19), text= (f"time : {play_time:.2f} 초"))

    root.after(1000, update_time)


# 게임 루프
def game_loop():
    global GAME_START, GAME_OVER, time_text, COUNT_DONE, direction

    # 게임 시작 상태가 아닐 때는 게임 루프 종료
    if not GAME_START:
        return

    # 화면 그리기
    draw_screen()
    canvas.delete("time_text")
    time_text = canvas.create_text(660,20,font=("Black Han Sans",20),fill = "blue", tag = "time_text")

    # 경과 시간 그리기
    if COUNT_DONE is True:
        update_time()

    # 불덩이 위치 이동
    for i in range(len(FIRE_X)):
        FIRE_X[i] += FIRE_DX[i]/6
        FIRE_Y[i] += FIRE_DY[i]/6

    root50 = math.sqrt(50)

    if Difficulty == "hard":
        t = random.randint(3,7)
        for i in range(8):   
            if i == 0:
                CFIRE_X[i] += 0
                CFIRE_Y[i] += 10/t
            elif i == 1:
                CFIRE_X[i] += root50/t
                CFIRE_Y[i] += root50/t
            elif i == 2:
                CFIRE_X[i] += 10/t
                CFIRE_Y[i] += 0
            elif i == 3:
                CFIRE_X[i] += root50/t
                CFIRE_Y[i] += -root50/t
            elif i == 4:
                CFIRE_X[i] += 0
                CFIRE_Y[i] += -10/t
            elif i == 5:
                CFIRE_X[i] += -root50/t
                CFIRE_Y[i] += -root50/t
            elif i == 6:
                CFIRE_X[i] += -10/t
                CFIRE_Y[i] += 0
            elif i == 7:
                CFIRE_X[i] += -root50/t
                CFIRE_Y[i] += root50/t

    # 화면 밖으로 나간 불덩이 지우기        
    i = 0

    while i < len(FIRE_X):
        if FIRE_X[i] >= 820 or FIRE_Y[i] >= 820 or FIRE_X[i] <= -20 or FIRE_Y[i] <= -20:
            FIRE_X.pop(i)
            FIRE_Y.pop(i)
            FIRE_DX.pop(i)
            FIRE_DY.pop(i)
        i += 1

    # 30ms 간격으로 게임 루프 재실행
    root.after(10, game_loop)


# 난이도
def easy():
    global Dt, delay, health, speed, Difficulty
    Dt = 30
    delay = 400
    health = 20
    speed = 0.6
    Difficulty = "easy"
    start_game()
    smash_loop()

def normal():
    global Dt, delay, health, speed, Difficulty
    Dt = 50
    delay = 300
    health = 12
    speed = 0.6
    Difficulty = "normal"
    start_game()
    smash_loop()

def hard():
    global Dt, delay, health, speed, Difficulty
    Dt = 66
    delay = 200
    health = 4
    speed = 0.6
    Difficulty = "hard"
    start_game()
    smash_loop()
    circle_smash_loop()


def create_CDTS():
    canvas.create_text(400,400,text="Choose Difficulty to Start",font=("System",30),fill = "blue", tags = "CDTS")

def delete_CDTS():
    canvas.delete("CDTS")

def CDTS():
    create_CDTS()
    root.after(600,delete_CDTS)
    root.after(1200,CDTS)

if sys.argv[1] == "easy":
    easy()
elif sys.argv[1] == "normal":
    normal()
elif sys.argv[1] == "hard":
    hard()

root.mainloop()
