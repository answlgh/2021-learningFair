import pygame
import sys
from pygame.rect import *
import time
import random
from time import sleep





    
#####함수정의#####


    
def restart(): # 초기화
    global GameOver, score, life
    GameOver = False
    score = 0
    life = 100
    Ranking = []
    for i in range(len(ball)): 
        recBall[i].y = -1
        
    ####반복#####
    while running:
        # 1. 화면지움
        SCREEN.fill(('black'))

        # 2. 이벤트처리
        evenfprocess()
        # 3. 플레이어 이동
        movePlayer()
        # 4. 공 생성 및 이동
        moveBall()
        if life < 80:
            moveGift()
        # 5. 충돌확인
        touch()
        # 6. text업데이트
        setText()
        # 7. 화면갱신
        pygame.display.flip()
        clock.tick(100)

def evenfprocess(): # 버튼조작
     for event in pygame.event.get(): # 키조작리스트 for사용해서 가져오기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # esc 누르면 종료
                pygame.quit()
            if event.key == pygame.K_LEFT: # 왼쪽이동
                move.x = -1
            if event.key == pygame.K_RIGHT: # 오른쪽이동
                move.x = 1
            if event.key == pygame.K_UP: # 위로이동
                move.y = -1
            if event.key == pygame.K_DOWN: # 아래로 이동
                move.y = 1
            if event.key == pygame.K_r: # R 누르면 재시작
                restart()

                
                


def Rankingscore(): # 점수기록
    if GameOver:
        Ranking.append(score) # Ranking 리스트에 점수 추가
        Ranking.sort(reverse=True) # Ranking  내림차순정렬
        

        
def movePlayer(): # 플레이어 움직이기
    if not GameOver:    
        recPlayer.x += move.x 
        recPlayer.y += move.y

    if recPlayer.x < 0: # x가 0보다 작으면 0에서 멈추기
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH-recPlayer.width: # x가 스크린 가로보다 클 때 멈추기
        recPlayer.x = SCREEN_WIDTH-recPlayer.width

    if recPlayer.y < 0: # y가 0보다 작으면 0에서 멈추기
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT-recPlayer.height: # y가 스크린 세로보다 클 때 멈추기
        recPlayer.y = SCREEN_HEIGHT-recPlayer.height
        
    SCREEN.blit(player,recPlayer)

def timeDelay500ms(): # 생성하는 시간 0.5초 지연 발생시켜 공끼리 간격 만들기
    global time_delay_500ms
    if time_delay_500ms > 5: 
        time_delay_500ms = 0
        return True
    
    time_delay_500ms += 1
    return False

def makeball(): # 공 생성
    if  GameOver: # 게임오버면 공 생성 중단
        return
    if timeDelay500ms(): 
        index = random.randint(0,len(ball)-1) # 0 ~ 19까지 값 랜덤으로 가지고 오기
        if recBall[index].y == -1: # 실행 멈춘 값 가져오기(Flase)
            recBall[index].x = random.randint(0,SCREEN_WIDTH) # y는 0 ~ 가로(400)중 랜덤
            recBall[index].y = 0 # 값 실행하기(True)

    
def moveBall(): # 공 움직이기
    makeball()
    
    for i in range(len(ball)): 
        if recBall[i].y == -1: # -1인 값은 생성안된 값으로보고 continue로 지나가고 다시 for문 반복
            continue

        if not GameOver:        
            recBall[i].y += 1 # 공 y값 1씩 증
        if recBall[i].y > SCREEN_HEIGHT:
            recBall[i].y = 0 # y값이 스크린 세로값과 같으면 초기화
            recBall[i].x = random.randint(0,SCREEN_WIDTH) # x는 0 ~ 가로(400) 중 랜덤
    
        SCREEN.blit(ball[i],recBall[i])

