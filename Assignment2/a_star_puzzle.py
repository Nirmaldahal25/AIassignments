# The implementation of 8 puzzle game by A star algorithm.
import heapq as hq
import graphviz
#LDUR 

# debug_count = 0
class StateMatrix:
    def __init__(self, state: list[list[int]],move=(0,0), empty_cell: tuple = (0, 0), fun_value=float("inf"), g_value=0, parent=None, repeated=False):
        self.state = state
        self.blank_position = empty_cell

        self.g_value = g_value
        self.parent = parent
        self.functional_value = fun_value
        self.move = move
        self.repeated = repeated

        self.neighbours = []
        
        #for graphviz
        self.node_representation = None

    def node_name(self, generator = None)->str:
        if not self.node_representation and generator: 
            self.node_representation = f"node{next(generator)}"
        return self.node_representation

    def edge(self)->str:
        return f"f={self.functional_value},g={self.g_value},h={self.functional_value - self.g_value}"

    def state_representation(self)->str:
            return graphviz.nohtml("{{"
                                   "{{{0}|<f1>{1}|{2}}}|"
                                   "{{{3}|{4}|{5}}}|"
                                   "{{{6}|<f2>{7}|{8}}}"
                                   "}}".format(*[x for y in self.state for x in y]))
    
    def display(self, depth=20):
        for substate in self.state:
            print(substate)
        print("---------")
        if self.parent and depth > 0:
            new_depth = depth - 1
            self.parent.display(new_depth)

    @staticmethod
    def is_state_ok(state: object) -> bool:
        if not isinstance(state, StateMatrix):
            return False

        if len(state.state) != 3:
            return False

        for substate in state.state:
            if len(substate) != 3:
                return False

        return True

    """Move values can only be -1<=x<=1 and -1<=y<=1 and x*x != y*y"""
    @staticmethod
    def is_legal_move(move: tuple[int], blank_position: tuple[int]) -> bool:
        if move == (0, 0):
            return False
        elif move[0] * move[0] == move[1] * move[1]:
            return False
        elif move[0] * move[0] > 1 or move[1] * move[1] > 1:
            return False

        pos_x = move[0] + blank_position[0]
        pos_y = move[1] + blank_position[1]
        if (pos_x < 0 or pos_x > 2) or (pos_y < 0 or pos_y > 2):
            return False
        return True

    def misplaced_tiles(self, goal_state) -> int | None:
        count = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != goal_state.state[i][j]:
                    count += 1
        return count

    def __eq__(self, __value: object) -> bool:
        if not StateMatrix.is_state_ok(__value):
            return False

        for i in range(3):
            for j in range(3):
                if self.state[i][j] != __value.state[i][j]:
                    return False
        return True

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def get_next_state(self, move: tuple[int]):
        new_state = [state[:] for state in self.state]
        row = self.blank_position[0] + move[0]
        column = self.blank_position[1] + move[1]

        old_row, old_column = self.blank_position
        new_state[row][column], new_state[old_row][old_column] = new_state[old_row][old_column], new_state[row][column]

        # global debug_count
        # if debug_count < 1:
        #     print(self.state, new_state, (row, column), (old_row, old_column), move)
        #     debug_count += 1

        g_value = self.g_value + 1
        return StateMatrix(new_state, empty_cell=(row, column), parent=self, g_value=g_value, move=move)

    def get_neighbours(self):
        if len(self.neighbours) == 0:
            # find all the neighbours or child states
            for i in range(-1,2):
                for j in range(-1,2):
                    move = (i, j)
                    if StateMatrix.is_legal_move(move, self.blank_position):
                        next_state = self.get_next_state(move)
                        self.neighbours.append(next_state)
        return self.neighbours


    def __lte__(self, __value):
        if not isinstance(__value, StateMatrix):
            return False
        return self.functional_value <= __value.functional_value
    
    def __lt__(self, __value):
        if not isinstance(__value, StateMatrix):
            return False
        return self.functional_value < __value.functional_value
    
    def __gt__(self, __value):
        if not isinstance(__value, StateMatrix):
            return False
        return self.functional_value > __value.functional_value
    
    def __gte__(self, __value):
        if not isinstance(__value, StateMatrix):
            return False
        return self.functional_value >= __value.functional_value
    
# initial state
initial = [[2, 8, 3],
           [1, 6, 4],
           [7, 0, 5]]

final = [[1, 2, 3],
         [8, 0, 4],
         [7, 6, 5]]


def a_star_algorithm()->StateMatrix:
    initial_state = StateMatrix(
        initial, empty_cell=(2, 1), g_value=0)
    goal_state = StateMatrix(final, empty_cell=(0, 1))
    initial_state.functional_value = initial_state.g_value + \
        initial_state.misplaced_tiles(goal_state=goal_state)
    
    open_list: list[StateMatrix] = list()
    open_list.append(initial_state)

    closed_list: list[StateMatrix] = list()
    while len(open_list) != 0:
        hq.heapify(open_list)
        state: StateMatrix = hq.heappop(open_list)
        if(state == goal_state):
            return state
        closed_list.append(state)
        neighbours: list[StateMatrix] = state.get_neighbours()

        for neighbour in neighbours:
            #calculate functional value of neighbour
            neighbour.functional_value = neighbour.g_value + neighbour.misplaced_tiles(goal_state)

            if neighbour in closed_list:
                index = closed_list.index(neighbour)
                if closed_list[index].g_value > neighbour.g_value:
                    closed_list[index].repeated = True
                    closed_list[index] = neighbour
                else:
                    neighbour.repeated = True
                
            elif neighbour in open_list:
                index = open_list.index(neighbour)
                if open_list[index].g_value > neighbour.g_value:
                    open_list[index].repeated = True #open_list[index](a shallow copy of other child) object has repeated set to True
                    open_list[index] = neighbour #open_list[index] object has repeated set to False
                else:
                    neighbour.repeated = True
            else:
                if not neighbour.repeated: #if same state repeats again with higer g_score, ignore
                    open_list.append(neighbour)

    return None


class Generator:
    def __init__(self, value = 0):
        self.value = value

    def __iter__(self):
        return self
    
    def __next__(self):
        self.value += 1
        return self.value

def initTree(state: StateMatrix, graph, generator):
    COLORS = ("green", "red", "blue")
    index = 0
    if state.repeated:
        index = 2
    graph.node(state.node_name(generator), state.state_representation(), color=COLORS[index])
    for child in state.neighbours:
        initTree(child, graph, generator)

def drawTree(state: StateMatrix, graph):
    if len(state.neighbours) > 0:
        for child in state.neighbours:
            graph.edge(f"{state.node_name()}:f2", f"{child.node_name()}:f1", label = child.edge(), len="1.00")
            drawTree(child, graph)

def state_space_tree(start_state: StateMatrix):
    generator = Generator()
    g = graphviz.Digraph('g', filename='btree.dot',
                     node_attr={'shape': 'record', 'height': '.4'})
    initTree(start_state, g, iter(generator))
    drawTree(start_state, g)
    g.save()

if __name__ == '__main__':
    goal = a_star_algorithm()
    if goal:
        goal.display(depth = 20)

        parent = goal
        while True:
            if not parent.parent:
                break
            parent = parent.parent

        state_space_tree(parent)