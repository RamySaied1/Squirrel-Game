from typing import TypeVar, Generic, List, Tuple, Optional, MutableMapping, Type, Any
from problem import Problem,State,Action
from vector import Vector
from map2d import Map2D

Directions = {
    "UP": Vector(0, -1),
    "DOWN": Vector(0, 1),
    "LEFT": Vector(-1, 0),
    "RIGHT": Vector(1, 0),
    "TAKE":Vector(0,0),
    "HIDE":Vector(0,0)
}

GROUND_SYMBOL = "."
WALL_SYMBOL = "#"
STASH_SYMBOL = "X"
AGENT_SYMBOL = "@"
NUT_SYMBOL = "N"


class Squirrel(Problem['Squirrel.State', str]):
    # Define a state of the Maze problem. This class is immutable and hashable so that it can be used by the search function
    class State:
        __slots__ = ("problem", "NutsPositions", "nutsWith",
                     "pos", "stashPositions", "pathCost", "heuristic")
        problem: 'Squirrel'
        NutsPositions: List
        nutsWith: int
        pos : Vector
        stashPositions : List
        pathCost: int 
        heuristic: int 



        def __init__(self, problem: 'Squirrel', NutsPositions: List, nutsWith: int, pos: Vector, stashPositions: List,pathCost :int =0,heuristic:int =-1):
            super().__setattr__("problem", problem)
            super().__setattr__("NutsPositions", NutsPositions)
            super().__setattr__("nutsWith", nutsWith)
            super().__setattr__("pos", pos)
            super().__setattr__("stashPositions", stashPositions)
            super().__setattr__("pathCost", pathCost)
            super().__setattr__("heuristic", heuristic)



        def __setattr__(self, name, value):
            raise NotImplementedError

        def __hash__(self):

            return hash(      (self.pos,tuple(self. NutsPositions),tuple(self.stashPositions))     )

        def __lt__(self, value: 'Squirrel.State') -> bool:
            return (self.pathCost+self.heuristic < value.pathCost+value.heuristic)

        def __eq__(self, value: 'Squirrel.State') -> bool:
            return (self.pos) == value.pos and (self.NutsPositions == value.NutsPositions) and (self.stashPositions == value.stashPositions)

        def __str__(self) -> str:
            return '\n'.join(''.join(AGENT_SYMBOL if self.pos == (x, y) else cell for x, cell in enumerate(row)) for y, row in enumerate(self.problem.grid))

        def setHeuristic(self):
            if (self.heuristic ==-1):
                super().__setattr__("heuristic", self.problem.heuristic(self))



        def setPathCost(self,parentCost,actionCost):
            super().__setattr__("pathCost", parentCost+actionCost)
        def getPathCost(self):
            return self.pathCost

    
    @classmethod
    def read_from_file(cls, file_path: str) -> 'Maze':
        with open(file_path, 'r') as f:
            grid = [[cell for cell in line.strip()] for line in f.readlines()]
            
            height = len(grid)
            assert height > 0, "Map height must be greater than zero"
            width = max(len(row) for row in grid)
            assert width > 0, "Map width must be greater than zero"

            agentPosition = [Vector(x,y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == AGENT_SYMBOL]
            stashPositions = [Vector(x, y) for y, row in enumerate(
                grid) for x, cell in enumerate(row) if cell == STASH_SYMBOL]
            NutsPositions = [Vector(x, y) for y, row in enumerate(
                grid) for x, cell in enumerate(row) if cell == NUT_SYMBOL]

            assert len(agentPosition) == 1, "There must be one agent in the maze"
            agentPosition = agentPosition[0]
            
            grid[agentPosition[1]][agentPosition[0]] = GROUND_SYMBOL
            for row in grid:
                row.extend([WALL_SYMBOL]*(width - len(row)))
            return Squirrel(Map2D(grid), agentPosition, NutsPositions, 0, stashPositions)

    def __init__(self, grid: Map2D,  agentPosition, NutsPositions, nutsWith, stashPositions):
        super().__init__()
        self.grid = grid
        self.initial_pos = (NutsPositions, nutsWith,
                            agentPosition, stashPositions)
    # Returns the initial state
    @property
    def initial_state(self) -> State:
        return Squirrel.State(self, *self.initial_pos)

    # Returns a list of possible actions from the given state
    def get_actions(self, state: State) -> List[Action]:
        actions=[name for name, direction in Directions.items() if self.grid.inside(state.pos+direction) and self.grid[state.pos+direction] != WALL_SYMBOL]
        if ((state.pos  not in state.stashPositions) or state.nutsWith<=0):
            actions.remove("HIDE")
        if (state.pos  not in state.NutsPositions):
            actions.remove("TAKE")

        return actions

    # Given a state and a valid action, return the next state and the action cost
    def get_successor(self, state: State, action: Action) -> Tuple[State, float]:
        if (action in ["UP","RIGHT","LEFT","DOWN"]):
            return Squirrel.State(self, state.NutsPositions, state.nutsWith, state.pos+Directions[action], state.stashPositions), 1+((state.nutsWith*(state.nutsWith+1))/2)
        elif(action =="TAKE"):
            NutsPositionsNew=list(state.NutsPositions)
            NutsPositionsNew.remove(state.pos)
            return Squirrel.State(self, NutsPositionsNew, state.nutsWith+1, state.pos+Directions[action],state.stashPositions) ,1
        else:
            stashPositionsNew = list(state.stashPositions)
            stashPositionsNew.remove(state.pos)
            
            return Squirrel.State(self, state.NutsPositions, state.nutsWith-1, state.pos+Directions[action], stashPositionsNew) ,1


    # Checks if the given state is a goal
    def is_goal(self, state: State) -> bool:
        return (state.nutsWith==0) and (len(state.NutsPositions)==0)
    
    # Calculate the heuristic of the given state
    def heuristic(self, state: State) -> float:
        # heuristic 1
        #return state.nutsWith+0*len(state.stashPositions)

        # heuristic 2
        maxNutDistance = minStashDistance=0
        maxNut=state.pos
        minStash=state.pos
        if (len(state.NutsPositions)>0):
            maxNutDistance=state.NutsPositions[0].distance(state.pos)
            maxNut = state.NutsPositions[0]
            for nut in state.NutsPositions:
                if state.pos.distance(nut) > maxNutDistance:
                    maxNutDistance = state.pos.distance(nut)
                    maxNut=nut
        

        if (len(state.stashPositions) > 0):
            minStashDistance = state.stashPositions[0].distance(maxNut)
            minStash = state.stashPositions[0]
            for stash in state.stashPositions:
                if maxNut.distance(stash) < minStashDistance:
                    minStashDistance = maxNut.distance(stash)
                    minStash=stash
        
        average = (minStash+maxNut)
        average = Vector(average.x/2,average.y/2)

        distance = average.distance(state.pos)

        return distance+len(state.stashPositions)+len(state.NutsPositions)






            

    
