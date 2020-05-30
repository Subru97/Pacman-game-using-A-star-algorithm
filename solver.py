from math import sqrt, pow

with open('Maze2.txt', 'r') as f:
    data = f.read().splitlines()

locator = {}
maze = []
door_key = {'b':'a', 'd':'c', 'g':'f', 'h':'i'}
maze_dim = [len(data), 0]
for i in range(maze_dim[0]):
    line = data[i].split()
    maze.append(line)
    maze_dim[1] = len(line)
    for j in range(maze_dim[1]):
        if line[j].isalpha():
            locator[line[j]] = [i, j]

class analyseMaze():
    def __init__(self, node, end=locator['e']):
        self.node = node
        self.start = start
        self.end = end

    def calculateHeuristics(self):
        return sqrt(pow((self.end[0]-self.node[0]), 2) + pow((self.end[1]-self.node[1]), 2)) 

    def neighbourAnalyser(self):
        neighbours = []
        current_door = []
        reRoute = False
        if not self.node[0]-1 < 0:
            if maze[self.node[0]-1][self.node[1]] == '0' or \
            maze[self.node[0]-1][self.node[1]] == 'e':
                neighbours.append([self.node[0]-1, self.node[1], self.node[2]+1])
            elif maze[self.node[0]-1][self.node[1]] in door_key.keys():
                reRoute = True
                current_door = maze[self.node[0]-1][self.node[1]]
                return [reRoute, current_door]
        if not self.node[0]+1 > maze_dim[0]:
            if maze[self.node[0]+1][self.node[1]] == '0' or \
            maze[self.node[0]+1][self.node[1]] in locator.keys():
                neighbours.append([self.node[0]+1, self.node[1], self.node[2]+1])
        if not self.node[1]-1 < 0:
            if maze[self.node[0]][self.node[1]-1] == '0' or \
            maze[self.node[0]][self.node[1]-1] in locator.keys():
                neighbours.append([self.node[0], self.node[1]-1, self.node[2]+1])
        if not self.node[1]+1 > maze_dim[1]:
            if maze[self.node[0]][self.node[1]+1] == '0' or \
            maze[self.node[0]][self.node[1]+1] in locator.keys():
                neighbours.append([self.node[0], self.node[1]+1, self.node[2]+1])
        return [reRoute, neighbours]

start = locator['s'].copy()
start.append(0)
obj = analyseMaze(start)
unvisitedNodes = [[obj, 0, [locator['s'].copy()]]]
visitedNodes = []
nodeHistory = []
nodeHistory.append(start[:2])
pathFound = False
i = 0
while not pathFound:
    f = []
    newNodes = []
    for node in unvisitedNodes:
        f.append([node, node[1] + node[0].calculateHeuristics()])
        if node[0].calculateHeuristics() == 0:
            print(node[2])
            break
    f.sort(key=lambda x: x[1])
    neighbours = f[0][0][0].neighbourAnalyser()
    parent = f[0][0][2].copy()    

    selected_node = unvisitedNodes.index(f[0][0])
    visitedNodes.append(unvisitedNodes[selected_node])
    del unvisitedNodes[selected_node]
    for n in neighbours:
        cObj = analyseMaze(n)
        parent = f[0][0][2].copy() 
        child = []
        child.extend(parent)
        child.append(n[:2])
        if not n[:2] in nodeHistory: 
            nodeHistory.append(n[:2])
            newNodes.append([cObj, n[2], child])
    unvisitedNodes.extend(newNodes)

    # i += 1
    # if i > 36:
    #     break
    if not len(unvisitedNodes):
        break
