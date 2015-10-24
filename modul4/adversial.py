from abc import abstractclassmethod
import numpy as np


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
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def actions(self, state, player=True):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state, player)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


inf = float('Inf')

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


def get_dynamic_depth(state, prev):
    # zeros = sum([1 for x in [line for line in state] if x == 0])
    zeros = 0
    for line in state:
        for x in line:
            if x == 0:
                zeros += 1

    if zeros > 10:
        depth = 3 - prev
    elif zeros > 7:
        depth = 2 - prev
    elif zeros > 5:
        depth = 2 - prev
    else:
        depth = 1 - prev

    #print("Dynamic depth size: ", depth)
    return depth if depth > -1 else 0


def expectimax(game, state, depth_f=get_dynamic_depth, prev_d=0, player=True):
    depth = depth_f(state, prev_d)
    #print("DEPTH", depth)
    #print("depth: %s, player: %s \n %s \n %s" % (depth, player, state, '-'*100))
    if game.terminal_test(state, player) or depth == 0:
        a = game.utility(state)

        #print('Terminal state:\n', (a, state))
    else:
        if player:
            #print("Player " + ("-"*50))
            a = -float('Inf')
            actions = list(game.actions(state, player))

            for action, new_state in actions:
                a_, state_ = expectimax(game, new_state, prev_d=prev_d+1, player=not player)
                if a_ > a:
                    a = a_
                    state = state_
            return a, state
        else:
            a = 0.0
            zeros = 0.0
            for i in range(4):
                for j in range(4):
                    if state[i, j] == 0:
                        for n, p in zip([1, 2], [0.9, 0.1]):
                            zeros += 1
                            copy_state = np.copy(state)
                            copy_state[i, j] = 1
                            temp_a, _ = expectimax(game, copy_state, prev_d=prev_d+1, player=not player)
                            a += (p * temp_a) / zeros

            '''
            for action, state in game.actions(state, player):
                a_, state_ = expectimax(game, state, player=not player)
                if a_ < a:
                    a = a_
                    state = state_
                # a, state =
                # min(a, expectimax(game, state, depth=depth-1, player=not player), key=lambda x: print(x) and x[0])
            '''

            return a, state
    return a, state
"""
Maybe implement minimax with if else on maximizingplayer instead of double innard defs.
"""

'''
def minimax_decision(state, game, depth, player=True):
    # player = game.to_move(state)
    def max_value(state):
        if game.terminal_test(state) or depth == 0:
            return game.utility(state)
        v = -inf
        for a, s in game.actions(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state)
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
'''


