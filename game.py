from common import *

WIDTH, HEIGHT = 1000, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Three Body Problem Simulation")

lock_row, lock_col = (3, 7)
lock_list = [[0]*lock_col]*lock_row

class Body:
    def __init__(self, bodydata, color, size):
        self.x = bodydata.x_position
        self.y = bodydata.y_position
        self.mass = bodydata.mass
        self.vx = bodydata.x_velocity
        self.vy = bodydata.y_velocity
        self.path = [(self.x, self.x)]
        self.color = color
        self.size = size

    def update_velocity(self, bodies, dt):
        for body in bodies:
            if body != self:
                dx = body.x - self.x
                dy = body.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < 50:
                    distance = 50
                force = self.mass * body.mass / distance ** 2
                angle = math.atan2(dy, dx)
                self.vx += force * math.cos(angle) / self.mass * dt
                self.vy += force * math.sin(angle) / self.mass * dt

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.path.append((self.x, self.y))

    def draw(self, selected_body):
        if selected_body == self:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size*2)
        else:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size)

    def drawpath(self):
        for i in range(len(self.path) - 1):
            pygame.draw.line(win, self.color, self.path[i], self.path[i + 1], 1)

class BodyData(NamedTuple):
    x_position: float
    y_position: float
    x_velocity: float
    y_velocity: float
    mass: float

bodydataA    = BodyData(550, 400, 0, 0, 10)
bodydataB    = BodyData(400, 600, 0, 0, 10)
bodydataC    = BodyData(350, 500, 0, 0, 10)
bodydataMain = BodyData(300, 400, 0, 0, 1)

bodyA =    Body(bodydataA,    (255, 0, 0), 10)
bodyB =    Body(bodydataB,    (0, 255, 0), 10)
bodyC =    Body(bodydataC,    (0, 0, 255), 10)
bodyMain = Body(bodydataMain, (0, 0, 0), 1)

bodies = [bodyA, bodyB, bodyC, bodyMain]

dt = 5
distance_offset = 50

class game:
    def __init__(self) -> None:
        self.GameManager = "start"
        self.selected_body = None
        self.setting_move = False

    def game_loop(self):
        win.fill((200, 200, 200))
        if self.GameManager == "setting":
            self.handle_settings()
            bodyMain.drawpath()
            for body in bodies:
                body.draw(self.selected_body)
        if self.GameManager == "start":
            #init bodies and restart
            self.GameManager = "running"
        if self.GameManager == "running":
            bodyMain.drawpath()
            for body in bodies:
                body.draw(None)
                body.update_velocity(bodies, dt)
                body.update_position(dt)
            for row in range(lock_row):
                for col in range(lock_col):
                    if lock_list[row][col] == 0 and check_body_distance(bodies[row], bodyMain) == distance_offset*(col+1):
                        lock_list[row][col] = 1
    
    def handle_settings(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Settings Mode: Drag and place bodies, Press Enter to confirm", True, (0, 0, 0))
        win.blit(text, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for body in bodies:
                    if math.hypot(body.x - event.pos[0], body.y - event.pos[1]) < 23:
                        self.selected_body = body
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.GameManager = "running"
                if event.key == pygame.K_x:
                    self.selected_body = None
                if event.key == pygame.K_m:
                    self.setting_move = not self.setting_move


        if self.selected_body:
            if self.setting_move:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.selected_body.x = mouse_x
                self.selected_body.y = mouse_y
            text = font.render(f"({self.selected_body.x}, {self.selected_body.y})", True, (0, 0, 0))
            win.blit(text, (50, 700))

def check_body_distance(b1: Body, b2: Body) -> int:
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return int(distance)

def print_setting():
    pass