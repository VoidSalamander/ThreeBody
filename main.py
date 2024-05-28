import pygame
import math
from music21 import *

pygame.init()
pygame.mixer.init()

# Load sound files
pygame.mixer.music.load('output.mid')

part1 = stream.Part()
part2 = stream.Part()
part3 = stream.Part()

WIDTH, HEIGHT = 1000, 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Body Problem Simulation")
blueBlackLock = [False]*5
greenBlackLock = [False]*5
redBlackLock = [False]*5
active = True

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


body1 = Body(WIDTH // 2 - 60.8, HEIGHT // 2, 0, 0, 1, (0, 0, 255), 10)
body2 = Body(WIDTH // 2 + 61.1, HEIGHT // 2, 0, 0, 1, (0, 255, 0), 10)
body3 = Body(WIDTH // 2, HEIGHT // 2 + 61.5 * math.sqrt(3), 0, 0, 1, (255, 0, 0), 10)
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

def play_sound(small_body, large_body, distance, lock:bool, color, sound, part):
    if check_body_distance(large_body, small_body) < distance and lock:
        n = note.Note(sound)
        n.quarterLength = math.sqrt(small_body.vx ** 2 + small_body.vy ** 2)*15
        n.volume.velocity = 127
        part.append(n)
        large_body.color = (0, 0, 0)
        lock = False
    elif check_body_distance(large_body, small_body) >= distance:
        large_body.color = color
        lock = True
    return lock

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

    for i in range(5):
        blueBlackLock[i] = play_sound(body4, body1, 50*(i+1), blueBlackLock[i], (0, 0, 255), 50+i*5, part1)
    
    for i in range(5):
        greenBlackLock[i] = play_sound(body4, body2, 50*(i+1), greenBlackLock[i], (0, 255, 0), 60+i*2, part2)

    for i in range(5):
        redBlackLock[i] = play_sound(body4, body3, 50*(i+1), redBlackLock[i], (255, 0, 0), 70+i*2, part3)

    win.fill((200, 200, 200))

    bodies[3].drawpath()

    for body in bodies:
        body.draw()
    display_surface.blit(textShowPause, textRectShowPause)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

score = stream.Score()
score.append(part1)
score.append(part2)
score.append(part3)

score.show('midi')