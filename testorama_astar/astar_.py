from heapq import heappush, heappop # for priority queue
import math
import time

#Class to represent a node
class node:
    xPos = 0 # x position
    yPos = 0 # y position
    cost = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate

    def __init__(self, xPos, yPos, cost, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.cost = cost
        self.priority = priority

    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        self.priority = self.cost + self.estimate(xDest, yDest) * 10 # A*

    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)
        return(d)

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
    closed_nodes_map = []  # map of closed (tried-out) nodes
    open_nodes_map = []  # map of open (not-yet-tried) nodes
    dir_map = []  # map of dirs
    row = [0] * n
    
    for i in range(m):  # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.cost, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the dirs
            path = ''
            while not (x == xA and y == yA):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x += dx[j]
                y += dy[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.cost, n0.priority)
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found


def main():
    dirs = 4  # number of possible directions to move on the map
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    y = 0
    x = 0
    xA = 0
    yA = 0
    xB = 0
    yB = 0

    array = []

    #Choose a board as input, from user input
    map = raw_input("Choose a map between 1-4: ")
    board = open(map+".txt", "r").readlines()

    for line in board:
        x = 0
        preArray = []
        for char in line:
            if char == '.':
                preArray.append(0)
            elif char == '#':
                preArray.append(1)
            elif char == 'A':
                xA = x
                yA = y
                preArray.append(0)
            elif char == 'B':
                xB = x
                yB = y
                preArray.append(0)
            x += 1
        y += 1
        array.append(preArray)


    n = x-1  # horizontal size of the map
    m = y  # vertical size of the map

    t = time.time()
    route = pathFind(array, n, m, dirs, dx, dy, xA, yA, xB, yB)

    # mark the route on the map
    if len(route) > 0:
        x = xA
        y = yA
        array[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            array[y][x] = 3
        array[y][x] = 4


    print '-----------------------------------------------------------'
    print 'Map:'
    print ' '
    for y in range(m):
        for x in range(n):
            xy = array[y][x]
            if xy == 0:
                print bcolors.OKBLUE + '.' + bcolors.ENDC,  # space
            elif xy == 1:
                print bcolors.FAIL + '#' + bcolors.ENDC,  # obstacle
            elif xy == 2:
                print bcolors.WARNING + 'A' + bcolors.ENDC,  # start
            elif xy == 3:
                print bcolors.OKGREEN + 'O' + bcolors.ENDC,  # route
            elif xy == 4:
                print bcolors.WARNING + 'B' + bcolors.ENDC,  # finish
        print

# Class holding colors used in console printing


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
        

main()