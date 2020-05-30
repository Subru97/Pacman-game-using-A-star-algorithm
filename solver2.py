from math import sqrt, pow

class analyseMaze():
        def __init__(self, node, end):
            self.node = node
            self.end = end

        def calculateHeuristics(self):
            return sqrt(pow((self.end[0]-self.node[0]), 2) + pow((self.end[1]-self.node[1]), 2)) 

        def neighbourAnalyser(self):
            neighbours = []
            if not self.node[0]-1 < 0:
                if maze[self.node[0]-1][self.node[1]] == '0' or \
                maze[self.node[0]-1][self.node[1]] in locator.keys():
                    neighbours.append([self.node[0]-1, self.node[1], self.node[2]+1])
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
            return neighbours


def pathFinder(start, end):
        obj = analyseMaze(start, end)
        unvisitedNodes = [[obj, 0, [start[:2].copy()]]]
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
                    # print(node[2])
                    return node
            f.sort(key=lambda x: x[1])
            neighbours = f[0][0][0].neighbourAnalyser()
            parent = f[0][0][2].copy()    

            selected_node = unvisitedNodes.index(f[0][0])
            visitedNodes.append(unvisitedNodes[selected_node])
            del unvisitedNodes[selected_node]
            for n in neighbours:
                cObj = analyseMaze(n, end)
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
            

def getPath():
    start_point = locator['s'].copy()
    start_point.append(0)
    end_point = locator['e'].copy()

    check_points = [locator['s'].copy(), locator['e'].copy()]
    path_recorder = []

    i = 0
    while True:
        start_point = check_points[i].copy()
        start_point.append(0)
        end_point = check_points[i+1].copy()
        # print(start_point, end_point, check_points, i)
        new_point = False
        path = pathFinder(start_point, end_point)
        path_recorder.append(path)
        for p in path[2]:
            if maze[p[0]][p[1]] in door_key.keys() and not locator[door_key[maze[p[0]][p[1]]]] in check_points:
                new_point = True
                check_points.insert(check_points.index(end_point[:2]), locator[door_key[maze[p[0]][p[1]]]])
        if new_point:
            i = 0
            path_recorder = []
        elif i+2 < len(check_points):
            i += 1
            if not path in path_recorder:
                path_recorder.append(path.copy())
            # print('-------------', path_recorder, start_point)
        else:
            if not path in path_recorder:
                path_recorder.append(path.copy())
            # print('-------------', path_recorder, start_point)
            break

    final = []

    for i in range(1, len(path_recorder)):
        del path_recorder[i][2][0]

    for path in path_recorder:
        final.extend(path[2])

    return final

def getMaze(filename='Maze1.txt'):
    with open(filename, 'r') as f:
        data = f.read().splitlines()

    global locator
    locator = {}
    global ghost_locator
    ghost_locator = []
    global door_key
    door_key = {'b':'a', 'd':'c', 'g':'f', 'h':'i'}
    global maze
    maze = []
    global maze_dim
    maze_dim = [len(data), 0]
    for i in range(maze_dim[0]):
        line = data[i].split()
        maze.append(line)
        maze_dim[1] = len(line)
        for j in range(maze_dim[1]):
            if line[j].isalpha():
                locator[line[j]] = [i, j]
            if line[j].isnumeric() and int(line[j]) > 1:
                ghost_locator.append([i, j, int(line[j])])

    for ghost in ghost_locator:
        for i in range(1,ghost[2]):
            if ghost[1]+i < maze_dim[1] and maze[ghost[0]][ghost[1]+i] == '0':
                maze[ghost[0]][ghost[1]+i] = '-1'
            elif ghost[1]+i < maze_dim[1] and maze[ghost[0]][ghost[1]+i] == '1':
                break
        for i in range(1,ghost[2]):
            if ghost[1]-i >= 0 and maze[ghost[0]][ghost[1]-i] == '0':
                maze[ghost[0]][ghost[1]-i] = '-1'
            elif ghost[1]-i >= 0 and maze[ghost[0]][ghost[1]-i] == '1':
                break
        for i in range(1,ghost[2]):
            if ghost[0]+i < maze_dim[0] and maze[ghost[0]+i][ghost[1]] == '0':
                maze[ghost[0]+i][ghost[1]] = '-1'
            elif ghost[0]+i < maze_dim[0] and maze[ghost[0]+i][ghost[1]] == '1':
                break
        for i in range(1,ghost[2]):
            if ghost[0]-i >= 0 and maze[ghost[0]-i][ghost[1]] == '0':
                maze[ghost[0]-i][ghost[1]] = '-1'
            elif ghost[0]-i >= 0 and maze[ghost[0]-i][ghost[1]] == '1':
                break

        for i in range(1,ghost[2]):
            if ghost[0]+i < maze_dim[0] and ghost[1]+i < maze_dim[1] and (maze[ghost[0]+i][ghost[1]+i] == '1' or maze[ghost[0]][ghost[1]+i] == '1' or maze[ghost[0]+i][ghost[1]] == '1'):
                break
            elif ghost[0]+i < maze_dim[0] and ghost[1]+i < maze_dim[1] and maze[ghost[0]+i][ghost[1]+i] == '0':
                maze[ghost[0]+i][ghost[1]+i] = '-1'
        for i in range(1,ghost[2]):
            if ghost[0]-i >= 0 and ghost[1]-i >= 0 and (maze[ghost[0]-i][ghost[1]-i] == '1' or maze[ghost[0]][ghost[1]-i] == '1' or maze[ghost[0]-i][ghost[1]] == '1'):
                break
            elif ghost[0]-i >= 0 and ghost[1]-i >= 0 and maze[ghost[0]-i][ghost[1]-i] == '0':
                maze[ghost[0]-i][ghost[1]-i] = '-1'
        for i in range(1,ghost[2]):
            if ghost[0]-i >= 0 and ghost[1]+i < maze_dim[1] and (maze[ghost[0]-i][ghost[1]+i] == '1' or maze[ghost[0]][ghost[1]+i] == '1' or maze[ghost[0]-i][ghost[1]] == '1'):
                break
            elif ghost[0]-i >= 0 and ghost[1]+i < maze_dim[1] and maze[ghost[0]-i][ghost[1]+i] == '0':
                maze[ghost[0]-i][ghost[1]+i] = '-1'
        for i in range(1,ghost[2]):
            if ghost[0]+i < maze_dim[0] and ghost[1]-i >= 0 and (maze[ghost[0]+i][ghost[1]-i] == '1' or maze[ghost[0]][ghost[1]-i] == '1' or maze[ghost[0]+i][ghost[1]] == '1'):
                break
            elif ghost[0]+i < maze_dim[0] and ghost[1]-i >= 0 and maze[ghost[0]+i][ghost[1]-i] == '0':
                maze[ghost[0]+i][ghost[1]-i] = '-1'

    return maze

if __name__ == '__main__':
    getMaze()
    getPath()