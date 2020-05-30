from solver2 import getMaze, getPath

import pygame

pygame.init()

screen = pygame.display.set_mode((530,530))

pygame.display.set_caption("Pacman")

icon = pygame.image.load('sprites/pacman.png')

pygame.display.set_icon(icon)

pacmanX = 53
pacmanY = 53
pacman = pygame.image.load('sprites/pacman.png')
wall = pygame.image.load('sprites/block.png')
openSpace = pygame.image.load('sprites/path.png')
reward = pygame.image.load('sprites/reward.png')
# ghost = pygame.image.load('sprites/ghost.png')
# pinkCell = pygame.image.load('sprites/pink_cell.png')

def createWall(x=0,y=0):
    screen.blit(wall, (x,y))

def createOpenSpace(x=53,y=53):
    screen.blit(openSpace, (x,y))

# def createGhost(x=0,y=0):
#     screen.blit(wall, (x,y))

# def createPinkCell(x=0,y=0):
#     screen.blit(openSpace, (x,y))

def player(x=53,y=53):
    screen.blit(pacman, (x, y))

maze = getMaze('Maze1.txt')
path = getPath()

mission_accomplished = False
showWindow = True
while showWindow:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showWindow = False

    screen.blit(reward, (371,318))

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '1':
                createWall(j*53, i*53)
            if maze[i][j] == '0':
                createOpenSpace(j*53, i*53)

    if not mission_accomplished:
        for i in range(1,len(path)):
            newX = (path[i][0])*53
            newY = (path[i][1])*53

            while not newX == pacmanX:
                if newX > pacmanX:
                        pacmanX += 1
                elif newX < pacmanX:
                    pacmanX -= 1
                player(pacmanY, pacmanX)
                pygame.display.update()
            while not newY == pacmanY:
                if newY > pacmanY:
                        pacmanY += 1
                elif newY < pacmanY:
                    pacmanY -= 1
                player(pacmanY, pacmanX)
                pygame.display.update()
                    
            createOpenSpace((path[i-1][1])*53, (path[i-1][0])*53)
            pygame.display.update()
    
    mission_accomplished = True