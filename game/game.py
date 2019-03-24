import pygame
import random

pygame.init()
sc = pygame.display.set_mode((610, 610))
basket = pygame.image.load("pic/basket.png")
bj = pygame.image.load("pic/bj.jpg")
bomb = pygame.image.load("pic/bomb.png")
coin = pygame.image.load("pic/coin.png")
start = pygame.image.load("pic/start.jpg")
over = pygame.image.load("pic/over.jpg")
ihp = pygame.image.load("pic/hp.png")
btn_up = pygame.image.load("pic/btn_up.png")
btn_down = pygame.image.load("pic/btn_down.png")
bbtn_up = pygame.image.load("pic/bbtn_up.png")
bbtn_down = pygame.image.load("pic/bbtn_down.png")
word = "hp"
font = pygame.font.SysFont("", 32)
text = font.render(word, True, (75, 217, 65))
score = 0
text1 = font.render(str(score), True, (255, 255, 255))
bx = 0
lx, ly = [], []
fx, fy = [], []
speedy = 1
hp = 4
# 金币生成的序列,通过序列可以源源不断生成金币
for i in range(0, 4):
    tx = random.randint(0, 586)
    ty = (i - 1) * 150
    lx.append(tx)
    ly.append(ty)

# 炸弹生成的序列
for i in range(0, 2):
    x = random.randint(0, 586)
    y = (i - 1) * 300
    fx.append(x)
    fy.append(y)


# 按钮类和按钮点击事件
class Button(object):
    def __init__(self, btn_up, btn_down, position):
        self.btn_up = btn_up
        self.btn_down = btn_down
        self.position = position

    def isOver(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.btn_down.get_size()

        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def isPressed(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            point_x, point_y = pygame.mouse.get_pos()
            x, y = self.position
            w, h = self.btn_down.get_size()
            in_x = x - w / 2 < point_x < x + w / 2
            in_y = y - h / 2 < point_y < y + h / 2
            return True

    def render(self):
        w, h = self.btn_up.get_size()
        x, y = self.position

        if self.isOver():
            sc.blit(self.btn_down, (x - w / 2, y - h / 2))
        else:
            sc.blit(self.btn_up, (x - w / 2, y - h / 2))


button = Button(btn_up, btn_down, (288, 460))

bbutton = Button(bbtn_up, bbtn_down, (288, 460))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    # 游戏开始界面
    sc.blit(start, (0, 0))
    bbutton.render()
    if bbutton.isPressed():
        hp = 3
        score = 0
        text1 = font.render(str(score), True, (255, 255, 255))
    # 进入游戏
    if hp > 0 and hp < 4 and score >= 0:
        sc.blit(bj, (0, 0))
        sc.blit(text, (10, 583))
        sc.blit(text1, (570, 570))
        sc.blit(basket, (bx, 540))
        # 难度变化
        if score <= 50:
            speedy = 2
        if score > 100:
            speedy = 3
        if score > 150:
            speedy = 4
        if score > 175:
            speedy = 5
        for i in range(len(lx)):
            sc.blit(coin, (lx[i], ly[i] - 600))
            ly[i] += speedy
            if ly[i] > 610 + 600:
                ly[i] = 600
                lx[i] = random.randint(0, 540)
                score -= 5
                text1 = font.render(str(score), True, (255, 255, 255))
            # 篮子的宽62 高 48
            # 碰撞判断
            if lx[i] + 24 > bx and \
                    lx[i] + 24 < bx + 62 and \
                    ly[i] >= 1120 and \
                    ly[i] <= 1140:
                ly[i] = 600
                lx[i] = random.randint(0, 586)
                score += 10
                text1 = font.render(str(score), True, (255, 255, 255))
        for i in range(len(fx)):
            sc.blit(bomb, (fx[i], fy[i] - 600))
            fy[i] += speedy
            if fy[i] > 610 + 600:
                fy[i] = 600
                fx[i] = random.randint(0, 545)
            # 篮子的宽62 高 48
            # 碰撞判断
            if fx[i] + 24 > bx and \
                    fx[i] + 24 < bx + 62 and \
                    fy[i] >= 1120 and \
                    fy[i] <= 1140:
                hp -= 1
                fy[i] = 600
                fx[i] = random.randint(0, 586)

        # 篮子跟随鼠标运动
        if event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            bx = mx - 24
        if bx < 0:
            bx = 0
        if bx > 610 - 62:
            bx = 548
        # 通过键盘控制篮子
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or \
                keys[pygame.K_RIGHT]:
            bx += 5
        if keys[pygame.K_d] or \
                keys[pygame.K_LEFT]:
            bx += -5
        for i in range(0, hp):
            sc.blit(ihp, (22 * i + 40, 585))

    # 重新开始游戏
    if hp == 0 or score < 0:
        # 重新初始化游戏
        bx = 0
        speedy = 1
        # 金币生成的序列
        for i in range(len(lx)):
            lx[i] = random.randint(0, 586)
            ly[i] = (i - 1) * 150

        # 炸弹生成的序列
        for i in range(len(fx)):
            fx[i] = random.randint(0, 586)
            fy[i] = (i - 1) * 300
        sc.blit(over, (0, 0))
        button.render()
        # 点击按钮后重新开始游戏
        if button.isPressed():
            hp = 3
            score = 0
            text1 = font.render(str(score), True, (255, 255, 255))
    pygame.display.update()
