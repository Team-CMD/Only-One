import random, sys, os, time, random
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

cardList = []       # 전체 카드
player_Card = []    # 플레이어 카드
computer_Card = []  # 컴퓨터 카드
share_Card = []     # 공유 카드
W_Height = 720      # 창 높이
W_Width = 1278      # 창 너비
Image_width = 0
Image_height = 0
betting_Check = True
Table_Money = 0
Gamer_Money = [50, 50]
player_bet = [0,0]
Temp_Money = 0
turn = 0 # 0 = 플레이어 배팅, 1 = 컴퓨터 배팅
status = ["common","common"] # common, all, die
window = Tk()

# 윈도우 창의제목 설정 가능
# 윈도우 창의 너비와 높이, 초기 화면 위치 설정
# 윈도우 창의 크기 조절 가능 여부

def window_set():
    window.title("Holdom Game") 
    window.geometry(str(W_Width)+"x"+str(W_Height)+"+300+100") 
    window.resizable(False,False)

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

    if Gamer_Money[0] != 0 and Gamer_Money[1] != 0:
        Table_Money += 2
        Gamer_Money[0] -= 1
        Gamer_Money[1] -= 1

def All():
    global Temp_Money

    if Gamer_Money[0] != 0:
        Temp_Money = Gamer_Money[0]

    Label_place()           

def Die(butImg):
    global betting_Check
    global Temp_Money
    global turn

    Temp_Money = 0
    status[0] = "die"
    betting_Check = False
    turn = 1
    Button_place(butImg)

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

def Check(butImg):
    global betting_Check
    global Table_Money
    global Gamer_Money
    global Temp_Money
    global turn

    if Temp_Money != 0:
        if Temp_Money >= player_bet[1]:
            if Temp_Money < Gamer_Money[0]:
                Gamer_Money[0] -= Temp_Money - player_bet[0] # 임시금액만큼 돈이 빠짐
                Table_Money += Temp_Money - player_bet[0]
            else:
                Gamer_Money[0] = 0
                Table_Money += Temp_Money
            player_bet[0] = Temp_Money
            if player_bet[0] == player_bet[1]:
                betting_Check = False
            if Gamer_Money[0] == 0 and player_bet[1] >= player_bet[0]:
                betting_Check = False
            if Gamer_Money[1] == 0:
                betting_Check = False
            Label_place()
            turn = 1
            Button_place(butImg)

def Rule():
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\View Design\\Rule View.png"
    rule = Image.open(path)
    rule2 = ImageTk.PhotoImage(rule)
    newWindow = Toplevel()
    ruleEx = Label(newWindow, image=rule2)
    ruleEx.pack()

def Button_place(butImg):
    state = NORMAL

    if turn:
        state = DISABLED

    up = Button(window, image=butImg[0], command=countUP, borderwidth = 0, state=state)
    up.place(x = W_Width*5/6-145, y=465, width=120, height=40)
    up.update()

    down = Button(window, image=butImg[1], command=countDown, borderwidth = 0, state=state)
    down.place(x = W_Width*5/6-145, y=605, width=120, height=40)
    down.update()

    all = Button(window, image=butImg[2], command=All, borderwidth = 0, state=state)
    all.place(x = W_Width*5/6+25, y=605, width=120, height=40)    
    all.update()

    die = Button(window, image=butImg[3], command=lambda : Die(butImg), borderwidth = 0, state=state)
    die.place(x = W_Width*5/6+25, y=465, width=120, height=40)
    die.update()

    betting = Button(window, image=butImg[4], command=lambda : Check(butImg), borderwidth = 0, state=state)
    betting.place(x = W_Width*5/6-60, y=535, width=120, height=40)
    betting.update()

    rule = Button(window, image=butImg[5], command=Rule, borderwidth = 2)
    rule.place(x=10,y=10,width=35, height=35)
    rule.update()

def Label_place():
    Main_Label = Label(window, text = "Gambling Board", font = ("",20), fg = "green",bg="white")
    Main_Label.place(x = W_Width*5/6-100, y = 20)

    PMoney_Label = Label(window, text = "나의 보유 칩", bg="white")
    PMoney_Label.place(x = W_Width*5/6-145, y = W_Height / 2 - 280, width = 120, height = 40)
    PMoney_Value = Label(window, text = Gamer_Money[0], bg = "white", relief="ridge", width = 120, height = 40)
    PMoney_Value.place(x = W_Width * 2 / 3 + 240, y = W_Height / 2 - 280, width = 120, height = 40)

    CMoney_Label = Label(window, text = "상대 보유 칩", bg="white")
    CMoney_Label.place(x = W_Width*5/6-145, y = W_Height / 2 - 240, width = 120, height = 40)
    CMoney_Value = Label(window, text = Gamer_Money[1], bg = "white", relief="ridge", width = 120, height = 40)
    CMoney_Value.place(x = W_Width * 2 / 3 + 240, y = W_Height / 2 - 240, width = 120, height = 40)

    TMoney_Label = Label(window, text = "테이블 전체 칩", bg="white")
    TMoney_Label.place(x = W_Width*5/6-145, y = W_Height / 2 - 200, width = 120, height = 40)
    TMoney_Value = Label(window, text = Table_Money, bg = "white", relief="ridge", width = 120, height = 40)
    TMoney_Value.place(x = W_Width * 2 / 3 + 240, y = W_Height / 2 - 200, width = 120, height = 40)

    Cbetting_Label = Label(window, text = "상대 배팅액", bg="white")
    Cbetting_Label.place(x = W_Width*5/6-145, y = W_Height / 2 - 80, width = 120, height = 40)
    Cbetting_Value = Label(window, text = player_bet[1], bg = "white", relief="ridge", width = 120, height = 40)
    Cbetting_Value.place(x = W_Width * 2 / 3 + 240, y = W_Height / 2 - 80, width = 120, height = 40)

    Pbetting_Label = Label(window, text = "나의 배팅액", bg="white")
    Pbetting_Label.place(x = W_Width*5/6-145, y = W_Height / 2 - 40, width = 120, height = 40)
    Pbetting_Value = Label(window, text = Temp_Money, bg = "white", relief="ridge", width = 120, height = 40)
    Pbetting_Value.place(x = W_Width * 2 / 3 + 240, y = W_Height / 2 - 40, width = 120, height = 40)

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

