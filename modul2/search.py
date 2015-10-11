from heapq import heappush, heappop
from algorithms.utils import memoize

class Agenda:
    """ Also known as a priority queue """
    def __init__(self):
        pass

    @staticmethod
    def add(queue, node):
        # Push node onto heap
        heappush(queue, node)

    @staticmethod
    def pop(queue):
        # Use heappop to retrieve node with highest priority
        return heappop(queue), queue

    @staticmethod
    def contains(item, queue):
        return item in queue


class LIFO:
    """ Also known as a stack """
    def __init__(self):
        pass

    @staticmethod
    def add(_open, item):
        _open.append(item)  # Last in

    @staticmethod
    def pop(queue):
        return queue.pop(), queue  # First out

    @staticmethod
    def contains(item, queue):
        return item in queue


class FIFO:
    """ Also known as a queue """
    def __init__(self):
        pass

    @staticmethod
    def add(_open, item):
        _open.appendleft(item)  # First in

    @staticmethod
    def pop(queue):
        return queue.pop(), queue  # First out

    @staticmethod
    def contains(item, queue):
        return item in queue


class GraphSearch:
    def __init__(self, problem, frontier):
        self.problem = problem
        self.frontier = frontier()
        self.open, self.closed, self.path, self.came_from = [], [], [], {}

        self.is_closed = memoize(lambda node: node in self.closed)

        # Initializing
        self.g = {self.problem.start: 0}
        self.frontier.add(self.open, self.problem.start)

    def search(self):
        """
        A general algorithm for A*, dfs and bfs search.
        :param problem: The problem instance that this graph searcher will try to solve
        :param frontier: Class which holds methods to interact with the data structure of open nodes
        :return: Path to goal and indicator of success
        """
        _open, closed, path = self.open, self.closed, self.path
        problem, g, frontier = self.problem, self.g, self.frontier
        is_closed = self.is_closed

        while _open:
            node, _open = frontier.pop(_open)
            closed.append(node)
            #problem.save_state(node)
            path.append(node)
            if problem.is_goal(node):
                return self.path, True
            for child in problem.actions(node):
                new_g = g[node] + problem.path_cost((node, child))
                if is_closed(child):
                    continue
                in_open = frontier.contains(child, _open)
                if not in_open or (child in g and new_g < g[child]):
                    g[child] = new_g
                    child.f = new_g + problem.h(child)
                    self.came_from[child] = node
                    if not in_open:
                        frontier.add(_open, child)

        return [], False

    def search_yieldie(self):
        """
        A general algorithm for A*, dfs and bfs search.
        :param problem: The problem instance that this graph searcher will try to solve
        :param frontier: Class which holds methods to interact with the data structure of open nodes
        :return: Path to goal and indicator of success
        """
        _open, closed, path = self.open, self.closed, self.path
        problem, g, frontier = self.problem, self.g, self.frontier
        is_closed = self.is_closed
        solved = False

        while _open:
            node, _open = frontier.pop(_open)
            closed.append(node)
            #problem.save_state(node)
            yield node
            if problem.is_goal(node):
                solved = True
                break
            for child in problem.actions(node):
                new_g = g[node] + problem.path_cost((node, child))
                if is_closed(child):
                    continue
                in_open = frontier.contains(child, _open)
                if not in_open or (child in g and new_g < g[child]):
                    g[child] = new_g
                    child.f = new_g + problem.h(child)
                    self.came_from[child] = node
                    if not in_open:
                        frontier.add(_open, child)

        return solved




    def reconstruct_path(self, path):
        " Reconstructs path from goal to start node. "
        while path[-1] != self.problem.start:
            path.append(self.came_from[path[-1]])
        return path[::-1]