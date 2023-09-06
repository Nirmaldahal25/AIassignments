import graphviz
# missionary and cannibals
# [number_of_missionaries, number_of_cannibals, position_of_boat]
number_of_missionaries = 3
number_of_cannibals = 3
boat_capacity = 2
max_number = (number_of_missionaries, number_of_cannibals, boat_capacity)
# 0 means that boat is at initial shore and 1 means boat is at opposite shore
position_of_boat = 0
initial_state: tuple[int] = (
    number_of_missionaries,
    number_of_cannibals,
    position_of_boat,
)

class Generator:
    def __init__(self, value = 0):
        self.value = value

    def __iter__(self):
        return self
    
    def __next__(self):
        self.value += 1
        return self.value

class StateSpaceTree:
    def __init__(
        self,
        state: tuple[int] = (),
        boat: tuple[int] = (),
        further: bool = False,
        childs: list[object] = [],
        repeated: bool = False
    ):
        self.boat = boat
        self.state = state
        self.further = further
        self.childs = childs
        self.repeated = repeated
        #for graphviz
        self.node_representation = None

    def add_childs(self, childs: list[object]):
        self.childs += childs

    def set_repeated(self, repeat):
        self.repeated = repeat 

    def display(self, depth: int = 0):
        print("Boat:", self.boat, "\n", "State:", self.state, "\n")
        if depth > 0 and len(self.childs) > 0:
            print("Printing Childs.....\n")
            new_depth = depth - 1
            for child in self.childs:
                child.display(depth=new_depth)

    def state_representation(self)->str:
        return graphviz.nohtml(f"<f0> {self.state[0]}|<f1> {self.state[1]}|<f2> {self.state[2]} ")
    
    def node_name(self, generator = None)->str:
        if not self.node_representation and generator: 
            self.node_representation = f"node{next(generator)}"
        return self.node_representation
    
    def edge(self)->str:
        return f"{self.boat[0]},{self.boat[1]}"
    
"""
state = [number_of_missionaries_at_initial_shore,
    number_of_cannibals_at_initial_shore, position_of_boat]

"""


def next_state(state: tuple[int], boat: tuple[int], max_number: tuple[int]):
    cannibal = state[0]
    missionary = state[1]
    boat_position = state[2]
    further_child = True

    if boat_position == 1:  # boat is at opposite shore,
        cannibal = state[1] + boat[1]
        missionary = state[0] + boat[0]

    else:  # boat is at initial shore
        cannibal = state[1] - boat[1]
        missionary = state[0] - boat[0]

    # max m, n = 3,3
    # Case I: if 1,2 then killed
    # Case II: if 2,1 on the other side there will be 1,2 then killed
    # Case II: if 0,3 or m,<=m then safe
    if (cannibal > missionary and missionary != 0) or (
        missionary > cannibal and missionary != max_number[0]
    ):
        further_child = False

    return StateSpaceTree(
        (missionary, cannibal, 0 if boat_position ==
         1 else 1), boat, further_child, []
    )


def is_legal_move(
    state: tuple[int], boat_st: tuple[int], max_number: tuple[int]
) -> bool:
    no_of_missionaries: int = max_number[0]
    no_of_cannibals: int = max_number[1]
    boat_capacity: int =  max_number[2]

    if boat_st == (0,0):
        return False
    elif (boat_st[0] + boat_st[1]) > boat_capacity:
        return False
    elif state[2] == 0 and (boat_st[0] > state[0] or boat_st[1] > state[1]):
        return False
    elif state[2] == 1 and (
        boat_st[0] > (no_of_missionaries - state[0])
        or boat_st[1] > (no_of_cannibals - state[1])
    ):
        return False
    return True


def cannibals_and_missionary(
    state: tuple[int], total_entity: tuple[int], prev_state: list[StateSpaceTree] = []
):
    if len(prev_state) == 0:
        prev_state.append(StateSpaceTree(state, (0,0), further = False, childs = []))
    current_state: list = list()
    
    if state == (0, 0, 1):
        return []
    
    for m in range(total_entity[0]):
        for c in range(total_entity[1]):
            boat = (m, c)
            if not is_legal_move(state, boat, total_entity):
                continue
            else:
                new_state = next_state(state, boat, total_entity)
                state_repeated = None

                for st in prev_state:
                    if st.state == new_state.state:
                        state_repeated = st
                        break

                if state_repeated:
                    new_state.repeated = True
                    # new_state.add_childs(state_repeated.childs)
                    pass
                else:
                    prev_state.append(new_state)

                if new_state.further and state_repeated is None:
                    child_state = cannibals_and_missionary(
                        new_state.state, total_entity, prev_state
                    )
                    new_state.add_childs(child_state)

                current_state.append(new_state)
    return current_state


def initTree(state: StateSpaceTree, graph, generator):
    COLORS = ("green", "red", "blue")
    index = 0
    if state.repeated:
        index = 2
    elif not state.further:
        index = 1
    graph.node(state.node_name(generator), state.state_representation(), color=COLORS[index])
    for child in state.childs:
        initTree(child, graph, generator)

def drawTree(state: StateSpaceTree, graph):
    if len(state.childs) > 0:
        for child in state.childs:
            graph.edge(f"{state.node_name()}:f1", f"{child.node_name()}:f1", label = child.edge(), len="1.00")
            drawTree(child, graph)

def state_space_tree(start_state: StateSpaceTree):
    generator = Generator()
    g = graphviz.Digraph('g', filename='btree.dot',
                     node_attr={'shape': 'record', 'height': '.4'})
    initTree(start_state, g, iter(generator))
    drawTree(start_state, g)
    g.save()

    
def main():
    in_state = StateSpaceTree(initial_state, (0, 0), True, [])
    tree = cannibals_and_missionary(in_state.state, max_number)
    in_state.add_childs(tree)
    # in_state.display(depth=20)
    state_space_tree(in_state)
    # printing tree


if __name__ == "__main__":
    main()
