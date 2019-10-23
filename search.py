from typing import TypeVar, List, Tuple, MutableSet, MutableMapping, Optional
from problem import Problem
from queue import PriorityQueue
from heapq import _siftup, _siftdown, heappop,heappush,heapify


State = TypeVar("State")
Action = TypeVar("Action")

# A Breadth First Search Implementation which takes a problem and optionally an initial state
# and returns a list of actions to reach the nearest goal or None if there is no solution
def bfs(problem: Problem[State, Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: List[State] = [initial_state]
    visited: MutableSet[State] = set()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    while len(frontier) > 0:
        current_state = frontier.pop(0)
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, _ = problem.get_successor(current_state, action)
            #print(action, predecessor)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                frontier.append(successor)
    return None



def aStar(problem: Problem[State, Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: List[State] = [initial_state]
    visited: MutableSet[State] = set()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    while len(frontier) > 0:
        current_state = heappop(frontier)
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, cost= problem.get_successor(current_state, action)
            #print(action, predecessor)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                successor.setPathCost(cost,current_state.getPathCost())
                successor.setHeuristic()
                heappush(frontier,successor)
            elif successor not in visited:
                i = frontier.index(successor)
                oldsucc=frontier[i]
                if (oldsucc.getPathCost()> cost+current_state.getPathCost()):
                    oldsucc.setPathCost(cost,current_state.getPathCost())
                    predecessor[oldsucc] = (current_state, action)
                    oldsucc.setHeuristic()
                    heapify(frontier)

    return None



def uniformCost(problem: Problem[State, Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: List[State] = [initial_state]
    visited: MutableSet[State] = set()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    while len(frontier) > 0:
        current_state = heappop(frontier)
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None: # reach the initial state
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited: # don't process the nodes twice
            continue
        visited.add(current_state) # mark it as visited
        for action in problem.get_actions(current_state): # get all possible actions that we can make from this state
            successor, cost= problem.get_successor(current_state, action)
            #print(action, predecessor)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                successor.setPathCost(cost,current_state.getPathCost())
                # successor.setHeuristic()
                heappush(frontier,successor)
            elif successor not in visited:
                i = frontier.index(successor)
                oldsucc=frontier[i]
                if (oldsucc.getPathCost()> cost+current_state.getPathCost()):
                    oldsucc.setPathCost(cost,current_state.getPathCost())
                    predecessor[oldsucc] = (current_state, action)
                    # oldsucc.setHeuristic()
                    heapify(frontier)

    return None


def greedyBestFirst(problem: Problem[State, Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: List[State] = [initial_state]
    visited: MutableSet[State] = set()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    while len(frontier) > 0:
        current_state = heappop(frontier)
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, cost= problem.get_successor(current_state, action)
            #print(action, predecessor)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                # successor.setPathCost(cost,current_state.getPathCost())
                successor.setHeuristic()
                heappush(frontier,successor)
            elif successor not in visited:
                i = frontier.index(successor)
                oldsucc=frontier[i]
                if (oldsucc.heuristic() > current_state.heuristic):
                    # oldsucc.setPathCost(cost,current_state.getPathCost())
                    predecessor[oldsucc] = (current_state, action)
                    oldsucc.setHeuristic()
                    heapify(frontier)

    return None