# The implementation of 8 puzzle game by A star algorithm.
import heapq as hq

# debug_count = 0
class StateMatrix:
    def __init__(self, state: list[list[int]], empty_cell: tuple = (0, 0), fun_value=float("inf"), g_value=0, parent=None, repeated=False):
        self.state = state
        self.blank_position = empty_cell

        self.g_value = g_value
        self.parent = parent
        self.functional_value = fun_value

        self.repeated = repeated

        self.neighbours = []

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
        return StateMatrix(new_state, empty_cell=(row, column), parent=self, g_value=g_value)

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

final = [[2, 0, 8],
         [1, 6, 3],
         [7, 5, 4]]


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

if __name__ == '__main__':
    goal = a_star_algorithm()
    if goal:
        goal.display(depth = 20)
