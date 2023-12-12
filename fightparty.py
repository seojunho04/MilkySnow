import tkinter
import time
import random
from tkinter import *
import subprocess

FNT = ("Times New Roman", 25)
stack_L = 0 #스텍 쌓을 때 쓰는 수 왼쪽 
stack_R = 0 #스텍 쌓을 때 쓰는 수 오른쪽 
crt_button = [None]* 8
idx=0 
L_crt = None  #왼쪽 캐릭터 선택
R_crt = None  #오른쪽 캐릭터 선택
nametext = None #선택할 때 보이는 이름
okbtn = None #선택 버튼
okcrtlist = []    # 사용자가 선택한 캐릭터를 넣을 빈 리스트
btn_right_ult = None #오른쪽스킬2버튼
btn_left_ult = None  #왼쪽스킬2버튼
btn_left = None  #왼쪽스킬버튼
btn_right = None #오른쪽스킬버튼
hpbar_image_L= None
hpbar_image_Re= None #이름 보이는 택 이미지 파일
skill_one_button_image = "button_image.png"
skill_ult_button_image = "ult_button_image.png"

q = None #왼쪽 캐릭터 선택
w = None #오른쪽 캐릭터 선택
label_right_ult = None #스킬2 라벨 왼쪽
label_left_ult = None #스킬2 라벨 오른쪽
turn = 0
cannotattack = None
start_title_image = None
start_button_image = None
start_button = None
class GameCharacter:

    def __init__(self, name, life, x, y, imgfile, tagname):
        self.name = name
        self.life = life
        self.lmax = life
        self.x = x
        self.y = y
        self.img = tkinter.PhotoImage(file=imgfile)
        self.tagname = tagname
        
    def draw(self):
        x = self.x
        y = self.y

        # 기존 체력바 삭제
        canvas.delete(f"{self.tagname}_health_bar")

        # 체력이 0 이하일 때 캐릭터 삭제
        if self.life <= 0:
            canvas.delete(self.tagname)
        else:
            canvas.create_image(x, y, image=self.img, tag=self.tagname)

            # 체력이 0 초과인 경우에만 체력바 그리기
            if self.life > 0:
                health_bar_width = 250  # 체력바 너비 조절
                health_ratio = self.life / self.lmax
                health_bar_height = 18
                health_bar_color = "pink"
                health_bar_x = x - health_bar_width / 2
                health_bar_y = y - 280

                # 변화된 체력 값에 따라 새로운 체력바 그리기
                current_health_width = health_bar_width * health_ratio
                canvas.create_rectangle(
                    health_bar_x,
                    health_bar_y,
                    health_bar_x + current_health_width,
                    health_bar_y + health_bar_height,
                    fill=health_bar_color,
                    outline=health_bar_color,
                    tags=(f"{self.tagname}_health_bar",)  # 태그를 사용하여 체력바 구분
                )
                
            hpbar_image_L = tkinter.PhotoImage(file="hpbar_image.png")
            canvas.create_image(180, 20, image=hpbar_image_L)
            hpbar_image_R = tkinter.PhotoImage(file="hpbar_image.png")
            canvas.create_image(610, 20, image=hpbar_image_R)
            canvas.create_text(x + 62, y - 305, text="HP {}/{}".format(self.life, self.lmax), font=("Times New Roman", 20),
                            fill="black", tag=self.tagname)



        
    def draw_name(self):
        x = self.x
        y = self.y
        canvas.create_text(x + 2-80, y - 248-35-20, text=self.name, font=("Times New Roman", 15), fill="black", tag=self.tagname)

    
    def attack(self):
        di = 1
        if self.x >= 400:
            di = -1
        for i in range(5):
            canvas.coords(self.tagname, self.x + i * 10 * di, self.y)
            canvas.update()
            time.sleep(0.1)
        canvas.coords(self.tagname, self.x, self.y)
        
    def damage_200(self):
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        rnb_P = random.randint(1, 100)
        rdmg_200 = random.randint(10, 25) 
        
        if rnb_P <100 and rnb_P >=80 :
            self.life = self.life - 30
            print(f"{self.name}에게 30의 데미지가 들어갔다.")
        elif rnb_P == 1 or rnb_P == 100 :
            self.life = self.life - 90 
            print("치명타를 맞았다!")
            print(f"{self.name}에게 90의 데미지가 들어갔다!!!")
        else :
            self.life = self.life - rdmg_200
            print("얍!")
            print(f"{self.name}에게 {rdmg_200}의 데미지가 들어갔다.")
        if self.life > 0:
            self.draw()
        else:
            print(self.name + "는 쓰러졌다...")
    

    def damage_180(self):
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        rnb_P = random.randint(1, 100)
        rdmg_180 = random.randint(15, 30) 

        if rnb_P <100 and rnb_P >=80 :
            self.life = self.life - 35
            print(f"{self.name}에게 35의 데미지가 들어갔다.")
        elif rnb_P == 1 or rnb_P == 100 :
            self.life = self.life - 95
            print("치명타를 맞았다!")
            print(f"{self.name}에게 95의 데미지가 들어갔다!!!")
        else :
            self.life = self.life - rdmg_180
            print("얍")
            print(f"{self.name}에게 {rdmg_180}의 데미지가 들어갔다.")
        if self.life > 0:
            self.draw()
        else:
            print(self.name + "는 쓰러졌다...")


    def damage_170(self):
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        rnb_P = random.randint(1, 100)
        rdmg_170 = random.randint(20, 35) 
        if rnb_P <100 and rnb_P >=80 :
            self.life = self.life - 40
            print(f"{self.name}에게 40의 데미지가 들어갔다.")
        elif rnb_P == 1 or rnb_P == 100 :
            self.life = self.life - 100 
            print("치명타를 맞았다!")
            print(f"{self.name}에게 100의 데미지가 들어갔다!!!")
        else :
            self.life = self.life - rdmg_170
            print("얍")
            print(f"{self.name}에게 {rdmg_170}의 데미지가 들어갔다.")
        if self.life > 0:
            self.draw()
        else:
            print(self.name + "는 쓰러졌다...")


    def damage_160(self):
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        rnb_P = random.randint(1, 100)
        rdmg_160 = random.randint(25, 40) 

        if rnb_P <100 and rnb_P >=80 :
            self.life = self.life - 45
            print(f"{self.name}에게 45의 데미지가 들어갔다.")
        elif rnb_P == 1 or rnb_P == 100 :
            self.life = self.life - 110
            print("치명타를 맞았다!")
            print(f"{self.name}에게 110의 데미지가 들어갔다!!!")
        else :
            self.life = self.life - rdmg_160
            print("얍")
            print(f"{self.name}에게 {rdmg_160}의 데미지가 들어갔다.")
        if self.life > 0:
            self.draw()
        else:
            print(self.name + "는 쓰러졌다...")


    def damage_ult(self):
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)    
        random_damage_ult = random.randint(50, 70)                      
        self.life = self.life - random_damage_ult                           
        print("세다!")
        print(f"{self.name}에게 {random_damage_ult}의 데미지가 들어갔다.")
        if self.life > 0:
            self.draw()
        else:
            print(self.name + "는 쓰러졌다...")


