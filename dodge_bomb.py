import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向の判定結果, 縦方向の判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    gm_sc = pg.Surface((WIDTH, HEIGHT))
    gm_sc.set_colorkey((255, 255, 0))
    font1 = pg.font.Font(None, 80)
    txt = font1.render("Game Over", True, (255, 255, 255))
    gm_sc.blit(txt, (400, 300))
    nk_img = pg.image.load("fig/8.png")
    gm_sc.blit(nk_img, (300, 300))
    gm_sc.blit(nk_img, (800, 300))
    screen.blit(gm_sc, (0, 0))
    pg.display.update()
    time.sleep(5)
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_dict = {
        (0, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (0, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 1),
        (0, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 1),
        (-5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (+5, 0):pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 1),
        (+5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 1),
        (-5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1),
        (+5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 1)
        } 
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  
    bb_rct.centerx = random.randint(0, WIDTH)  
    bb_rct.centery = random.randint(0, HEIGHT)  
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    kk_dict = get_kk_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        avx = vx * bb_accs[min(tmr//500, 9)] 
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] 
                sum_mv[1] += mv[1] 
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(avx, avy)
        bb_rct.width=bb_imgs[min(tmr//500, 9)].get_rect().width  
        bb_rct.height=bb_imgs[min(tmr//500, 9)].get_rect().height
        kk_img = kk_dict.get(tuple(sum_mv), kk_dict[(0, 0)])
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate: 
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
