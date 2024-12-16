import pygame.display
import pygame.draw
import pygame.event
import pygame.key
import pygame.mouse
import pygame.rect
import pygame.time
import random

pygame.init()

screen = pygame.display.set_mode((750, 500)) # (W,H) 50 boxes in a row, 75 in a column
background = (100,0,175)
screen.fill(background)

running = True


#############################################READ ME#####################################################
#ALL USES OF PYGAME.TIME.DELAY(X) IS SO THE USER CAN SEE WHAT IS HAPPENING. IT IS PURELY FOR VISUAL EFFECT AND PLAYS NO ROLE IN THE ACTUAL RUNNING OF THE PROGRAM.
############################################Thank you####################################################




#class for each box, boxes will be the grid and will change color
class Box:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.walls = {"top": True, "bottom":True, "left":True, "right": True}
        self.color = (0,0,0)

    #draws the Box onto the screen
    def update_box(self):
        pygame.draw.rect(screen, self.color, (self.xPos, self.yPos, 10, 10)) #draws box

    #draws walls of Box
    def draw_walls(self):
        #builds the top wall
        if self.walls["top"]:
            pygame.draw.line(screen, (255,255,255), (self.xPos, self.yPos), (self.xPos + 10, self.yPos))

        #builds the bottom wall
        if self.walls["bottom"]:
            pygame.draw.line(screen, (255,255,255), (self.xPos, self.yPos + 10), (self.xPos + 10, self.yPos + 10))
        
        #builds the left wall
        if self.walls["left"]:
            pygame.draw.line(screen, (255,255,255), (self.xPos, self.yPos), (self.xPos, self.yPos + 10))

        #builds the right wall
        if self.walls["right"]:
            pygame.draw.line(screen, (255,255,255), (self.xPos + 10, self.yPos), (self.xPos + 10, self.yPos + 10))

#lists of all boxes and their coords
listOfBoxCoords = []
listOfBoxObj = []

#list of blocking boxes and their coords
listOfBlockBox = []
listOfBlockCoords = []
#adds boxes and their coordinates to lists
for row in range(50):
    for column in range(75):
        #print(f"row: {row}, column: {column}")
        listOfBoxObj.append(Box(column * 10,row * 10))
        listOfBoxCoords.append((column * 10,row * 10))


#draws boxes onto screen
for box in listOfBoxObj:
    box.update_box()
pygame.display.update()


#randomly chooses 1400 blocking boxes
def random_creation():
    for i in random.sample(listOfBoxObj, 1400):
        i.color = (175,0,0)
        i.update_box()
        i.draw_walls()
        listOfBlockBox.append(i)
        listOfBlockCoords.append((i.xPos,i.yPos))
        pygame.display.update()
        pygame.time.delay(1)

random_creation()    

