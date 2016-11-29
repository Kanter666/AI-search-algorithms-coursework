from pandas import *        #library for simple printing of world(matrix)
from queue import PriorityQueue
import copy
import queue
import random
from random import randint
import os                   #library for cleaning screen

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, priority, item):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

#class that models word
class World:
    'Model of world for block puzzle'

    def __init__(self, height, width, boxes, position):
        self.space = [['-' for x in range(width)] for y in range(height)]
        self.boxes=0
        for xy in boxes:
            self.boxes += 1
            self.space[xy[0]][xy[1]]=self.boxes
        self.final = []
        for i in range(self.boxes):
            self.final.append([height-1-i,1,self.boxes-i])
        self.space[position[0]][position[1]]='A'
        self.position = position
        self.height = height
        self.width=width
        self.depth=-1
        self.route=[]
        self.routeDir=[]
        self.addState()

    #function for printing current state of world
    def print(self):
        print (pandas.DataFrame(self.space))

    def getPosition(self):
        return self.position

    def getHeight(self):
        return self.height

    #depth getter
    def getDepth(self):
        return self.depth

    def getRouteDir(self):
        return self.routeDir

    def canMove(self, direction, position):
        if (direction == 'u'):
            if (position[0] > (0)):
                return True
        elif (direction == 'd'):
            if (position[0] < (self.height - 1)):
                return True
        elif (direction == 'r'):
            if (position[1] < (self.width - 1)):
                return True
        elif (direction == 'l'):
            if (position[1] > (0)):
                return True
        return False


    #function for moving the agent
    #parameters: direction, postion - from where are we moving, character - if we are moving with agent or no
    #directions: u-up, d-down, r-right, l-left
    def move(self, direction, position, character):
        if(direction=='u'):
                self.space[position[0]][position[1]] = '-'
                position[0]-=1
                if (self.space[position[0]][position[1]] != '-'):
                    self.space[position[0]+1][position[1]] = self.space[position[0]][position[1]]
        elif(direction=='d'):
                self.space[position[0]][position[1]] = '-'
                position[0] += 1
                if (self.space[position[0]][position[1]] != '-'):
                    self.space[position[0]-1][position[1]] = self.space[position[0]][position[1]]
        elif (direction == 'r'):
                self.space[position[0]][position[1]] = '-'
                position[1] += 1
                if (self.space[position[0]][position[1]] != '-'):
                    self.space[position[0]][position[1] - 1] = self.space[position[0]][position[1]]
        elif(direction=='l'):
                self.space[position[0]][position[1]] = '-'
                position[1] -= 1
                if(self.space[position[0]][position[1]] != '-' ):
                    self.space[position[0]][position[1]+1]=self.space[position[0]][position[1]]
        self.routeDir.append(direction)
        self.space[position[0]][position[1]] = character
        self.position=position
        self.addState()
        return self


    def isFinal(self):
        for xy in self.final:
            if(self.space[xy[0]][xy[1]]!=xy[2]):
                return False
        print("you won")
        return True

    # function for saving previous states - not just as references of objects but as new objects
    def addState(self):
        self.depth += 1
        newList = []
        for x in self.space:
            newList.append(list(x))
        self.route.append(list(newList))

    def printRoute(self):
        node=0
        for state in self.route:
            print('State of world in depth: ',node)
            node+=1
            print(pandas.DataFrame(state))

    def estimateFunction(self):
        distance = self.depth
        nearby=False
        for i in ['u', 'd', 'l', 'r']:
            if (self.canMove(i, self.position)):
                if (i == 'u'):
                    if(self.space[self.position[0]-1][self.position[1]] != '-'):
                        nearby=True
                elif (i == 'd'):
                    if (self.space[self.position[0] + 1][self.position[1]] != '-'):
                        nearby = True
                elif (i == 'r'):
                    if (self.space[self.position[0]][self.position[1]+1] != '-'):
                        nearby = True
                elif (i == 'l'):
                    if (self.space[self.position[0]][self.position[1 - 1]] != '-'):
                        nearby = True
        if(not(nearby)):
            distance+=2
        for box in range(1,self.boxes+1):
            position = []
            q = queue.Queue()
            counter=-1
            for i in self.space:
                counter += 1
                try:
                    position=[counter, i.index(box)]
                except ValueError:
                    continue
            q.put([self, 0, position])
            notInPlace=True
            while notInPlace:
                world = q.get()
                world.append(world[0].getPosition())
                if((world[0].space[box][1])==box):
                    distance+=world[1]
                    notInPlace=False
                world[1]+=1
                for i in ['u', 'd', 'l', 'r']:
                    if (world[0].canMove(i,world[2])):
                        q.put([copy.deepcopy(world[0]).move(i, copy.deepcopy(world[2]), box), copy.deepcopy(world[1])])
        return distance

