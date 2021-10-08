from ursina import *
import random


app = Ursina()

def reset_grid(grid):
    for i in grid:
        for j in i:
            j.alive = False
            j.color = color.white


'''
Setting up all global variable that each class use to run the game
'''

to_kill = []
to_alive = []
grid = [[None for _ in range(150)] for _ in range(150)]
living_rule = [True if i == 3 else False for i in range(9)]
dying_rule = [False if i in [2, 3] else True for i in range(9)]
print(living_rule, dying_rule)
speed = 3
timing = 0
playing = False
simulation_speed = 5

'''
Setting up all class that inherit from Entity() class from Ursina
Basically each object in the game is an Entity

defined class :

- Play Button
- Cases
'''
class RandomButton(Button):
    global grid
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model = 'quad',
            texture = 'assets/random_button.png',
            highlight_color = color.light_gray,
            scale = (0.1,0.1),
            origin = (.1,.1),
            position = (-0.83,.36),
            color = color.white
        )

    def input(self, key):

        global grid
        
        if self.hovered:
            
            if key == 'left mouse down':
                reset_grid(grid)
                for i in grid:
                    for j in i:
                        if random.randint(0, 10) >= 7:
                            j.alive = True
                            j.color = color.black

class PlayButton(Button):
    global playing

    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            texture = 'assets/pause_button.png',
            highlight_color = color.light_gray,
            scale = (0.1, 0.1),
            origin = (0.1, 0.1),
            position = (-0.83,.46),
            color = color.white
        )

    def input(self, key):
        global playing
        if self.hovered:
            if key == 'left mouse down':
                if not playing:
                    playing = True
                    self.texture = 'assets/play_button.png'
                elif playing:
                    playing = False
                    self.texture = 'assets/pause_button.png'

    
class Case(Button):

    global grid
    global simulation_speed
    global timing

    def __init__(self, pos, grid_location, **kwargs):
        super().__init__(
            parent = scene,
            position = pos,
            model = "quad",
            color = color.white,
            highlight_color = color.lime,
            scale = (1,1),
            texture = 'assets/grid_case.png'
        )
        self.grid_location = grid_location
        self.alive = False

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                if not self.alive:
                    self.alive = True
                    self.color = color.black
                elif self.alive:
                    self.alive = False
                    self.color = color.white

    def update(self):
        global grid
        global timing
        global living_rule
        global dying_rule
        global simulation_speed

        if timing == simulation_speed - 2:
            alive_count = 0 
            x, y = self.grid_location
            for i in range(y-1, y+2):
                for j in range(x-1, x+2):
                    if (0 <= j < len(grid)) and (0 <= i < len(grid)):
                        if (j,i) != (x,y):
                            if grid[i][j].alive:
                                alive_count += 1
            if self.alive:
                if dying_rule[alive_count]:
                    to_kill.append((x,y))
            elif not self.alive:
                if living_rule[alive_count]:
                    to_alive.append((x,y))
                    
                        

'''
Setting up the UI
'''
play_button = PlayButton()
random_button = RandomButton()

'''
Setting up the cases grid for the game
'''
                    
for y in range(len(grid)):
    for x in range(len(grid)):
        grid[y][x] = Case(pos = (-len(grid)//2 + x, -len(grid)//2 + y), grid_location = (x,y))


'''
event detection
'''

def input(key):
    global speed
    if key == '+':
        speed += 1.5
    if key == '-':
        speed -= 1.5


def update():

    global grid
    global to_kill
    global to_alive
    global speed
    global timing
    global simulation_speed

    if held_keys['q']:
        camera.x -= speed * time.dt
    if held_keys['d']:
        camera.x += speed * time.dt
    if held_keys['z']:
        camera.y += speed * time.dt
    if held_keys['s']:
        camera.y -= speed * time.dt
    if held_keys['space']:
        camera.z -= 10 * time.dt
    if held_keys['shift']:
        camera.z += 10 * time.dt

    
    if playing:
        timing += 1

    if timing == simulation_speed - 1:
        for x,y in to_kill:
            grid[y][x].alive = False
            grid[y][x].color = color.white
        for x,y in to_alive:
            grid[y][x].alive = True
            grid[y][x].color = color.black
        to_kill = []
        to_alive = []
    if timing == simulation_speed:
        timing = 0

'''
run app
'''
app.run()