#c is a coordinate, x and y are the x and y coordinates, respectively
def round_down(c):
    x,y = c
    return ((x//10) * 10, (y//10) * 10)

#returns start and end value
def get_click():
    clicks = 0
    start = (0,0)
    end = (0,0)

    t = True
    while t:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1
                if clicks == 1:
                    #selects start block
                    x,y = pygame.mouse.get_pos()
                    start = round_down((x,y))
                    print(f"start choosen: {start}")

                    #sets start block to purple
                    startBox = listOfBoxObj[listOfBoxCoords.index(start)]
                    startBox.color = (155,0,155)
                    startBox.update_box()
                    pygame.display.update()
                    
                elif clicks == 2:
                    #selects end block
                    x,y = pygame.mouse.get_pos()
                    end = round_down((x,y))
                    print(f"end choosen: {end}")
                    t = False

                    #sets end block to purple
                    endBox = listOfBoxObj[listOfBoxCoords.index(end)]
                    endBox.color = (155,0,155)
                    endBox.update_box()
                    pygame.display.update()
    return start,end

def find_neighbors(z):
    #neighbors of current index
    neighbors = []
    x,y = z


    if x > 0:
        neighbors.append((x - 10, y))      
    if x < 740:
        neighbors.append((x + 10, y))
    if y > 0:
        neighbors.append((x,y - 10))
    if y < 490:
        neighbors.append((x, y + 10))
        
    return neighbors



def change_neighbors(neighbor, current):

    neighborBoxObj = listOfBoxObj[listOfBoxCoords.index(neighbor)]
    currentBoxObj = listOfBoxObj[listOfBoxCoords.index(current)]

    #coressponding coordinate
    neighborBoxObj.checked = True
    neighborBoxObj.color = (0,190,0)

    #if neighbor is to the right of current box
    if neighborBoxObj.xPos > currentBoxObj.xPos:
        neighborBoxObj.walls["left"] = False
        currentBoxObj.walls["right"] = False
    #if neighbor is to the left of current box
    if neighborBoxObj.xPos < currentBoxObj.xPos:
        neighborBoxObj.walls["right"] = False
        currentBoxObj.walls["left"] = False

    #if neighbor is below current box
    if neighborBoxObj.yPos > currentBoxObj.yPos:
        neighborBoxObj.walls["top"] = False
        currentBoxObj.walls["bottom"] = False

    #if neighbor is aboveS current box
    if neighborBoxObj.yPos < currentBoxObj.yPos:
        neighborBoxObj.walls["bottom"] = False
        currentBoxObj.walls["top"] = False

    neighborBoxObj.update_box()
    neighborBoxObj.draw_walls()
    currentBoxObj.update_box()
    currentBoxObj.draw_walls()


def depth_search():

    #start is first square. end is goal. checks to make sure they are not border blocks
    start,end = get_click()
    if start in listOfBlockCoords:
        print(f"invalid start: {start}")
        pygame.time.delay(1000)
        pygame.quit()
        return -1

    #checks if valid end
    if end in listOfBlockCoords:
        print(f"invalid end {end}")
        pygame.time.delay(1000)
        pygame.quit()
        return -1

    print(f"start {start}, end {end}")

    #squares we have checked
    visited = []

    #creates an intial list of just the starting box
    unvisited = [start]

    #repeats until program ends by user termination or when end is found
    while len(unvisited) > 0:
        current = unvisited.pop()
        
        print(f"current: {current}")
        currentBoxObj = listOfBoxObj[listOfBoxCoords.index(current)]

        #skips block if its visited
        if current in visited:
            continue
        
        #if it reaches the end, it stops the loop
        if current == end:
            currentBoxObj.color = (155,0,155)
            print(f"found {current}")
            pygame.time.delay(5000)
            pygame.quit()
            #while True:
            #    for event in pygame.event.get():
            #        if event.type == pygame.QUIT:
            #            pygame.quit()

        #add current to visited
        visited.append(current)

        #color current box green if its not the start or end
        if current != start and current != end:
            currentBoxObj.color = (0,190,0)
        currentBoxObj.update_box()
        pygame.display.update()

        #neighbor functions
        neighbors = find_neighbors(current)
        print(f"neighbors {neighbors}")

        if len(neighbors) > 0:
            for neighbor in neighbors:        
                if neighbor not in visited and neighbor not in listOfBlockCoords:
                    if neighbors.index(neighbor) == 0:
                        #if neighbor is the end box
                        if neighbor == end:
                            endBox = listOfBoxObj[listOfBoxCoords.index(end)]
                            endBox.color = (155,0,155)
                            endBox.update_box()
                            pygame.display.update()
                            print("found!")
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                        change_neighbors(neighbor, current)
                    unvisited.append(neighbor)
                    pygame.time.delay(1)
            
        #else:
        #    print(f"no path from {start} to {end}")
        #    pygame.time.delay(1000)
        #    pygame.quit()
    print(f"no path from {start} to {end}")
    pygame.time.delay(5000)
    pygame.quit()
#depth_search()
    

def breadth_first():
    #start is first square. end is goal. checks to make sure they are not border blocks
    start,end = get_click()
    if start in listOfBlockCoords:
        print(f"invalid start: {start}")
        pygame.time.delay(1000)
        pygame.quit()
        return -1

    #checks if valid end
    if end in listOfBlockCoords:
        print(f"invalid end {end}")
        pygame.time.delay(1000)
        pygame.quit()
        return -1

    print(f"start {start}, end {end}")


    current = start
    
    checked = [current]
    edgeBoxes = [current]    

    while end not in checked:
        if -1 in edgeBoxes:
            edgeBoxes = edgeBoxes[edgeBoxes.index(-1)::]
        for neighbor in edgeBoxes:
            for n in find_neighbors(neighbor):
                change_neighbors(neighbor = neighbor, current = current)
                edgeBoxes.append(neighbor)
        checked.append(edgeBoxes)
        edgeBoxes.append(-1)

        pygame.display.update()


    pygame.time.delay(7000)
    pygame.quit()


breadth_first()

pygame.quit()
    