def start_button():
    global start_title_image, start_button_image, start_button, hpbar_image_L, hpbar_image_R
    start_title_image = tkinter.PhotoImage(file="start_image.png")
    canvas.create_image(410, 280, image=start_title_image, tags="start_title_image")
    start_button_image = tkinter.PhotoImage(file="start_button_image.png")
    start_button = tkinter.Button(image = start_button_image, command = L_select_character_btn)
    start_button.place(x = 270, y = 380)



def L_select_character_btn():  #왼쪽 캐릭터 선택
    global start_title_image, start_button_image, start_button

    canvas.delete("start_title_image")
    start_button.destroy()
    crt_imagelist = [
    "sensi_btn.png",
    "masic_btn.png",
    "donut_btn.png",
    "gunner_btn.png",
    "batgirl_btn.png",
    "greenbear_btn.png",
    "fencing_btn.png",
    "knife_btn.png"
    ]

    

    for i in range(8):
        crt_image = tkinter.PhotoImage(file=crt_imagelist[i])
        crt_button[i] = tkinter.Button(image = crt_image, command =lambda idx=i: select_character(idx))
        crt_button[i].image = crt_image
        btn_x = 300 + (i*125)
        if i <= 3 :
            crt_button[i].place(x = btn_x , y = 50)
        else :
            btn_x = 300 + ((i-4)*125)
            crt_button[i].place(x = btn_x , y = 175)

 
    def select_character(idx):
        global L_crt, nametext, okbtn

        # 이전에 선택한 캐릭터의 태그를 가져와서 삭제
        if L_crt:
            canvas.delete(L_crt.tagname)
            canvas.delete(nametext)
        if okbtn:
            okbtn.destroy()

        L_crt = character_L[idx]
        L_crt.draw()
        nametext= canvas.create_text(550, 330, text=character_L[idx].name, font=("Times New Roman", 30), fill="black")
        nametext
        okbtn = tkinter.Button(text="선택", font=("Times New Roman", 20), command = okbottun) #command = 
        okbtn.place(x = 510, y = 360)

    def okbottun():
        global L_crt, okcrtlist
        okcrtlist.append(L_crt.tagname)
        if okcrtlist[0]:
            okbtn.destroy() #선택 버튼 제거됨
            canvas.delete(nametext) #캐릭터 이름 텍스트 제거
            for q in range(8):
                crt_button[q].destroy() #캐릭터 선택 버튼 제거됨
            R_player = R_select_character_btn()
            return R_player