def com_Betting(butImg):
    global turn
    global betting_Check
    global Table_Money
    global Temp_Money

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
                if Gamer_Money[0] == 0:
                    player_bet[1] = com_beforeBet + player_beforeBet
                else:
                    player_bet[1] = com_beforeBet + random.randrange(player_beforeBet, Gamer_Money[1]+1)
        Table_Money += player_bet[1] - com_beforeBet
        Gamer_Money[1] -= player_bet[1] - com_beforeBet
        if Gamer_Money[1] == 0 and player_beforeBet > 0 and player_bet[0] >= player_bet[1]:
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
    Button_place(butImg)
        

def cardImageSet():
    global Image_height
    global Image_width
    img = []
    resized_img = []
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\Card Design\\"

    for i in range(11):
        img.append(Image.open(path + str(i) + '.png'))
        img[i] = img[i].resize((img[i].size[0]//4, img[i].size[1]//4), Image.ANTIALIAS)
        resized_img.append(ImageTk.PhotoImage(img[i]))
    
    Image_width = img[0].size[0]
    Image_height = img[0].size[1]

    return resized_img

def WindowUpdate():
    try:
        window.update()
    except:
        sys.exit()

def Intro():
    backgrond = Image.open(os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\View Design\\Intro View.png")
    backgrond2 = ImageTk.PhotoImage(backgrond)
    start = Label(image=backgrond2)
    start.pack();
    WindowUpdate()
    time.sleep(3)
    start.destroy()

def ButtonImageSet():
    img = []
    resized_img = []
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\Button Design\\"

    img.append(Image.open(path + "Up Button.png"))
    img.append(Image.open(path + "Down Button.png"))
    img.append(Image.open(path + "All in Button.png"))
    img.append(Image.open(path + "Die Button.png"))
    img.append(Image.open(path + "Betting Button.png"))
    img.append(Image.open(path + "Setting Button.png"))

    for i in range(6):
        img[i] = img[i].resize((img[i].size[0]//2, img[i].size[1]//2), Image.ANTIALIAS)
        resized_img.append(ImageTk.PhotoImage(img[i]))

    return resized_img

if __name__ == "__main__":
    window_set()
    img = cardImageSet()
    butImg = ButtonImageSet()
    Intro()
    path = os.path.dirname(os.path.realpath(__file__)) + "\\Resource\\View Design\\Main View.png"
    back = Image.open(path)
    backgrond = ImageTk.PhotoImage(back)
    C = Canvas(window, width=W_Width, height=W_Height)
    C.pack()
    C.create_image(0,0,anchor=NW, image=backgrond)

    while (Gamer_Money[0] != 0 and Gamer_Money[1] != 0) or winner == 2:
        cardImg = []
        init()
        Roll()
        Label_place()
        Button_place(butImg)

        if Gamer_Money[0] == 0 or Gamer_Money[1] == 0:
            betting_Check = False

        cardImg.append(Label(window, image=img[computer_Card[0]], borderwidth = 0))
        cardImg.append(Label(window, image=img[share_Card[0]], borderwidth = 0))
        cardImg.append(Label(window, image=img[share_Card[1]], borderwidth = 0))
        cardImg.append(Label(window, image=img[0], borderwidth = 0))
        cardImg.append(Label(window, image=img[player_Card[0]], borderwidth = 0))
        cardImg.append(Label(window, image=img[0], borderwidth = 0))
        cardImg.append(Label(window, image=img[0], borderwidth = 0))
        cardImg.append(Label(window, image=img[0], borderwidth = 0))
            
        cardImg[5].place(x=W_Width/3-Image_width/2, y=20)
        cardImg[6].place(x=W_Width/3 - Image_width*3/2, y=W_Height/2 - Image_height//2)
        cardImg[7].place(x=W_Width/3 + Image_width/2, y=W_Height/2 - Image_height//2)
        cardImg[3].place(x=W_Width/3-Image_width/2, y= W_Height - Image_height-20)
        WindowUpdate()
        time.sleep(2)
        cardImg[5].destroy()
        cardImg[6].destroy()
        cardImg[7].destroy()

        cardImg[0].place(x=W_Width/3-Image_width/2, y=20)
        cardImg[1].place(x=W_Width/3 - Image_width*3/2, y=W_Height/2 - Image_height//2)
        cardImg[2].place(x=W_Width/3 + Image_width/2, y=W_Height/2 - Image_height//2)
        WindowUpdate()
        

        while betting_Check:
            if turn == 1:
                com_Betting(butImg)
            WindowUpdate()
            
        cardImg[4].place(x=W_Width/3-Image_width/2, y= W_Height - Image_height-20)
        time.sleep(1)
        WindowUpdate()
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
        Label_place()
        WindowUpdate()
        

    if Gamer_Money[0] == 0:
        messagebox.showinfo("Final Winner", "Final Winner : Computer")
    else:
        messagebox.showinfo("Final Winner", "Final Winner : Player")
    sys.exit()