import sys
import bisect
from typing import TextIO, Dict, List, Set
from string import ascii_lowercase 

class PriorityQueue():
    def __init__(self):
        # keep both of these same size, keep indexs in line
        self.cost_list: List[int] = []
        self.word_list: List[str] = []

    def isEmpty(self) -> bool:
        return len(self.cost_list) == 0

    def insert(self, word, cost):
        self.word_list.append(word)
        self.cost_list.append(cost)

    def pop(self) -> str:
        """
        return the 
        """
        min_val = 0
        for i in range(len(self.cost_list)):
            if self.cost_list[i] < self.cost_list[min_val]:
                min_val = i
        word = self.word_list[min_val]
        del self.word_list[min_val]
        del self.cost_list[min_val]        
        return word


       
def generate_neighbors(word_set: Set[str], word: str) -> List[str]:
    """
    word_set: Set of acceptable words, faster than list for use case
    word: the specified word we are building neighbors for

    return: A list of words that differ from the parameter 'word' by one letter
    """
    neighbors = []
    for i in range(0, len(word)):
        for letter in ascii_lowercase:
            if letter != word[i]:
                neighbor = word[:i] + letter + word[i+1:]
                if neighbor in word_set:
                    neighbors.append(neighbor)
    return neighbors                


def generate_graph(word_list: List[str]) -> Dict[str, List[str]]:
    """
    word_list: A list of accepted words in the file
    
    returns: A dictionary representing the graph. Keys are nodes, values are neighbors.
    """
    word_set = set(word_list)
    graph = {word: [] for word in word_set}

    for word in word_list:
        graph[word] = generate_neighbors(word_set, word)
    return graph    



def generate_heuristic(word_list: List[str], goal: str) -> Dict[str, int]:
    """
    word_list: A list of accepted words in the file
    goal: The goal state

    return: A dictionary, where the keys are accepted words, and the value is the number of letters that differ from the goal state
    """
    graph ={word: 0 for word in set(word_list)}
    for word in word_list:
        heuristic = 0 # lower is better
        for i in range(0, len(goal)):
            if (word[i] != goal[i]):
                heuristic += 1
        graph[word] = heuristic
    return graph            


def word_path(file: TextIO, initial: str, goal: str):
    """
    file: file object in read mode to build the graph from
    initial: the initial starting word, passed via cmd line
    goal: the goal state, passed via cmd line
    """
    if (len(initial) != len(goal)):
        print("Length of intial word and goal word are not the same, cannot find path.")
        sys.exit(1)
    target_length = len(initial)
    word_list = []

    for line in file:
        word = line.strip()
        if len(word) == target_length:
            word_list.append(word)

    words_heuristic = generate_heuristic(word_list, goal)
    words_graph = generate_graph(word_list)

    path = aStar(words_graph, words_heuristic, initial, goal)
    for word in path:
        print(word)

    # from this point we have our graph built, as well as our heuristic function. we just need to implement A* now
          
def aStar(graph: Dict[str, List[str]], heuristic: Dict[str, int], initial: str, goal: str) -> List[str]:
    """
    graph: A dictionary meant to represent a graph. Keys are the nodes value, values are the nodes neighbors
    heuristic: A dictionary attaching each word to the lower bound of reaching goal state. 
    initial: the initial state in our search
    goal: the goal state in our search

    return: the list of words to reach the goal state
    """
    frontier = PriorityQueue()
    frontier.insert(initial, 0) # initial has a cost of 0

    came_from: Dict[str, str] = dict()
    cost_so_far: Dict[str, int] = dict()

    came_from[initial] = None
    cost_so_far[initial] = 0

    while not frontier.isEmpty():
        current = frontier.pop()

        if current == goal:
            break

        for neighbor in graph[current]:
            new_cost = cost_so_far[current] + heuristic[neighbor]
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                frontier.insert(neighbor, new_cost)
                came_from[neighbor] = current

    path: List[str] = []
    current = goal
    # building the path based off of the came_from dict
    while current != initial:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            print(f"no solution")
            sys.exit(1)    
    path.append(initial)
    path.reverse()

    return path


def main():
    if (len(sys.argv) != 4):
        print(f"Error: Expected 3 arguements but received {len(sys.argv) - 1}.")
        sys.exit(1)
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                word_path(file, sys.argv[2], sys.argv[3])
        except FileNotFoundError:
            print(f"File with the name '{sys.argv[1]}' was not found.")
        except IOError:
            print("An Error occured while attempting to read the file")    


if __name__ == "__main__":
    main()