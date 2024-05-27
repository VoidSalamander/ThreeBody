import pygame
import math
import threading

pygame.init()
pygame.mixer.init()

# Load sound files
pygame.mixer.music.load('output.mid')


WIDTH, HEIGHT = 1000, 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Body Problem Simulation")
blueBlackLock = False
greenBlackLock = False
redBlackLock = False
active = True


def play_sound():
    threading.Thread(target=pygame.mixer.music.play()).start()

class Body:
    def __init__(self, x, y, vx, vy, mass, color, size):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.path = [(x, y)]
        self.color = color
        self.size = size

    def update_velocity(self, bodies, dt):
        for body in bodies:
            if body != self:
                dx = body.x - self.x
                dy = body.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < 30:
                    distance = 30
                force = self.mass * body.mass / distance ** 2
                angle = math.atan2(dy, dx)
                self.vx += force * math.cos(angle) / self.mass * dt
                self.vy += force * math.sin(angle) / self.mass * dt

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.path.append((self.x, self.y))

    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size)

    def drawpath(self):
        for i in range(len(self.path) - 1):
            pygame.draw.line(win, self.color, self.path[i], self.path[i + 1], 1)


def check_body_distance(b1: Body, b2: Body):
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance


body1 = Body(WIDTH // 2 - 59.1, HEIGHT // 2, 0, 0, 1, (0, 0, 255), 10)
body2 = Body(WIDTH // 2 + 61.1, HEIGHT // 2, 0, 0, 1, (0, 255, 0), 10)
body3 = Body(WIDTH // 2, HEIGHT // 2 + 61 * math.sqrt(3), 0, 0, 1, (255, 0, 0), 10)
body4 = Body(WIDTH // 2, HEIGHT // 2 + 60 * math.sqrt(3) + 31.1, 0.05, 0, 0.03, (100, 100, 100), 1)

bodies = [body1, body2, body3, body4]

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Press R to continue.', True, (0, 255, 0), (0, 0, 128))
textRect = text.get_rect()
textRect.center = (WIDTH//2, HEIGHT // 2)
textShowPause = font.render('Press P to pause', True, (0, 255, 0), (0, 0, 128))
textRectShowPause = textShowPause.get_rect()
textRectShowPause.topright = (WIDTH - 10, 10)

dt = 10
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print("Timer paused. Press 'p' to resume.")
                active = False
            elif event.key == pygame.K_r:
                print("Timer resumed.")
                active = True

    # active is false
    if not active:
        # show paused message on the screen
        display_surface.blit(text, textRect)
        pygame.display.update()

        continue
    else:
        pass

    for body in bodies:
        body.update_velocity(bodies, dt)
    for body in bodies:
        body.update_position(dt)
    if check_body_distance(body1, body4) < 20 and blueBlackLock: # Blue Black
        print("Blue Black")
        pygame.mixer.music.play()
        body1.color = (0, 0, 0)
        blueBlackLock = False
    elif check_body_distance(body1, body4) >= 20:
        body1.color = (0, 0, 255)
        blueBlackLock = True
    if check_body_distance(body2, body4) < 20 and greenBlackLock: # Green Black
        print("Green Black")
        pygame.mixer.music.play()
        body2.color = (0, 0, 0)
        greenBlackLock = False
    elif check_body_distance(body2, body4) >= 20:
        greenBlackLock = True
        body2.color = (0, 255, 0)
    if check_body_distance(body3, body4) < 20 and redBlackLock: # Red Black
        print("Red Black")
        pygame.mixer.music.play()
        body3.color = (0, 0, 0)
        redBlackLock = False
    elif check_body_distance(body3, body4) >= 20:
        redBlackLock = True
        body3.color = (255, 0, 0)

    win.fill((200, 200, 200))

    bodies[3].drawpath()

    for body in bodies:
        body.draw()
    display_surface.blit(textShowPause, textRectShowPause)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