def textMenu():
    def validInput(characters):
        while True:
            string = input('Write your choice :/n')
            if (string in characters):
                return string
            else:
                print('You wrote "',string,'", that is not valid choice, choose from: ',characters)
    def chooseWorld():
        print('Choose difficulty(world) from: ')
        print('                                 1 - first difficulty')
        world = World(2,3,[[0,0]],[0, 1])
        world.print()
        print('                                 2 - second difficulty')
        world = World(3, 3, [[0, 0], [2, 0]], [0, 2])
        world.print()
        print('                                 3 - third difficulty')
        world = World(3, 3, [[0, 2], [2, 0]], [1, 2])
        world.print()
        print('                                4 - fourth difficulty')
        world = World(4, 4, [[3, 0], [3, 1], [3, 2]], [3, 3])
        world.print()
        print('')
        choice=validInput(['1','2','3','4'])
        if (choice == "1"):
            return World(2, 3, [[0, 0]], [0, 1])
        elif (choice == "2"):
            return World(3, 3, [[0, 0], [2, 0]], [0, 2])
        elif (choice == "3"):
            return World(3, 3, [[0, 0], [0, 2]], [2, 2])
        elif (choice == "4"):
            return World(4, 4, [[3, 0], [3, 1], [3, 2]], [3, 3])

    def runAlgorithm(algorithm):
        print()
        print('----------------------------------------------------------------------------------------------------')
        print('-----------------------',algorithm,'-----------------------')
        print('----------------------------------------------------------------------------------------------------')
        world=chooseWorld()
        algorithm+="(world)"
        print(algorithm)
        exec(algorithm)
        print()
        input("Press Enter to continue...")
        return




    while(True):
        print('----------------------------------------------------------------------------------------------------')
        print('------------------------Program for implementing different types of searches------------------------')
        print('-------------------------------------------Adam Kantorik--------------------------------------------')
        print('-----------------------------------------ak2g15@soton.ac.uk-----------------------------------------')
        print('----------------------------------------------------------------------------------------------------')
        print('')
        print('Menu:')
        print('         1 - Bread first search')
        print('         2 - Depth first search')
        print('         3 - Iterative deepening search')
        print('         4 - A star search')
        print('         5 - "Evolutionary" search')
        print('         C - Clear screen')
        print('         Q - Quit program')

        choice=validInput(["1","2","3","4","5","c","C",'q',"Q"])

        if(choice =="1"):
            runAlgorithm("breadthFirstSearch")
        elif(choice =="2"):
            runAlgorithm("depthFirstSearch")
        elif(choice =="3"):
            runAlgorithm("iterativeDeepeningSearch")
        elif (choice =="4"):
            runAlgorithm("AstarSearch")
        elif (choice =="5"):
            print('----------------------------------------------------------------------------------------------------')
            print('"Evolutionary" search')
            print('----------------------------------------------------------------------------------------------------')
            world = chooseWorld()
        elif (choice == "c" or choice == "C"):
            print('You choosed Clear screen')
            os.system('cls' if os.name == 'nt' else 'clear')
        elif (choice == "q" or choice == "Q"):
            print('Finishing')
            return







def breadthFirstSearch(inWorld):
    d=0
    q = queue.Queue()
    q.put(inWorld)
    while True:
        d+=1
        directions = []
        world = q.get()
        print('Original world, number of nodes explored = ', d)
        world.print()
        for i in ['u','d','l','r']:
            if(world.canMove(i, world.position)):
                print(i)
                directions.append(copy.deepcopy(world).move(i, copy.deepcopy(world.getPosition()), 'A'))
        for i in directions:
            if(i.isFinal()):
                print('Finaaaaaaaaaaaaaaaaaal')
                print(i.printRoute())
                return i
            q.put(i)

def depthFirstSearch(inWorld):
    d=0
    q = []
    q.append(inWorld)
    while True:
        d+=1
        directions = []
        world = q.pop()
        print('Original world, number of nodes explored = ', d)
        world.print()
        for i in ['u','d','l','r']:
            if (world.canMove(i, world.position)):
                print(i)
                directions.append(copy.deepcopy(world).move(i, copy.deepcopy(world.getPosition()), 'A'))
        random.shuffle(directions)
        for i in directions:
            if(i.isFinal()):
                print('Finaaaaaaaaaaaaaaaaaal')
                i.printRoute()
                return i
            q.append(i)