def makegift(): # 선물 생성
    if  GameOver:
        return
    if timeDelay500ms():
        index1 = random.randint(0,len(gift)-1)
        if recGift[index1].y == -1: 
            recGift[index1].x = random.randint(0,SCREEN_WIDTH) # x는 0 ~ 가로(400) 중 랜덤
            recGift[index1].y = 0 

    
def moveGift(): # 선물 움직이기
    makegift()
    
    for j in range(len(gift)):
        if recBall[j].y == -1:
            continue

        if not GameOver:        
            recGift[j].y += 1
        if recGift[j].y > SCREEN_HEIGHT:
            recGift[j].y = 0
            recGift[j].x = random.randint(0,SCREEN_WIDTH)
            
            
            
            
        SCREEN.blit(gift[j],recGift[j])



def touch(): # 충돌
    global score,GameOver
    global life, GameOver
    global Ranking, GameOver

    if GameOver: # 게임오버일 경우 함수 종료
        return
    
    for rec in recBall:
        
        if rec.y == -1: # 가져 온 Rec의 값이 -1일 경우 닿았는지 확인하지 않고 지나가기 
            continue
        if rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec.left < recPlayer.right \
            and recPlayer.left < rec.right: # 공과 플레이어끼리 닿았는지 확인
            life -= 1 # 생명 1씩 감소
            
            if life == 0: # 생명이 0이 된다다면 게임오버, 순위 리스트 기록
                GameOver = True
                Rankingscore()
                break

    for rec in recGift:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec.left < recPlayer.right \
            and recPlayer.left < rec.right: # 생명이 100보다 작거나 같다면 50더하기
            if life <= 100:
                life += 50
            
    score += 1


def setText(): # 텍스트 
    game_Font = pygame.font.SysFont("Arial",20,True,False) # 폰트지정
    SCREEN.blit(game_Font.render(
        f'score : {score}',True,'white'),(10,10,0,0)) # x10 y10위치에 score 생성
    SCREEN.blit(game_Font.render(
        f'life : {life}',True,'white'),(10,30,0,0)) # x10 y30위치에 life 생성

    


    if GameOver: # 게임오버 상황에서 텍스트
        if len(Ranking):
            SCREEN.blit(game_Font.render(
                f'TOP 3 : {Ranking[:3]}',True,'gold'),(110,250,0,0))
    if GameOver and blinking():
        SCREEN.blit(game_Font.render(
            'Game Over!',True,'red'),(150,300,0,0))
        SCREEN.blit(game_Font.render(
            'Press R - Restart ',True,'orange'),(130,320,0,0))
        SCREEN.blit(game_Font.render(
            'Press ESC - Finish. ',True,'green'),(121,340,0,0))


def blinking(): # 게임오버문구 4초마다 깜빡거리게하기
    global time_delay_4sec, toggle
    time_delay_4sec += 1
    if time_delay_4sec > 40:
        time_delay_4sec = 0
        toggle = ~toggle

    return toggle
        


#변수
running = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0,0,0,0) # x,y,가로,세로 영억 Rect객체로 조작
time_delay_500ms = 0
score = 0
life = 100
Ranking = []
GameOver = False
time_delay_4sec = 0
toggle = False        

        




# 스크린생성
pygame.init() # 파이게임 초기화
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # 스크린 가로x세로 크기설정 
pygame.display.set_caption('알고리즘과 게임컨텐츠 6조') # 윈도우 타이틀 설정



# 플레이어 생성
player = pygame.image.load('resources/images/player.png') # 플레이어 이미지 로드
player = pygame.transform.scale(player,(30,40)) # 크기지정
recPlayer = player.get_rect() # 플레이어 좌표 생성
recPlayer.centerx = (SCREEN_WIDTH/2) # x좌표 센터 지정
recPlayer.centery = (SCREEN_WIDTH/2) # y좌표 센터 지정


