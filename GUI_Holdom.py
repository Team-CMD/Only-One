import random, sys
import os
from tkinter import *
import PIL
from PIL import Image, ImageTk
import time

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
window = Tk()

# 윈도우 창의제목 설정 가능
# 윈도우 창의 너비와 높이, 초기 화면 위치 설정
# 윈도우 창의 크기 조절 가능 여부

def window_set():
    window.title("Holdom Game") 
    window.geometry(str(W_Width)+"x"+str(W_Height)+"+300+100") 
    window.resizable(False,False)

def cardCompare():
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

    if score[0] > score[1]:
        winner = 0
    elif score[0] == score[1]:
        winner = 2
    else:
        winner = 1

    return winner

def Call():
    pass

def Die():
    pass

def countUP():
    global Table_Money

    if Table_Money <= 40:
        Table_Money += 1
    else:
        Table_Money = 20 # 임시

def countDown():
    global Table_Money 

    if Table_Money >= 0:
        Table_Money -= 1
    else:
        Table_Money = 20 # 임시

def Check():
    global betting_Check

    betting_Check = False

def Button_place():
    up = Button(window, text="Up", command=countUP, borderwidth = 4, background="yellow")
    up.place(x=W_Width*2/3 + 30, y=W_Height/2+40, width=120, height=40)

    call = Button(window, text="Call", command=Call, borderwidth = 4, background="yellow")
    call.place(x=W_Width*2/3 + 30, y=W_Height/2+140, width=120, height=40)

    down = Button(window, text="Down", command=countDown, borderwidth = 4, background="yellow")
    down.place(x=W_Width*2/3 + 30, y=W_Height/2+240, width=120, height=40)

    die = Button(window, text="Die", command=Die, borderwidth = 4, background="yellow")
    die.place(x=W_Width*2/3+200, y=W_Height/2+90, width=120, height=40)

    check = Button(window, text="Check", command=Check, borderwidth = 4, background="yellow")
    check.place(x=W_Width*2/3+200, y=W_Height/2+190, width=120, height=40)

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

def cardImageSet():
    global Image_height
    global Image_width
    img = []
    resized_img = []
    path = os.path.dirname(os.path.realpath(__file__)) + "\\CardImage\\"

    for i in range(11):
        img.append(Image.open(path + str(i) + '.png'))
        img[i] = img[i].resize((img[i].size[0]//7, img[i].size[1]//7), Image.ANTIALIAS)
        resized_img.append(ImageTk.PhotoImage(img[i]))
    
    Image_width = img[0].size[0]
    Image_height = img[0].size[1]

    return resized_img


if __name__ == "__main__":
    window_set()
    img = cardImageSet()

    while True:
        Table_Money = 0
        label = []
        Roll()
        Button_place()
    
        label.append(Label(window, image=img[computer_Card[0]]))
        label.append(Label(window, image=img[share_Card[0]]))
        label.append(Label(window, image=img[share_Card[1]]))
        label.append(Label(window, image=img[0]))
        label.append(Label(window, image=img[player_Card[0]]))
            
        label[0].place(x=W_Width/3, y=0)
        label[1].place(x=W_Width/3 - Image_width, y=W_Height/2 - Image_height//2)
        label[2].place(x=W_Width/3 + Image_width, y=W_Height/2 - Image_height//2)
        label[3].place(x=W_Width/3, y= W_Height - Image_height)
        window.update()

        while betting_Check:
            window.update()
            # 베팅 함수 
        # 카드 공개
        label[4].place(x=W_Width/3, y= W_Height - Image_height)
        window.update()
        time.sleep(3)
        betting_Check = True

        winner = cardCompare()
        if winner == 2:
            pass # 비길경우
        else:
            pass

    window.mainloop()


