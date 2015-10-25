#from abc import abstractclassmethod
import numpy as np
import multiprocessing as mp
import copy as cp

'''
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
'''

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

depth_by_zeros_map = {
    0: 0,
    1: 5, 2: 5, 3: 4, 4: 4,
    5: 4, 6: 3, 7: 3, 8: 3,
    9: 3, 10: 3, 11: 2, 12: 2,
    13: 2, 14: 1, 15: 1, 16: 1
}


def get_dynamic_depth(state, prev, depth_by_zeros=depth_by_zeros_map):
    zeros = state[state == 0].size
    depth = depth_by_zeros[zeros] - prev
    return depth if depth > 0 else 0


def expectimax_process(q, game, state, depth, player):
    q.put(expectimax(game, state, depth, player))


def expectimax_top(game, state, depth_f=get_dynamic_depth):
    depth = depth_f(state, 0)
    q = mp.Queue()

    processes = []
    for i, action in game.actions(state):
        processes.append(mp.Process(target=expectimax_process, args=(q, game, action, depth, True)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    a = -float('Inf')

    state = []
    while not q.empty():
        a_, state_ = q.get()
        if a_ > a:
            a = a_
            state = state_

    return a, state


def expectimax(game, state, depth, player=True):
    if game.terminal_test(state) or depth == 0:
        a = game.utility(state)
    else:
        if player:
            a = -float('Inf')

            actions = game.actions(state)
            for action, new_state in actions:
                a_, state_ = expectimax(game, new_state, depth-1, player=False)
                if a_ > a:
                    a = a_
                    state = state_
            return a, state
        else:
            a = 0.0
            zeros = 0
            for (i, j), cell in np.ndenumerate(state):
                if cell == 0:
                    zeros += 1
                    copy_state = np.copy(state)
                    copy_state[i, j] = 1
                    temp_a, _ = expectimax(game, copy_state, depth-1, player=True)
                    a += (0.9 * temp_a) / zeros

                    copy_state[i, j] = 2
                    temp_a, _ = expectimax(game, copy_state, depth-1, player=True)
                    a += (0.1 * temp_a) / zeros

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


