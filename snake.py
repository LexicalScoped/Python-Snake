import pygame
import random

pygame.init()

block_size = 10
window_width = 600
window_height = 600

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "forest_green": (34, 139, 34),
    "blue": (0, 0, 255),
    "purple": (128, 0, 128),
    "light_blue": (173,216, 230),
    "orange": (255, 165, 0),
}

color_names = [ "red", "forest_green", "blue", "orange" ]

directions = {
    "none": (0, 0),
    "left": (-block_size, 0),
    "right": (block_size, 0),
    "up": (0, -block_size),
    "down": (0, block_size),
}

class snake():
    x = int(window_width / 2)
    y = int(window_height / 2)
    direction = directions["none"]
    color = colors["purple"]
    speed = 20
    body = []
    length = 1
    def reset_snake(self):
        self.x = int(window_width / 2)
        self.y = int(window_height / 2)
        self.direction = directions["none"]
        self.color = colors["purple"]
        self.speed = 20
        self.body = []
        self.length = 1
    def change_direction(self, direction):
        if self.direction == directions["left"] and direction == directions["right"]:
            return
        if self.direction == directions["right"] and direction == directions["left"]:
            return
        if self.direction == directions["up"] and direction == directions["down"]:
            return
        if self.direction == directions["down"] and direction == directions["up"]:
            return
        else:
            self.direction = direction
            return
    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
    def head(self):
        return [ self.x, self.y ]

class food():
    x = int(round(random.randrange(0, window_width - block_size) / 10.0) * 10.0)
    y = int(round(random.randrange(0, window_height - block_size) / 10.0) * 10.0)
    color = colors[random.choice(color_names)]
    def new_location(self):
        self.x = int(round(random.randrange(0, window_width - block_size) / 10.0) * 10.0)
        self.y = int(round(random.randrange(0, window_height - block_size) / 10.0) * 10.0)
        self.color = colors[random.choice(color_names)]


class Game():
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("SNEK")
    loop = True
    play = False
    clock = pygame.time.Clock()
    s = snake()
    f = food()
    def draw_snek(self):
        self.s.move()
        self.play = self.collision()
        self.s.body.append(self.s.head())
        if len(self.s.body) > self.s.length:
            del self.s.body[0]
        for block in self.s.body:
            pygame.draw.rect(self.window, self.s.color, [block[0], block[1], block_size, block_size])
        if self.s.body[-1]:
            if self.s.x < 0:
                self.s.x = window_width
            elif self.s.x >= window_width:
                self.s.x = 0
            if self.s.y < 0:
                self.s.y = window_height
            elif self.s.y >= window_height:
                self.s.y = 0
    def draw_food(self):
        pygame.draw.rect(self.window, self.f.color, [self.f.x, self.f.y, block_size, block_size])
    def eat_food(self):
        if self.s.x == self.f.x and self.s.y == self.f.y:
            self.s.length += 1
            self.f.new_location()
    def collision(self):
        if not self.s.direction == directions["none"]:
            for position in self.s.body:
                if self.s.x == position[0] and self.s.y == position[1]:
                    return False
            return True
        else:
            return True
    def menu(self):
        font = pygame.font.SysFont("Arial", 25)
        output = ["Press N for New Game", "Press Q to Quit", "Score: "+ str(self.s.length -1)]
        pos = 27
        for line in output:
            msg = font.render(line, True, colors["red"])
            self.window.blit(msg, [40, pos])
            pos += 27
    def run_game(self):
        self.s.reset_snake()
        self.f.new_location()
        self.play = True
        while self.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.play = False
                    self.loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.s.change_direction(directions["left"])
                    elif event.key == pygame.K_RIGHT:
                        self.s.change_direction(directions["right"])
                    elif event.key == pygame.K_UP:
                        self.s.change_direction(directions["up"])
                    elif event.key == pygame.K_DOWN:
                        self.s.change_direction(directions["down"])
            self.window.fill(colors["light_blue"])
            self.draw_food()
            self.draw_snek()
            pygame.display.update()
            self.eat_food()
            self.clock.tick(self.s.speed)
        return False

def execute():
    game = Game()
    while game.loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game.loop = False
                if event.key == pygame.K_n:
                    game.run_game()
        game.window.fill(colors["light_blue"])
        game.menu()
        pygame.display.update()
    pygame.quit()
    quit()


if __name__ == "__main__":
    execute()