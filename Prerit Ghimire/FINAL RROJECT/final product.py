import pygame,sys,random,math
pygame.init()
W,H=800,600
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("Survival Shooter RPG")
pygame.mouse.set_visible(False)
WHITE=(255,255,255);BLACK=(0,0,0);RED=(200,0,0);GREEN=(0,200,0);YELLOW=(255,255,0);BLUE=(0,0,200)
f=pygame.font.SysFont("Arial",32);bf=pygame.font.SysFont("Arial",64);clk=pygame.time.Clock()
high_score=0;max_level=1;most_waves=1
bullet_group=pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((40,40));self.image.fill(GREEN)
        self.rect=self.image.get_rect(center=(W//2,H//2))
        self.speed=5;self.health=100;self.level=1;self.xp=0;self.fire_rate=200;self.last_shot=0
    def update(self,keys):
        if keys[pygame.K_w]and self.rect.top>0:self.rect.y-=self.speed
        if keys[pygame.K_s]and self.rect.bottom<H:self.rect.y+=self.speed
        if keys[pygame.K_a]and self.rect.left>0:self.rect.x-=self.speed
        if keys[pygame.K_d]and self.rect.right<W:self.rect.x+=self.speed
    def shoot(self,t):
        now=pygame.time.get_ticks()
        if now-self.last_shot>=self.fire_rate:
            bullet_group.add(Bullet(self.rect.center,t));self.last_shot=now
    def gain_xp(self,a):
        self.xp+=a
        if self.xp>=self.level*50:
            self.level+=1;self.xp=0;self.health+=20;self.fire_rate=max(80,self.fire_rate-20)
class Enemy(pygame.sprite.Sprite):
    def __init__(self,wave):
        super().__init__()
        self.image=pygame.Surface((30,30));self.image.fill(RED)
        self.rect=self.image.get_rect(center=(random.randint(0,W),random.randint(0,H)))
        self.speed=random.randint(1,2)+wave//5;self.health=30+(wave-1)*5
    def update(self,p):
        if self.rect.x<p.rect.x:self.rect.x+=self.speed
        if self.rect.x>p.rect.x:self.rect.x-=self.speed
        if self.rect.y<p.rect.y:self.rect.y+=self.speed
        if self.rect.y>p.rect.y:self.rect.y-=self.speed
class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,t):
        super().__init__()
        self.image=pygame.Surface((8,8));self.image.fill(YELLOW)
        self.rect=self.image.get_rect(center=pos)
        a=math.atan2(t[1]-pos[1],t[0]-pos[0]);self.dx=math.cos(a)*12;self.dy=math.sin(a)*12;self.damage=10
    def update(self):
        self.rect.x+=self.dx;self.rect.y+=self.dy
        if not screen.get_rect().colliderect(self.rect):self.kill()
class Item(pygame.sprite.Sprite):
    def __init__(self,pos,kind):
        super().__init__()
        self.kind=kind;self.image=pygame.Surface((15,15))
        self.image.fill(GREEN if kind=="health" else BLUE)
        self.rect=self.image.get_rect(center=pos)
def txt(s,fn,col,y):
    r=fn.render(s,True,col);screen.blit(r,(W//2-r.get_width()//2,y))
def btn(label,y,mx,my):
    r=pygame.Rect(W//2-130,y,260,42)
    hov=r.collidepoint(mx,my)
    pygame.draw.rect(screen,(40,40,40) if not hov else (80,80,20),r)
    pygame.draw.rect(screen,YELLOW if hov else WHITE,r,2)
    t=f.render(label,True,YELLOW if hov else WHITE)
    screen.blit(t,(W//2-t.get_width()//2,y+8))
    return r
def main_menu():
    while True:
        screen.fill(BLACK)
        mx,my=pygame.mouse.get_pos()
        txt("Survival Shooter RPG",bf,WHITE,80)
        if high_score or max_level>1:
            txt(f"Best: {high_score}pts  Lvl:{max_level}  Waves:{most_waves}",f,YELLOW,160)
        r_start=btn("PLAY",210,mx,my)
        r_how=btn("HOW TO PLAY",265,mx,my)
        r_quit=btn("QUIT",320,mx,my)
        pygame.draw.circle(screen,YELLOW,(mx,my),10,2)
        pygame.display.flip();clk.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:return
                if e.key==pygame.K_ESCAPE:pygame.quit();sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                if r_start.collidepoint(mx,my):return
                if r_how.collidepoint(mx,my):how_to_play()
                if r_quit.collidepoint(mx,my):pygame.quit();sys.exit()
def how_to_play():
    lines=["HOW TO PLAY","","WASD - Move","Mouse - Aim","Auto fires at cursor","","Kill enemies for XP+items","Level up = more HP & fire speed","Green drop = +20 HP","Blue drop = +20 XP","","ESC - Back to menu"]
    while True:
        screen.fill(BLACK)
        mx,my=pygame.mouse.get_pos()
        for i,l in enumerate(lines):
            col=YELLOW if i==0 else WHITE
            fn=bf if i==0 else f
            txt(l,fn,col,60+i*38)
        r_back=btn("BACK",H-70,mx,my)
        pygame.draw.circle(screen,YELLOW,(mx,my),10,2)
        pygame.display.flip();clk.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:return
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                if r_back.collidepoint(mx,my):return
def game_over_screen(score,wave,kills):
    global high_score,max_level,most_waves
    new_hs=score>high_score;new_lv=player.level>max_level;new_wv=wave>most_waves
    high_score=max(high_score,score);max_level=max(max_level,player.level);most_waves=max(most_waves,wave)
    while True:
        screen.fill(BLACK)
        mx,my=pygame.mouse.get_pos()
        txt("GAME OVER",bf,RED,60)
        rows=[("Score",score,YELLOW,new_hs),("Level",player.level,WHITE,new_lv),("Wave",wave,WHITE,new_wv),("Kills",kills,RED,False)]
        for i,(lbl,val,col,is_new) in enumerate(rows):
            ls=f.render(lbl,True,WHITE);vs=f.render(str(val),True,col)
            screen.blit(ls,(W//2-180,165+i*40));screen.blit(vs,(W//2+60,165+i*40))
            if is_new:screen.blit(f.render("NEW BEST!",True,YELLOW),(W//2+120,165+i*40))
        txt(f"All-time: {high_score}pts  Lvl:{max_level}  Waves:{most_waves}",f,YELLOW,345)
        r_play=btn("PLAY AGAIN",400,mx,my)
        r_menu=btn("MAIN MENU",455,mx,my)
        pygame.draw.circle(screen,YELLOW,(mx,my),10,2)
        pygame.display.flip();clk.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:return"restart"
                if e.key==pygame.K_ESCAPE:return"menu"
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                if r_play.collidepoint(mx,my):return"restart"
                if r_menu.collidepoint(mx,my):return"menu"
def game_loop():
    global player
    player=Player()
    pg=pygame.sprite.Group(player);eg=pygame.sprite.Group();ig=pygame.sprite.Group()
    bullet_group.empty()
    score=0;wave=1;n=5;kills=0
    for _ in range(n):eg.add(Enemy(wave))
    while True:
        keys=pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:return"menu",score,wave,kills
        player.shoot(pygame.mouse.get_pos())
        if not eg:
            wave+=1;n+=2
            for _ in range(n):eg.add(Enemy(wave))
        player.update(keys)
        for en in eg:en.update(player)
        bullet_group.update()
        for b in list(bullet_group):
            for en in pygame.sprite.spritecollide(b,eg,False):
                en.health-=b.damage;b.kill()
                if en.health<=0:
                    en.kill();score+=10;kills+=1;player.gain_xp(10)
                    if random.random()<0.3:ig.add(Item(en.rect.center,random.choice(["health","xp"])))
        if pygame.sprite.spritecollide(player,eg,True):
            player.health-=10
            if player.health<=0:return"dead",score,wave,kills
        for it in pygame.sprite.spritecollide(player,ig,True):
            if it.kind=="health":player.health+=20
            else:player.gain_xp(20)
        screen.fill(BLACK);pg.draw(screen);eg.draw(screen);bullet_group.draw(screen);ig.draw(screen)
        hud=[f"HP:{player.health}",f"Lvl:{player.level} XP:{player.xp}/{player.level*50}",f"Score:{score}",f"Wave:{wave}",f"Kills:{kills}"]
        for i,h in enumerate(hud):screen.blit(f.render(h,True,WHITE),(10,10+i*34))
        mx,my=pygame.mouse.get_pos()
        pygame.draw.circle(screen,YELLOW,(mx,my),10,2)
        pygame.display.flip();clk.tick(60)
player=Player()
while True:
    main_menu()
    while True:
        res,score,wave,kills=game_loop()
        if res=="menu":break
        out=game_over_screen(score,wave,kills)
        if out=="menu":break