from datetime import datetime as dt
import pygame
from random import randint
import sys
import utility as u

SCRW = 1600
SCRH = 1000
FPS = 10000
SQUARESIZE = 10

COLOURMODE = 2

pygame.init()
SCREEN = pygame.display.set_mode((SCRW,SCRH))
pygame.display.set_caption("A randomly generated maze")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

class Maze:
    def __init__(self,width,height,size,colourMode):
        self.width = width
        self.height = height
        self.size = size
        self.colourMode = colourMode

        self.cells = []
        self.walls = []
        self.sets = []
        self.cols = []

        print(f"width {width}, height {height}")

        for y in range((self.height*2)-1):
            self.cells.append([])
            if y%2 == 0:
                # paths
                for x in range((self.width)-1):
                    if x%2 == 0:
                        self.cells[y].append("path")
                        self.sets.append([[x,y]])
                    else:
                        self.cells[y].append("not path")
                        self.walls.append([x,y,"h"])
            else:
                #only walls
                for x in range((self.width)-1):
                    if x%2 == 0:
                        self.walls.append([x,y,"v"])
                    else:
                        self.cells[y].append("not path")

        # now init the rainbow for set colours
        rgb = u.Rainbow()
        maxSets = self.width*self.height
        for _ in range(maxSets):
            self.cols.append(rgb.get())
            for _ in range(16):
                rgb.tick()

    def tick(self):

        # pick random wall
        if len(self.walls) == 0:
            return None

        x,y,orn = self.walls[randint(0,len(self.walls)-1)]
        if orn == "h": # if horizontally separating wall
            cellA = [x-1, y]
            cellB = [x+1, y]
        else:
            cellA = [x, y-1]
            cellB = [x, y+1]

        self.draw_cell(cellA,(255,0,0))
        self.draw_cell(cellB, (255, 0, 0))

        # not check if the cells are in the same set
        setA, setB = [],[]
        for item in self.sets:
            #print(f"cellA {cellA}, set {item}")
            if cellA in item:
                #print("A Found yay")
                setA = item
                break

        for item in self.sets:
            if cellB in item:
                #print(f"cellB {cellB}, set {item}")
                setB = item
                #print("B Found yay")
                break

        if setA == [] or setB == []:
            #print("not found")
        #    raise NotImplementedError("Something broke")
            return None

        if setA != setB:
            # in different sets, connect them
            #print(self.cells)
            #print(f"cell width {len(self.cells)}, height {len(self.cells[y])}")
            #print(f"y {y}, x {x}")
            try:
                self.cells[x][y] = "path" # remove the wall
            except IndexError:
                pass
            self.sets.remove(setA)
            self.sets.remove(setB)
            newSet = []
            for which in [setA,setB]: # merge the sets
                for item in which:
                    newSet.append(item)
            newSet.append([x,y])
            self.sets.append(newSet)

        self.walls.remove([x, y, orn])

        if len(self.sets) == 1:
            self.walls = []

        return None

    def draw(self):
        if self.colourMode == 2:
            for i in range(len(self.sets)):
                for square in self.sets[i]:
                    self.draw_cell(square, self.cols[i])
        else:
            x, y = 0, 0
            for row in self.cells:
                for bit in row:
                    # print(f"x {x}\t y {y}")
                    # if self.cells[x][y] == "path":
                    if bit == "path":
                        col = (255, 255, 255)
                    else:
                        col = (0, 0, 0)
                    self.draw_cell((x, y), col)
                    y += 1
                x += 1
                y = 0

            if len(self.walls) != 0:
                for item in self.walls:
                    self.draw_cell([item[0],item[1]],(0,0,100))

    def draw_cell(self,pos,col):
        x = pos[0]
        y = pos[1]
        pygame.draw.rect(SCREEN, col,
                         (x * self.size, y * self.size, self.size, self.size))

def go_quit():
    print(f"Uptime {pygame.time.get_ticks()//1000} seconds")
    pygame.quit()
    sys.exit()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go_quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                go_quit()
            if event.key == pygame.K_s and False:
                name = "maze-generator-" + str(dt.now()) + ".png"
                pygame.image.save(SCREEN,name)#,"png")

maze = Maze(SCRW//SQUARESIZE,SCRH//SQUARESIZE,SQUARESIZE,COLOURMODE)

while True:
    pygame.display.flip()
    handle_events()
    SCREEN.fill((0, 0, 0))
    clock.tick(FPS)

    maze.draw()
    maze.tick()
    pygame.display.set_caption(
        f"Remaining walls: {len(maze.walls)} "
        f"| Uptime {pygame.time.get_ticks()//1000} "
        f"| Sets {len(maze.sets)}")