# 공 생성
ballImage = ['resources/images/rock01.PNG', 'resources/images/rock02.PNG','resources/images/rock03.PNG','resources/images/rock04.PNG','resources/images/rock05.PNG',
             'resources/images/rock06.PNG','resources/images/rock07.PNG','resources/images/rock08.PNG','resources/images/rock09.PNG','resources/images/rock10.PNG',
             'resources/images/rock11.PNG','resources/images/rock12.PNG','resources/images/rock13.PNG','resources/images/rock14.PNG','resources/images/rock15.PNG',
             'resources/images/rock16.PNG', 'resources/images/rock17.PNG','resources/images/rock18.PNG','resources/images/rock19.PNG','resources/images/rock20.PNG',
             'resources/images/rock21.PNG','resources/images/rock22.PNG','resources/images/rock23.PNG','resources/images/rock24.PNG','resources/images/rock25.PNG',
             'resources/images/rock26.PNG','resources/images/rock27.PNG','resources/images/rock28.PNG','resources/images/rock29.PNG','resources/images/rock30.PNG',]
ball = [pygame.image.load(random.choice(ballImage)) for i in range(20)] # 공 이미지 중 랜덤으로 선택하여 20개 생성
recBall = [None for i in range(len(ball))] # 초기값 None 
for i in range(len(ball)): #
    ball[i] = pygame.transform.scale(ball[i],(20,20)) # 공사이즈 지정
    recBall[i] = ball[i].get_rect() 
    recBall[i].y = -1  # recball 값을 실행하지 않는다(False)


# 이벤트 선물 생성
gift = [pygame.image.load('resources/images/gift.png') for j in range(3)]
recGift = [None for j in range(len(gift))]
for j in range(len(gift)):
    gift[j] = pygame.transform.scale(gift[j],(30,30))
    recGift[j] = gift[j].get_rect()
    recGift[j].y = -1 


# 배경음악 로드 및 적용
pygame.mixer.music.load('resources/sounds/bgm.mp3')
pygame.mixer.music.set_volume(0.4)  # 볼륨 적용
pygame.mixer.music.play(-1)  # 반복할 숫자를 인자로 넣음. -1은 반복재생


# 시간
clock = pygame.time.Clock() 


            

def game_screen(): # 게임 시작 화면
    SCREEN.fill(('black'))

    
    game_Font = pygame.font.SysFont("Arial", 25, True, False)
    SCREEN.blit(game_Font.render(
        '- Game explanation -', True, 'YELLOW'), (105, 140, 0, 0))

    game_Font = pygame.font.SysFont("Arial", 20, True, False)
    SCREEN.blit(game_Font.render(
        'Press ←↑→↓  -  move player ', True, 'YELLOW'), (90, 200, 0, 0))
    SCREEN.blit(game_Font.render(
        'Meteorite hits reduce life. ', True, 'YELLOW'), (100, 230, 0, 0))
    SCREEN.blit(game_Font.render(
        'If life is less than 80, a gift is generated. ', True, 'YELLOW'), (50, 260, 0, 0))    
    SCREEN.blit(game_Font.render(
        'Eating a gift increases your life.. ', True, 'YELLOW'), (80, 290, 0, 0))  




    game_Font = pygame.font.SysFont("Arial", 25, True, False)
    SCREEN.blit(game_Font.render(
        'Press S - GAME START!', True, 'Blue'), (80, 380, 0, 0))
    SCREEN.blit(game_Font.render(
        'Press ESC - GAME END!', True, 'RED'), (80, 420, 0, 0))
    


        
    pygame.display.update()

    # 게임 시작 화면 키 설정
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return pygame.quit()
            elif event.key == pygame.K_s:
                return 'restart'  # 게임시작 'play'
        if event.type == quit:
            return pygame.quit()

    return 'game_screen'


# 실제실행
def Gamerunning():  # 메인루프
    action = 'game_screen'
    while action != 'GameOver':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'restart':  # 게임시작 'play'
            action = restart()  # 게임루프

    pygame.quit()


Gamerunning()


    
