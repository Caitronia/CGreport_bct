import pygame
import random

pygame.init()

# screen setup
width, height = 800, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PLINKO - Neon Edition")
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)

# physics
gravity = 0.25
ball_radius = 18
peg_radius = 14
rows = 10
cols = 9
bin_height = 160

class Ball:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocity.y += gravity
        self.velocity *= 0.995
        self.position += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, RED,
                           (int(self.position.x), int(self.position.y)),
                           ball_radius)

# pegs
pegs = []
spacing_x = width // cols
spacing_y = 70
start_y = 200

for row in range(rows):
    offset = spacing_x // 2 if row % 2 == 0 else 0
    for col in range(cols - (row % 2)):
        x = col * spacing_x + offset + spacing_x // 2
        y = start_y + row * spacing_y
        pegs.append(pygame.math.Vector2(x, y))

# bins
bin_width = width // cols
bins = []
for i in range(cols):
    bins.append(pygame.Rect(i * bin_width,
                            height - bin_height,
                            bin_width,
                            bin_height))

# multipliers
center = cols // 2
multipliers = []
for i in range(cols):
    distance = abs(i - center)
    multipliers.append(max(1, 10 - distance * 2))

balls = []
score = 0

title_font = pygame.font.SysFont("arial", 60, bold=True)
multiplier_font = pygame.font.SysFont("arial", 36, bold=True)
score_font = pygame.font.SysFont("arial", 32, bold=True)

running = True

# MAIN LOOP
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(width // 2 + random.randint(-20, 20), 100))

    # title
    title = title_font.render("PLINKO", True, NEON_BLUE)
    screen.blit(title, (width//2 - title.get_width()//2, 40))

    # pegs
    for peg in pegs:
        pygame.draw.circle(screen, WHITE,
                           (int(peg.x), int(peg.y)), peg_radius)

    # balls
    for ball in balls[:]:
        ball.update()

        for peg in pegs:
            offset = ball.position - peg
            distance = offset.length()

            if 0 < distance < ball_radius + peg_radius:
                normal = offset.normalize()
                ball.position = peg + normal * (ball_radius + peg_radius)
                ball.velocity = ball.velocity.reflect(normal) * 0.75

        if ball.position.y >= height - bin_height:
            for i, b in enumerate(bins):
                if b.collidepoint(ball.position.x, ball.position.y):
                    score += multipliers[i] * 10
                    balls.remove(ball)
                    break

        ball.draw(screen)

    # bins
    for i, b in enumerate(bins):
        color = NEON_PINK if multipliers[i] == max(multipliers) else NEON_BLUE
        pygame.draw.rect(screen, (30,30,30), b)
        pygame.draw.rect(screen, color, b, 4)

        text = multiplier_font.render(f"{multipliers[i]}x", True, NEON_YELLOW)
        screen.blit(text, text.get_rect(center=b.center))

    # score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

pygame.quit()