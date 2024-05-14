import pygame
import math

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)

WIDTH, HEIGHT = 1000, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Body Problem Simulation")

pygame.mixer.music.load('output.mid')

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
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 30:
                    distance = 30
                force = self.mass * body.mass / distance**2
                angle = math.atan2(dy, dx)
                self.vx += force * math.cos(angle) / self.mass * dt
                self.vy += force * math.sin(angle) / self.mass * dt
                if body == bodies[3] and distance < 100 and distance > 99:
                    pygame.mixer.music.play()
                    print("OK")
    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.path.append((self.x, self.y))

    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size)
    
    def drawpath(self):
        for i in range(len(self.path) - 1):
            pygame.draw.line(win, self.color, self.path[i], self.path[i + 1], 1)

body1 = Body(WIDTH // 2 - 59.1, HEIGHT // 2,                        0, 0,    1,     (0, 0, 255), 10)
body2 = Body(WIDTH // 2 + 61.1, HEIGHT // 2,                        0, 0,    1,     (0, 255, 0), 10)
body3 = Body(WIDTH // 2, HEIGHT // 2 + 61 * math.sqrt(3),         0, 0,    1,     (255, 0, 0), 10)
body4 = Body(WIDTH // 2, HEIGHT // 2 + 60 * math.sqrt(3) + 31.1, 0.05, 0, 0.03, (100, 100, 100), 1)

bodies = [body1, body2, body3, body4]

clock = pygame.time.Clock()
dt = 10
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for body in bodies:
        body.update_velocity(bodies, dt)

    for body in bodies:
        body.update_position(dt)

    win.fill((200, 200, 200))

    #for effect in EffectList:
        #effect.draw()

    bodies[3].drawpath()

    for body in bodies:
        body.draw()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
