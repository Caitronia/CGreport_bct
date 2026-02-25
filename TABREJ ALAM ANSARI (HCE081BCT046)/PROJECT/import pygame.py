import pygame
import random
import sys

# --------------------- Initialization ---------------------
pygame.init()

# Screen
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎯 Team Connect")

clock = pygame.time.Clock()
FPS = 60

# Fonts
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 60)
ui_font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

# Colors
BG1 = (102, 126, 234)
BG2 = (240, 147, 251)
WHITE = (255, 255, 255)
PURPLE = (120, 80, 200)
LIGHT = (240, 240, 255)
GREEN = (100, 200, 120)
BLACK = (0, 0, 0)

# Game settings
ROWS, COLS = 3, 4
CARD_SIZE = 120
PADDING = 20
BOARD_OFFSET_X = 80
BOARD_OFFSET_Y = 120

emojis = ['💼', '🚀', '💡', '🎨', '☕', '🌟']

# --------------------- Card Class ---------------------
class Card:
    def __init__(self, x, y, emoji):
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        self.emoji = emoji
        self.flipped = False
        self.matched = False
        self.flip_progress = 0
        self.animating = False

    def start_flip(self):
        if not self.animating and not self.matched:
            self.animating = True
            self.flip_progress = 0

    def update(self):
        if self.animating:
            self.flip_progress += 0.03  # slower & smooth flip
            if self.flip_progress >= 1:
                self.flip_progress = 1
                self.animating = False
                self.flipped = not self.flipped

    def draw(self):
        scale = abs(1 - self.flip_progress * 2)
        width = max(10, int(CARD_SIZE * scale))

        draw_rect = pygame.Rect(
            self.rect.centerx - width // 2,
            self.rect.y,
            width,
            CARD_SIZE
        )

        color = LIGHT if (self.flipped or self.matched) else PURPLE
        if self.matched:
            color = GREEN

        pygame.draw.rect(screen, color, draw_rect, border_radius=12)

        if (self.flipped or self.matched) and width > 40:
            text = emoji_font.render(self.emoji, True, BLACK)
            screen.blit(text, text.get_rect(center=draw_rect.center))

# --------------------- Confetti Particle ---------------------
class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(5, 12)
        self.color = random.choice([(102,126,234),(240,147,251),(255,215,0),(255,105,180),(76,220,196)])
        self.speed = random.uniform(2, 6)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5,5)

    def update(self):
        self.y += self.speed
        self.angle += self.rotation_speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)

# --------------------- Initialize Game ---------------------
def init_game():
    global cards, flipped, matches, moves, win, confettis
    pair_list = emojis * 2
    random.shuffle(pair_list)

    cards = []
    for r in range(ROWS):
        for c in range(COLS):
            x = BOARD_OFFSET_X + c * (CARD_SIZE + PADDING)
            y = BOARD_OFFSET_Y + r * (CARD_SIZE + PADDING)
            cards.append(Card(x, y, pair_list.pop()))

    flipped = []
    matches = 0
    moves = 0
    win = False
    confettis = [Confetti() for _ in range(50)]  # generate confetti

init_game()

# --------------------- Main Game Loop ---------------------
running = True
while running:
    clock.tick(FPS)

    # Gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = BG1[0]*(1-ratio) + BG2[0]*ratio
        g = BG1[1]*(1-ratio) + BG2[1]*ratio
        b = BG1[2]*(1-ratio) + BG2[2]*ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not win:
            for card in cards:
                if card.rect.collidepoint(event.pos):
                    if not card.flipped and not card.animating and not card.matched:
                        card.start_flip()
                        flipped.append(card)
                        if len(flipped) == 2:
                            moves += 1

    # Update cards
    for card in cards:
        card.update()

    # Check matches
    if len(flipped) == 2:
        if not flipped[0].animating and not flipped[1].animating:
            if flipped[0].emoji == flipped[1].emoji:
                flipped[0].matched = True
                flipped[1].matched = True
                matches += 1
            else:
                pygame.time.delay(600)  # pause before flipping back
                flipped[0].start_flip()
                flipped[1].start_flip()
            flipped = []

    # Check win
    if matches == len(emojis):
        win = True

    # Draw cards
    for card in cards:
        card.draw()

    # UI Panel
    pygame.draw.rect(screen, WHITE, (650, 100, 300, 200), border_radius=20)
    screen.blit(ui_font.render(f"Moves: {moves}", True, BLACK), (660, 120))
    screen.blit(ui_font.render(f"Matches: {matches}/6", True, BLACK), (660, 160))

    # Win screen & confetti
    if win:
        text = big_font.render("You Win!", True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH//2, 60)))

        # Update & draw confetti
        for conf in confettis:
            conf.update()
            conf.draw()

        # Draw Restart button
        restart_rect = pygame.Rect(WIDTH//2-80, HEIGHT-120, 160, 50)
        pygame.draw.rect(screen, PURPLE, restart_rect, border_radius=12)
        screen.blit(ui_font.render("Restart", True, WHITE), 
                    (restart_rect.x+30, restart_rect.y+10))

        # Check if restart clicked
        if pygame.mouse.get_pressed()[0]:
            if restart_rect.collidepoint(pygame.mouse.get_pos()):
                init_game()

    pygame.display.flip()

pygame.quit()
sys.exit()