def R_select_character_btn():  #왼쪽 캐릭터 선택
    crt_imagelist = [
    "sensi_btn.png",
    "masic_btn.png",
    "donut_btn.png",
    "gunner_btn.png",
    "batgirl_btn.png",
    "greenbear_btn.png",
    "fencing_btn.png",
    "knife_btn.png"
    ]

    for i in range(8):
        crt_image = tkinter.PhotoImage(file=crt_imagelist[i])
        crt_button[i] = tkinter.Button(image = crt_image, command =lambda idx=i: select_character(idx))
        crt_button[i].image = crt_image
        btn_x = 30 + (i*125)
        if i <= 3 :
            crt_button[i].place(x = btn_x , y = 50)
        else :
            btn_x = 30 + ((i-4)*125)
            crt_button[i].place(x = btn_x , y = 175)

 
    def select_character(idx):
        global R_crt, nametext, okbtn

        # 이전에 선택한 캐릭터의 태그를 가져와서 삭제
        if R_crt:
            canvas.delete(R_crt.tagname)
            canvas.delete(nametext)
        if okbtn:
                okbtn.destroy()

        R_crt = character_R[idx]
        R_crt.draw()
        nametext= canvas.create_text(280, 330, text=character_L[idx].name, font=("Times New Roman", 30), fill="black")
        nametext
        okbtn = tkinter.Button(text="선택", font=("Times New Roman", 20), command = okbottun) #command = 
        okbtn.place(x = 240, y = 360)

    def okbottun():
        global R_crt, okcrtlist
        okcrtlist.append(R_crt.tagname)
        print(okcrtlist)
        if okcrtlist[1]:
            okbtn.destroy() #선택 버튼 제거됨
            canvas.delete(nametext) #캐릭터 이름 텍스트 제거
            game_start()
            for q in range(8):
                crt_button[q].destroy() #캐릭터 선택 버튼 제거됨

    
def crt_listct_L(): #캐릭터를 캐릭터 리스트에서 지정해줌
    global q
    for i in range(8):
        if okcrtlist[0] == character_L[i].tagname:
            q = i
            return q


def crt_listct_R(): #캐릭터를 캐릭터 리스트에서 지정해줌
    global w
    for i in range(8):
        if okcrtlist and len(okcrtlist) >= 2 and okcrtlist[1] == character_R[i].tagname:
            w = i
            return w   

def click_left():
    global q, w, stack_L, btn_left_ult, label_left_ult, turn, cannotattack
    crt_listct_L()
    crt_listct_R()
    R = character_R[w]
    L = character_L[q]
    if (turn == 0) or (turn %2 == 0):
        canvas.delete(cannotattack)
        turn = turn + 1
        stack_L = stack_L + 1
        L.attack()
        if L.tagname == "Lsensi" or "Lbatgirl" or "Lfencing" or "Lknife" :
            R.damage_200()
        elif L.tagname == "Lgreenbear" :
            R.damage_180()
        elif L.tagname == "Lgunner" :
            R.damage_170() 
        else : 
            R.damage_160() 

        character_L[q].draw_name()
        character_R[w].draw_name()

        if character_R[w].life <= 0:
            canvas.delete( character_R[w].draw())
            label_1 = tkinter.Label(text=character_L[q].name + "승리!", font =("Times New Roman", 60), fg="black")
            label_1.place(x = 110, y =300)
            root.after(5000, menu)
            return turn
        else : 
            if stack_L >= 3:
                btn_left_ult.config(state=tkinter.NORMAL)
                label_left_ult.config(text="활성화")
            elif stack_L == 2:
                label_left_ult.config(text="2/3")
            elif stack_L == 1:
                label_left_ult.config(text="1/3")
            elif stack_L == 0:
                label_left_ult.config(text="0/3")
        return stack_L, turn
        
    else:
        
        canvas.delete(cannotattack)
        cannotattack= canvas.create_text(400, 330, text=L.name +"의 공격 차례가 아닙니다.", font=("Times New Roman", 30), fill="red")


