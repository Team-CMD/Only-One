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

'''
def Button_place():
    call = Button(window, text="call", borderwidth = 4)
    call.place(x=1400, y=130, width=100, height=100)

    rai = Button(window, text="raize", borderwidth = 4)
    rai.place(x=1400, y=400, width=100, height=100)

    die = Button(window, text="die", borderwidth = 4)
    die.place(x=1400, y=700, width=100, height=100)
'''

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

def CardImage():
    global Image_height
    global Image_width
    label = []
    img = []
    resized_image = []
    path = os.path.dirname(os.path.realpath(__file__))
    path += "\\Image\\"

    img.append(Image.open(path + str(computer_Card[0]) + '.png'))
    img.append(Image.open(path + str(share_Card[0]) + '.png'))
    img.append(Image.open(path + str(share_Card[1]) + '.png'))
    img.append(Image.open(path + 'back.png'))
    img.append(Image.open(path + str(player_Card[0]) + '.png'))

    Image_width = img[0].size[0]//7
    Image_height = img[0].size[1]//7

    for i in range(len(img)):
        img[i] = img[i].resize((Image_width, Image_height), Image.ANTIALIAS)
        resized_image.append(ImageTk.PhotoImage(img[i]))

    return resized_image

if __name__ == "__main__":
    window_set()

    while True:
        label = []
        Roll()
        img = CardImage()
        for i in range(len(img)):
            label.append(Label(window, image=img[i]))
            
        label[0].place(x=W_Width/3, y=0)
        label[1].place(x=W_Width/3 - Image_width, y=W_Height/2 - Image_height//2)
        label[2].place(x=W_Width/3 + Image_width, y=W_Height/2 - Image_height//2)
        label[3].place(x=W_Width/3, y= W_Height - Image_height)
        window.update()

        while betting_Check:
            time.sleep(5)
            betting_Check = False
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


