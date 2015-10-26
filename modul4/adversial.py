import numpy as np
import multiprocessing as mp

inf = float('Inf')

depth_by_zeros_map = {
    0: 0, 1: 5, 2: 5, 3: 4, 4: 4,
    5: 4, 6: 3, 7: 3, 8: 3,
    9: 3, 10: 3, 11: 2, 12: 2,
    13: 2, 14: 1, 15: 1, 16: 1
}


def get_dynamic_depth(state, depth_by_zeros=depth_by_zeros_map):
    zeros = state[state == 0].size
    depth = depth_by_zeros[zeros]
    return depth if depth > 0 else 0


def expectimax_process(q, game, state, depth, player):
    q.put(expectimax(game, state, depth, player))


def expectimax_top(game, state, depth_f=get_dynamic_depth):
    depth = depth_f(state)
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