def menu():
    root.destroy()
    subprocess.run(["python", "gamemain.py"])


def btn_left_ult_clicked():
    global stack_L, btn_right_ult, turn, cannotattack, label_left_ult
    crt_listct_L()
    crt_listct_R()
    R = character_R[w]
    L = character_L[q]
    if (turn %2 == 0):
        canvas.delete(cannotattack)
        label_left_ult.config(text="0/3")
        turn = turn + 1
        L.attack()
        R.damage_ult()
        stack_L = 0  
        btn_left_ult.config(state=tkinter.DISABLED) 
        if character_R[w].life <= 0:
            canvas.delete( character_R[w].draw())
            label_1 = tkinter.Label(text=character_L[q].name + "승리!", font =("Times New Roman", 60), fg="black")
            label_1.place(x = 110, y =300)
            return stack_L, turn
        else:
            return stack_L, turn                         
    else:
        canvas.delete(cannotattack)
        cannotattack= canvas.create_text(400, 330, text=L.name +"의 공격 차례가 아닙니다.", font=("Times New Roman", 30), fill="red")


def click_right():
    global q, w, stack_R, label_right_ult, btn_right_ult, turn, cannotattack
    crt_listct_L()
    crt_listct_R()
    R = character_R[w]
    L = character_L[q]
    if (turn == 1) or (turn%2 == 1):
        canvas.delete(cannotattack)
        turn = turn + 1
        stack_R = stack_R + 1
        R.attack()
        if R.tagname == "Rsensi" or "Rbatgirl" or "Rfencing" or "Rknife":
            L.damage_200()
        elif R.tagname == "Rgreenbear" :
            L.damage_180()
        elif R.tagname == "Rgunner" :
            L.damage_170()
        else : 
            L.damage_160()

        character_L[q].draw_name()
        character_R[w].draw_name()

        if character_L[q].life <= 0:
            canvas.delete( character_L[q].draw())
            label_2 = tkinter.Label(text=character_R[w].name + "승리!", font =("Times New Roman", 60), fg="black")
            label_2.place(x = 110, y =300)
            return turn
        else : 
            if stack_R >= 3:
                btn_right_ult.config(state=tkinter.NORMAL)
                label_right_ult.config(text="활성화")
            elif stack_R == 2:
                label_right_ult.config(text="2/3")
            elif stack_R == 1:
                label_right_ult.config(text="1/3")
            elif stack_R == 0:
                label_right_ult.config(text="0/3")

        return stack_R, turn
    else :
        canvas.delete(cannotattack)
        cannotattack= canvas.create_text(400, 330, text=R.name +"의 공격 차례가 아닙니다.", font=("Times New Roman", 30), fill="red")
    
def btn_right_ult_clicked():
    global stack_R, turn, cannotattack, label_right_ult
    crt_listct_L()
    crt_listct_R()
    R = character_R[w]
    L = character_L[q]
    if (turn%2 == 1):
        canvas.delete(cannotattack)
        label_right_ult.config(text="0/3")
        turn = turn + 1
        R.attack()
        L.damage_ult()
        stack_R = 0  
        btn_right_ult.config(state=tkinter.DISABLED) 
        if character_L[w].life <= 0:
            canvas.delete( character_L[q].draw())
            label_1 = tkinter.Label(text=character_L[q].name + "승리!", font =("Times New Roman", 60), fg="black")
            label_1.place(x = 110, y =300)
            return turn
        else:
            return stack_R, turn   

    else :
        canvas.delete(cannotattack)
        cannotattack= canvas.create_text(400, 330, text=R.name +"의 공격 차례가 아닙니다.", font=("Times New Roman", 30), fill="red") 

def start_bar():
    start_label = tkinter.Label(text="게임 시작!", font =("Times New Roman", 100), fg="pink")
    start_label.place(x = 90, y =200)
    def remove_label():
        start_label.destroy()
    root.after(1000, remove_label)

