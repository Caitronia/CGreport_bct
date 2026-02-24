import pygame, sys, random, math
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Shooter RPG")
WHITE, BLACK, RED, GREEN, YELLOW, BLUE = (255,255,255), (0,0,0), (200,0,0), (0,200,0), (255,255,0), (0,0,200)
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 64)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.health = 100
        self.level = 1
        self.xp = 0
        self.fire_rate = 200  
        self.last_shot_time = 0
    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0: self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH: self.rect.x += self.speed
    def shoot(self, target):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.fire_rate:
            bullet_group.add(Bullet(self.rect.center, target))
            self.last_shot_time = now
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 50:
            self.level += 1
            self.xp = 0
            self.health += 20
            self.fire_rate = max(80, self.fire_rate - 20)
            print(f"LEVEL UP! Level {self.level}")
class Enemy(pygame.sprite.Sprite):
    def __init__(self, wave):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0,WIDTH), random.randint(0,HEIGHT)))
        self.speed = random.randint(1,2) + wave//3   # small increase every 5 waves
        self.health = 30 + (wave-1)*2                # +5 HP per wave
    def update(self, player):
        if self.rect.x < player.rect.x: self.rect.x += self.speed
        if self.rect.x > player.rect.x: self.rect.x -= self.speed
        if self.rect.y < player.rect.y: self.rect.y += self.speed
        if self.rect.y > player.rect.y: self.rect.y -= self.speed
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=pos)
        angle = math.atan2(target[1]-pos[1], target[0]-pos[0])
        self.dx = math.cos(angle)*12
        self.dy = math.sin(angle)*12
        self.damage = 10
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not screen.get_rect().colliderect(self.rect):
            self.kill()
class Item(pygame.sprite.Sprite):
    def __init__(self, pos, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((15,15))
        if kind == "health": self.image.fill(GREEN)
        elif kind == "xp": self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=pos)
player = Player()
player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
score, wave, enemies_to_spawn = 0, 1, 5
def main_menu():
    while True:
        screen.fill(BLACK)
        title = big_font.render("Survival Shooter RPG", True, WHITE)
        start = font.render("Press ENTER to Start", True, WHITE)
        quit_text = font.render("Press ESC to Quit", True, WHITE)
        screen.blit(title, (WIDTH//2-title.get_width()//2,150))
        screen.blit(start, (WIDTH//2-start.get_width()//2,300))
        screen.blit(quit_text, (WIDTH//2-quit_text.get_width()//2,350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
def game_loop():
    global score, wave, enemies_to_spawn
    score, wave, enemies_to_spawn = 0, 1, 5
    player.health, player.level, player.xp = 100, 1, 0
    player.fire_rate = 200
    enemy_group.empty()
    bullet_group.empty()
    item_group.empty()
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        player.shoot(pygame.mouse.get_pos())
        if len(enemy_group) == 0:
            wave += 1
            enemies_to_spawn += 2
            for _ in range(enemies_to_spawn):
                enemy_group.add(Enemy(wave))
        player.update(keys)
        for enemy in enemy_group: enemy.update(player)
        bullet_group.update()
        for bullet in bullet_group:
            hit_list = pygame.sprite.spritecollide(bullet, enemy_group, False)
            for enemy in hit_list:
                enemy.health -= bullet.damage
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10
                    player.gain_xp(10)
                    if random.random() < 0.3:
                        kind = random.choice(["health","xp"])
                        item_group.add(Item(enemy.rect.center, kind))

        if pygame.sprite.spritecollide(player, enemy_group, True):
            player.health -= 10
            if player.health <= 0: return
        for item in pygame.sprite.spritecollide(player, item_group, True):
            if item.kind == "health": player.health += 20
            elif item.kind == "xp": player.gain_xp(20)
        screen.fill(BLACK)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        item_group.draw(screen)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        wave_text = font.render(f"Wave: {wave}", True, WHITE)
        level_text = font.render(f"Level: {player.level} XP:{player.xp}", True, WHITE)
        screen.blit(health_text, (10,10))
        screen.blit(score_text, (10,50))
        screen.blit(wave_text, (10,90))
        screen.blit(level_text, (10,130))
        mx,my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, YELLOW, (mx,my), 10, 2)
        pygame.display.flip()
        clock.tick(60)
main_menu()
while True:
    game_loop()
    screen.fill(BLACK)
    over = big_font.render("GAME OVER", True, RED)
    restart = font.render("Press ENTER to Restart", True, WHITE)
    quit_text = font.render("Press ESC to Quit", True, WHITE)
    screen.blit(over, (WIDTH//2-over.get_width()//2,200))
    screen.blit(restart, (WIDTH//2-restart.get_width()//2,300))
    screen.blit(quit_text, (WIDTH//2-quit_text.get_width()//2,350))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: waiting = False
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

