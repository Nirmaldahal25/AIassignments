import graphviz
from statespacetree import cannibals_and_missionary, StateSpaceTree, Generator

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

def bfs(root : StateSpaceTree)->list[StateSpaceTree]:
    visited_node: list[StateSpaceTree] = list()
    queue : list[StateSpaceTree] = list()
    queue.append(root)

    while(len(queue) != 0):
        tree = queue.pop(0)
        if tree not in visited_node:
            visited_node.append(tree)
        if tree.repeated:
            continue
        elif tree.state == (0,0,1):
            break
        else:
            queue += tree.childs
    
    return visited_node


def initTree(states: list[StateSpaceTree], graph, generator):
    COLORS = ("green", "red", "blue")
    for state in states:
        index = 0
        if state.repeated:
            index = 2
        elif not state.further:
            index = 1
        graph.node(state.node_name(generator), state.state_representation(), color=COLORS[index])

def drawTree(states: list[StateSpaceTree], graph):
    count = 1
    while count <= (len(states) - 1):
        graph.edge(f"{states[count-1].node_name()}:f1", f"{states[count].node_name()}:f1", len="1.00")
        count += 1


def main():
    in_state = StateSpaceTree(initial_state, (0, 0), True, [])
    tree = cannibals_and_missionary(in_state.state, max_number)
    in_state.add_childs(tree)

    nodes = bfs(in_state)
    generator = Generator()
    g = graphviz.Digraph('g', filename='btreebfs.dot',
                     node_attr={'shape': 'record', 'height': '.4'})
    initTree(nodes, g, iter(generator))
    drawTree(nodes, g)
    g.save()

if __name__=="__main__":
    main()