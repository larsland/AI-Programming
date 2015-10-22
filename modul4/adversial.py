from abc import abstractclassmethod


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
        let a := +inf
        foreach child of node
            a := min(a, expectiminimax(child, depth-1))
    else if we are to play at node
        // Return value of maximum-valued child node
        let a := -inf
        foreach child of node
            a := max(a, expectiminimax(child, depth-1))
    else if random event at node
        // Return weighted average of all child nodes' values
        let a := 0
        foreach child of node
            a := a + (Probability[child] * expectiminimax(child, depth-1))
    return a
'''

inf = float('Inf')
"""
Maybe implement minimax with if else on maximizingplayer instead of double innard defs.
"""


def minimax_decision(state, game, depth, maximizingPlayer):
    # player = game.to_move(state)
    def max_value(state):
        if game.terminal_test(state) or depth == 0:
            return game.utility(state, player)
        v = -inf
        for a, s in game.actions(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = inf
        for a, s in game.actions(state):
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    action, state = max(game.actions(state), lambda a, s: min_value(s))
    return action


def alpha_beta_search(state, game, d=6, cutoff_test=None):
    # player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -inf
        for a, s in game.actions(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = inf
        for a, s in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))

    action, state = argmax(game.successors(state), lambda a, s: min_value(s, -inf, inf, 0))
    return action





