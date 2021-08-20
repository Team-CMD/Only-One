import random, sys
import os
from tkinter import *
from PIL import Image, ImageTk
import time
from tkinter import messagebox
import random

cardList = []       # 전체 카드
player_Card = []    # 플레이어 카드
computer_Card = []  # 컴퓨터 카드
share_Card = []     # 공유 카드
W_Height = 690      # 창 높이
W_Width = 1225      # 창 너비
Image_width = 0
Image_height = 0
betting_Check = True
Table_Money = 0
Gamer_Money = [50, 50]
player_bet = [0,0]
Temp_Money = 0
Betting_Money = 0
turn = 0 # 0 = 플레이어 배팅, 1 = 컴퓨터 배팅
tie = 0 # 승부 여부. 무승부 1, 그 외 0
status = ["common","common"] # common, all, die
txt = ""
window = Tk()

# 윈도우 창의제목 설정 가능
# 윈도우 창의 너비와 높이, 초기 화면 위치 설정
# 윈도우 창의 크기 조절 가능 여부

def window_set():
    window.title("Holdom Game") 
    window.geometry(str(W_Width)+"x"+str(W_Height)+"+300+100") 
    window.resizable(False,False)

def txtRead():
    global txt
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\" + "rule.txt"

    f = open(path, 'r',encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        txt += line
    f.close()

def cardCompare():
    global status
    card = []
    score = [0]*2
    winner = 2
    card.append(player_Card+share_Card)
    card.append(computer_Card+share_Card)

    for i in range(2):
        tmp = card[i]
        tmp.sort()
        cnt = len(list(set(tmp)))

        if cnt == 1:                                # 트리플 경우
            score[i] = 300 + tmp[0]
        elif cnt == 2:                              # 더블 경우
            score[i] = 100 + tmp[1] 
        else: 
            if (tmp[2] == tmp[1]+1 == tmp[0]+2):    # 스트레이트
                score[i] = 200 + tmp[2]
            else:                                   # 조합x      
                score[i] = tmp[2]

    for i in range(2):
        if status[i] == "die": # 플레이어 다이로 인한 컴퓨터 승
            winner = (i+1)%2
            return winner

    if score[0] > score[1]: #플레이어 승
        winner = 0
    elif score[0] == score[1]: #무승부
        winner = 2
    else: #컴퓨터 승
        winner = 1

    return winner

def init():
    global Temp_Money
    global Table_Money

    status[0] = "common"
    status[1] = "common"
    
    Temp_Money = 0
    player_bet[0] = 0
    player_bet[1] = 0

    Table_Money += 2
    Gamer_Money[0] -= 1
    Gamer_Money[1] -= 1

def All():
    global betting_Check
    global Table_Money
    global Gamer_Money
    global Temp_Money

    if Gamer_Money[0] > 0 and Gamer_Money[0] - Temp_Money < player_bet[1] - Temp_Money:
        Table_Money += Gamer_Money[0]
        Temp_Money += Gamer_Money[0]
        Gamer_Money[0] = 0 
        status[0] = "all"
        betting_Check = False
    else:
        messagebox.showinfo("참고하세요", "해당 버튼은 상대 배팅액보다 보유액이 적어야 사용가능합니다!")
    Label_place()       

def Die():
    global betting_Check
    global Temp_Money
    
    Temp_Money = 0
    status[0] = "die"
    betting_Check = False

def countUP():
    global Temp_Money

    if Temp_Money - player_bet[0] < Gamer_Money[0]:
        Temp_Money += 1
        Label_place()

def countDown():
    global Temp_Money

    if Temp_Money > player_bet[1]:
        Temp_Money -= 1
        Label_place()

def Check():
    global betting_Check
    global Table_Money
    global Gamer_Money
    global Temp_Money
    global turn

    Gamer_Money[0] -= Temp_Money - player_bet[0] # 임시금액만큼 돈이 빠짐
    Table_Money += Temp_Money - player_bet[0]
    player_bet[0] = Temp_Money
    if player_bet[0] == player_bet[1]:
        betting_Check = False
    if Gamer_Money[0] == 0 and player_bet[1] >= player_bet[0]:
        betting_Check = False
    if Gamer_Money[1] == 0:
        betting_Check = False
    Label_place()
    turn = 1
    Button_place()

def Rule():
    newWindow = Toplevel()
    aa = Label(newWindow, text=txt, justify="left")
    aa.pack()

def Button_place():
    state = NORMAL

    if turn:
        state = DISABLED

    up = Button(window, text="Up", command=countUP, borderwidth = 4, background="yellow", state=state)
    up.place(x=W_Width*2/3 + 30, y=W_Height/2+90, width=120, height=40)
    up.update()

    down = Button(window, text="Down", command=countDown, borderwidth = 4, background="yellow", state=state)
    down.place(x=W_Width*2/3 + 30, y=W_Height/2+240, width=120, height=40)
    down.update()

    all = Button(window, text="All_in", command=All, borderwidth = 4, background="yellow", state=state)
    all.place(x=W_Width*2/3 + 120, y=W_Height/2+165, width=120, height=40)    
    all.update()

    die = Button(window, text="Die", command=Die, borderwidth = 4, background="yellow", state=state)
    die.place(x=W_Width*2/3+200, y=W_Height/2+90, width=120, height=40)
    die.update()

    check = Button(window, text="Check", command=Check, borderwidth = 4, background="yellow", state=state)
    check.place(x=W_Width*2/3+200, y=W_Height/2+240, width=120, height=40)
    check.update()

    rule = Button(window, text="R", command=Rule, borderwidth = 4, background="green")
    rule.place(x=10,y=10,width=20, height=20)
    rule.update()

def Label_place():
    Main_Label = Label(window, text = "Gambling Board", font = 150, fg = "green")
    Main_Label.place(x = 930, y =10)

    PMoney_Label = Label(window, text = "나의 보유 칩")
    PMoney_Label.place(x = W_Width * 2 / 3, y = W_Height / 2 - 280, width = 120, height = 40)
    PMoney_Value = Label(window, text = Gamer_Money[0], bg = "white", relief="ridge", width = 120, height = 40)
    PMoney_Value.place(x = W_Width * 2 / 3 + 200, y = W_Height / 2 - 280, width = 120, height = 40)

    CMoney_Label = Label(window, text = "상대 보유 칩")
    CMoney_Label.place(x = W_Width * 2 / 3, y = W_Height / 2 - 240, width = 120, height = 40)
    CMoney_Value = Label(window, text = Gamer_Money[1], bg = "white", relief="ridge", width = 120, height = 40)
    CMoney_Value.place(x = W_Width * 2 / 3 + 200, y = W_Height / 2 - 240, width = 120, height = 40)

    TMoney_Label = Label(window, text = "테이블 전체 칩")
    TMoney_Label.place(x = W_Width * 2 / 3, y = W_Height / 2 - 200, width = 120, height = 40)
    TMoney_Value = Label(window, text = Table_Money, bg = "white", relief="ridge", width = 120, height = 40)
    TMoney_Value.place(x = W_Width * 2 / 3 + 200, y = W_Height / 2 - 200, width = 120, height = 40)

    Cbetting_Label = Label(window, text = "상대 배팅액")
    Cbetting_Label.place(x = W_Width * 2 / 3, y = W_Height / 2 - 80, width = 120, height = 40)
    Cbetting_Value = Label(window, text = player_bet[1], bg = "white", relief="ridge", width = 120, height = 40)
    Cbetting_Value.place(x = W_Width * 2 / 3 + 200, y = W_Height / 2 - 80, width = 120, height = 40)

    Pbetting_Label = Label(window, text = "나의 배팅액")
    Pbetting_Label.place(x = W_Width * 2 / 3, y = W_Height / 2 - 40, width = 120, height = 40)
    Pbetting_Value = Label(window, text = Temp_Money, bg = "white", relief="ridge", width = 120, height = 40)
    Pbetting_Value.place(x = W_Width * 2 / 3 + 200, y = W_Height / 2 - 40, width = 120, height = 40)

def Roll():
    # 덱에서 랜덤으로 뽑아 카드를 주는 함수
    # 이하 반복문 공유 카드 리스트에 2장 저장
    # 각 게이머에게 카드 한장씩 지급
    global player_Card
    global computer_Card
    global share_Card

    share_Card.clear()
    player_Card.clear()
    computer_Card.clear()

    if not cardList:
        for i in range(4):
            for j in range(1,11):
                cardList.append(j)

    for i in range(2): 
        tmp = random.choice(cardList)
        share_Card.append(tmp)
        cardList.remove(tmp)

    temp = []
    temp = random.sample(cardList, 2)

    for i in range(0,2):
        if i == 0:
            player_Card.append(temp[i])
        else:
            computer_Card.append(temp[i])
        cardList.remove(temp[i])

def com_Betting():
    global turn
    global betting_Check
    global Table_Money
    global Temp_Money
    global Betting_Money

    sel = random.randrange(20)
    if sel < 18:
        com_beforeBet = player_bet[1]
        player_beforeBet = player_bet[0] - player_bet[1]
        if player_beforeBet == 0:    # 컴퓨터 선 베팅
            player_bet[1] = random.randrange(1, Gamer_Money[1]+1)   # +2 한 이유:  반올림 + 1 효과
        else:                        # 컴퓨터 후 베팅
            if player_beforeBet > Gamer_Money[1]:                       # 게임 참여 했음 but 콜 할 돈이 안됨
                player_bet[1] = com_beforeBet + Gamer_Money[1] 
            else:
                player_bet[1] = com_beforeBet + random.randrange(player_beforeBet, Gamer_Money[1]+1)
        Table_Money += player_bet[1] - com_beforeBet
        Gamer_Money[1] -= player_bet[1] - com_beforeBet
        if Gamer_Money[1] == 0 and player_beforeBet != 0:
            betting_Check = False
        else:
            if player_bet[0] == player_bet[1]:
                betting_Check = False
            else:
                betting_Check = True
    else:
        status[1] = "die"
        betting_Check = False

    time.sleep(3)
    Label_place()
    turn = 0
    Button_place()
        

def cardImageSet():
    global Image_height
    global Image_width
    img = []
    resized_img = []
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\"

    for i in range(11):
        img.append(Image.open(path + str(i) + '.png'))
        img[i] = img[i].resize((img[i].size[0]//7, img[i].size[1]//7), Image.ANTIALIAS)
        resized_img.append(ImageTk.PhotoImage(img[i]))
    
    Image_width = img[0].size[0]
    Image_height = img[0].size[1]

    return resized_img

if __name__ == "__main__":
    window_set()
    txtRead()
    img = cardImageSet()

    while Gamer_Money[0] != 0 and Gamer_Money[1] != 0:
        cardImg = []
        init()
        Roll()
        Label_place()
        Button_place()

        if Gamer_Money[0] == 0 or Gamer_Money[1] == 0:
            betting_Check = False

        cardImg.append(Label(window, image=img[computer_Card[0]]))
        cardImg.append(Label(window, image=img[share_Card[0]]))
        cardImg.append(Label(window, image=img[share_Card[1]]))
        cardImg.append(Label(window, image=img[0]))
        cardImg.append(Label(window, image=img[player_Card[0]]))
            
        cardImg[0].place(x=W_Width/3, y=0)
        cardImg[1].place(x=W_Width/3 - Image_width, y=W_Height/2 - Image_height//2)
        cardImg[2].place(x=W_Width/3 + Image_width, y=W_Height/2 - Image_height//2)
        cardImg[3].place(x=W_Width/3, y= W_Height - Image_height)
        window.update()

        while betting_Check:
            if turn == 1:
                com_Betting()
            window.update()
            
        cardImg[4].place(x=W_Width/3, y= W_Height - Image_height)
        time.sleep(1)
        window.update()
        time.sleep(2)
        betting_Check = True

        winner = cardCompare()
        if winner == 2: # 비길경우
            messagebox.showinfo("Winner", "The Game ended in a tie")
        else:
            if winner == 0: # 플레이어 승
                Gamer_Money[0] += Table_Money
                if status[1] == "die":
                    messagebox.showinfo("Winner", "상대의 die로 게임에서 이기셨습니다")
                else:
                    messagebox.showinfo("Winner", "Player Win")
            else: # 컴퓨터 승
                Gamer_Money[1] += Table_Money
                messagebox.showinfo("Winner", "Computer Win")
            Table_Money = 0
            turn = winner
        window.update()
        

    if Gamer_Money[0] == 0:
        messagebox.showinfo("Final Winner", "Final Winner : Computer")
    else:
        messagebox.showinfo("Final Winner", "Final Winner : Player")
    sys.exit()

    window.mainloop()