def game_start():
    global okcrtlist, btn_right_ult, btn_left, btn_right, btn_left_ult, hpbar_image_L, hpbar_image_R, skill_one_button_image, label_left_ult, label_right_ult, q, w, skill_ult_button_image
    if okcrtlist[1]:
        crt_listct_L()
        crt_listct_R()
        start_bar()



        skill_one_button_image = tkinter.PhotoImage(file="button_image.png")
        skill_ult_button_image = tkinter.PhotoImage(file="ult_button_image.png")
        btn_left = tkinter.Button(image = skill_one_button_image, command = click_left)
        btn_left.place(x = 150, y = 360)



        btn_left_ult = tkinter.Button(image = skill_ult_button_image, command=btn_left_ult_clicked, state=tkinter.DISABLED)
        btn_left_ult.place(x = 150, y = 420)

        btn_right = tkinter.Button(image = skill_one_button_image, command = click_right)
        btn_right.place(x = 550, y = 360)

        btn_right_ult = tkinter.Button(image = skill_ult_button_image, command=btn_right_ult_clicked, state=tkinter.DISABLED)
        btn_right_ult.place(x = 550, y = 420)

        hpbar_image_L = tkinter.PhotoImage(file="hpbar_image.png")
        canvas.create_image(199, 50, image=hpbar_image_L, tags="hpbar_L")
        hpbar_image_R = tkinter.PhotoImage(file="hpbar_image.png")
        canvas.create_image(599, 50, image=hpbar_image_R, tags="hpbar_R")
        character_L[q].draw_name()
        character_R[w].draw_name()

        label_left_ult = tkinter.Label(text="0/3", font =("Times New Roman", 20), fg="black")
        label_left_ult.place(x = 180, y =460)

        label_right_ult = tkinter.Label(text="0/3", font =("Times New Roman", 20), fg="black")
        label_right_ult.place(x = 580, y =460)                   

root = tkinter.Tk()
root.title("Fight Party!")

windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()

center_width = (windows_width / 2) - 400
center_height = (windows_height / 2) - 400

main_width = 800
main_height = 600

root.geometry(f"{main_width}x{main_height}+{int(center_width)}+{int(center_height)}")
canvas = tkinter.Canvas(root, width = 800, height = 600)
canvas.pack()
bg_image = tkinter.PhotoImage(file = "fp_background.png")
canvas.create_image(400, 300, image = bg_image)


character_L = [
    GameCharacter("【 레이첼 】", 200, 200, 320, "sensi_L.png", "Lsensi"),  #self, name, life, x, y, imgfile, tagname
    GameCharacter("【 허쉬 】", 160, 200, 320, "masic_L.png", "Lmasic"),
    GameCharacter("【 슈 】", 160, 200, 320, "donut_L.png", "Ldonut"),
    GameCharacter("【 마일론 】", 170, 200, 320, "gunner_L.png", "Lgunner"),
    GameCharacter("【 라소 】", 200, 200, 320, "batgirl_L.png", "Lbatgirl"),
    GameCharacter("【 베리 】", 180, 200, 320, "greenbear_L.png", "Lgreenbear"),
    GameCharacter("【 펜시 】", 200, 200, 320, "fencing_L.png", "Lfencing"),
    GameCharacter("【 이프 】", 200, 200, 320, "knife_L.png", "Lknife")
]

character_R = [
    GameCharacter("【 레이첼 】", 200, 600, 320, "sensi_R.png", "Rsensi"),  #self, name, life, x, y, imgfile, tagname
    GameCharacter("【 허쉬 】", 160, 600, 320, "masic_R.png", "Rmasic"),
    GameCharacter("【 슈 】", 160, 600, 320, "donut_R.png", "Rdonut"),
    GameCharacter("【 마일론 】", 170, 600, 320, "gunner_R.png", "Rgunner"),
    GameCharacter("【 라소 】", 200, 600, 320, "batgirl_R.png", "Rbatgirl"),
    GameCharacter("【 베리 】", 180, 600, 320, "greenbear_R.png", "Rgreenbear"),
    GameCharacter("【 펜시 】", 200, 600, 320, "fencing_R.png", "Rfencing"),
    GameCharacter("【 이프 】", 200, 600, 320, "knife_R.png", "Rknife")
]

start_button()

root.mainloop()