def iterativeDeepeningSearch(inWorld):
    nodes = 0
    d = 0
    q = []
    q.append(inWorld)
    while True:
        nodes +=1
        directions = []
        if (len(q) < 1):
            d += 1
            q.append(inWorld)
        world = q.pop()
        print('Original world, number of nodes explored = ', nodes)
        world.print()
        for i in ['u', 'd', 'l', 'r']:
            if (world.canMove(i, world.position)):
                print(i)
                directions.append(copy.deepcopy(world).move(i, copy.deepcopy(world.getPosition()), 'A'))
        for i in directions:
            if (i.isFinal()):
                print('Finaaaaaaaaaaaaaaaaaal')
                i.printRoute()
                return i
            if (i.depth <= d):
                q.append(i)
            else:
                print('Got to depth ', d, ', ending this cycle')

def AstarSearch(inWorld):
    d = 0
    q = MyPriorityQueue()
    q.put(1, inWorld)
    while True:
        d += 1
        directions = []
        world = q.get()
        print('Original world, number of nodes explored = ', d)
        world.print()
        for i in ['u', 'd', 'l', 'r']:
            if (world.canMove(i, world.position)):
                print(i)
                directions.append(copy.deepcopy(world).move(i, copy.deepcopy(world.getPosition()), 'A'))
        for i in directions:
            if (i.isFinal()):
                print('Finaaaaaaaaaaaaaaaaaal')
                print(i.printRoute())
                return i
            function=i.estimateFunction()
            q.put(function, i)

#function for finding solution using evolutionary algorithm
#paramethers: nue -number of evolutions, sop - size of population, depthFac - depthFactor
def evolutionarySearch(inWorld, nue, sop, depthFac):

    def getParent(chance, popul):
        parent=0
        for p in range(len(popul)-1):
            if(randint(0,chance)==1):
                parent=popul[p][0].getRouteDir()
                break
        if(parent==0):
            parent=popul[len(popul)-1][0].getRouteDir()
        return parent

    def newIndividual():
        world = copy.deepcopy(inWorld)
        d = 0
        while (d < findingDepth):
            let = ['u', 'd', 'l', 'r']
            random.shuffle(let)
            for i in let:
                if (world.canMove(i, world.position)):
                    world.move(i, world.position, 'A')
                    break
            if (world.isFinal()):
                break
            d += 1
        return world

    def mixParents():
        world = copy.deepcopy(inWorld)
        d = 0
        kid = []
        parent1 = getParent(2, population)
        parent2 = getParent(2, population)
        for x in range(len(parent1)):
            if (randint(0, 1) == 1 or x >= len(parent2)):
                kid.append(parent1[x])
            else:
                kid.append(parent2[x])
            if (randint(0, 20) == 1):
                let = ['u', 'd', 'l', 'r']
                random.shuffle(let)
                kid[x] = let[0]

        while (d < findingDepth):
            if (d < (len(kid)) and world.canMove(kid[d], world.position)):
                world.move(kid[d], world.position, 'A')
            else:
                let = ['u', 'd', 'l', 'r']
                random.shuffle(let)
                for l in let:
                    if (world.canMove(l, world.position)):
                        world.move(l, world.position, 'A')
                        break
            if (world.isFinal()):
                break
            d += 1
        print('World number ', i, ' with fitness ', world.estimateFunction(), 'got this moves: ', world.getRouteDir())
        print('Parent 1: ', parent1)
        print('Parent 2: ', parent2)
        return world


    population = []
    findingDepth=inWorld.getHeight()*7*depthFac
    for i in range(sop):
        world=newIndividual()
        population.append((world,world.estimateFunction()))
    population.sort(key=lambda tup: tup[1]) #sorting of population by estimate function

    for i in population:
        print('World with route : ', i[0].getRouteDir(), ' with estimate of ', i[1], 'is: ')
        i[0].print()

    for j in range(nue):
        newPopulation = []
        for i in range(sop):
            print()
            if(randint(0, 2) == 1):
                world=newIndividual()
                print('World number ', i, ' with fitness ', world.estimateFunction(), 'got this moves: ', world.getRouteDir())
                print('No parents - new individual')
            else:
                world=mixParents()
            world.print()
            newPopulation.append((world, world.estimateFunction()))

        newPopulation.sort(key=lambda tup: tup[1])
        population=list(newPopulation)

    return


# world = World(2,3,[[0,0]],[0, 1])
# world = World(3,3,[[0,0],[2,0]],[0, 2])
# world = World(3,4,[[0,0],[2,0],[2,1]],[0, 2])
# world = World(4,4,[[3,0],[3,1],[3,2]],[3, 3])
# print(world.estimateFunction())
# breadthFirstSearch(world)
# evolutionarySearch(world, 30, 20, 6)
textMenu()





