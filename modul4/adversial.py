from abc import abstractclassmethod
from math import inf


class Game:
    @abstractclassmethod
    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."

    @abstractclassmethod
    def make_move(self, move, state):
        "Return the state that results from making a move from a state."

    @abstractclassmethod
    def utility(self, state, player):
        "Return the value of this final state to player."

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def actions(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


'''
function expectiminimax(node, depth)
    if node is a terminal node or depth = 0
        return the heuristic value of node
    if the adversary is to play at node
        // Return value of minimum-valued child node
        let α := +∞
        foreach child of node
            α := min(α, expectiminimax(child, depth-1))
    else if we are to play at node
        // Return value of maximum-valued child node
        let α := -∞
        foreach child of node
            α := max(α, expectiminimax(child, depth-1))
    else if random event at node
        // Return weighted average of all child nodes' values
        let α := 0
        foreach child of node
            α := α + (Probability[child] * expectiminimax(child, depth-1))
    return α
'''

inf = float('Inf')
"""
Maybe implement minimax with if else on maximizingplayer instead of double innard defs.
"""


def minimax_decision(state, game):
    # player = game.to_move(state)
    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -inf
        for a, s in game.actions(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a, s in game.successors(state):
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    action, state = max(game.successors(state), lambda a, s: min_value(s))
    return action


