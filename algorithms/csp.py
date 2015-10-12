from algorithms.search import Problem
from copy import deepcopy
from abc import abstractclassmethod
from itertools import count
counter = count()


class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description

    def __repr__(self):
        return "<Constraint (variables:%s, c:%s)>" % (self.variables, self.description or '')


class CSP(Problem):
    def __init__(self, node_domain_map, constraints):
        self.node_domain_map = node_domain_map
        self.constraints = constraints

        Problem.__init__(self, (node_domain_map, constraints))

    def get_domain(self, node):
        return self.node_domain_map[node]

    def set_domain(self, node, domain):
        self.node_domain_map[node] = domain

    def actions(self, state):
        # Generates children and runs the rerun method.
        actions = []
        for node, dom in state.node_domain_map.items():
            if len(dom) > 1:
                for j in range(len(dom)):
                    child = deepcopy(state)
                    child.node_domain_map[node] = [dom[j]]
                    child.rerun(node)
                    if not child.contradiction:
                        actions.append(child)
                return actions
        return actions

    @abstractclassmethod
    def save_state(self):
        pass

    @abstractclassmethod
    def solve(self, algorithm):
        pass

    @abstractclassmethod
    def initialize(self):
        pass

    @abstractclassmethod
    def path_cost(self, movement):
        pass

    @abstractclassmethod
    def is_goal(self, other):
        pass

    def __repr__(self):
        return "<CSP (n: %s, c: %s)>" % (self.node_domain_map, self.constraints)


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.node_domain_map = csp.node_domain_map
        self.constraints = csp.constraints
        self.queue = []
        self.contradiction = False

    def __repr__(self):
        return "<GAC(n:%s, q:%s, c:%s)>" % (self.node_domain_map, self.queue, self.constraints)

    def get_domain(self, node):
        return self.node_domain_map[node]

    def set_domain(self, node, domain):
        self.node_domain_map[node] = domain

    def initialize(self):
        self.queue = [(node, con) for node, con in self.constraints.items()]

    def domain_filtering(self):
        while self.queue:
            node, cons = self.queue.pop()
            #print('Node bro', (node, cons))
            if self.revise(node, cons):
                self.push_pairs(node, cons)

    """
    def revise_(self, node, cons):
        combinations = [self.csp.get_domain(j) for j in cons.variables if j != node]

        def constraint_cmp(x, var_combs=combinations):
            return any(map(lambda vs: cons.method(vs, [x]), var_combs))

        old_len = len(self.csp.get_domain(node))
        # print('woot', (node, [item for item in self.csp.get_domain(node) if constraint_cmp(item)]))
        self.csp.set_domain(node, [item for item in self.csp.get_domain(node) if constraint_cmp(item)])
        if not self.csp.get_domain(node):
            self.contradiction = True
            return False

        return old_len > len(self.csp.get_domain(node))
    """

    def revise(self, node, cons=None):
        from itertools import product
        """
        Removes all inconsistent values in a domain for all possible arc from an node
        It also saves to the csp_state if the current state is a contradiction
        :param from_node: The node to run revise from
        :return: Boolean telling whether the domain was revised or not
        """
        to_be_removed = []
        for arc in self.constraints[node].variables:
            for domain in self.get_domain(node):
                remove = True
                for x, y in product([domain], self.get_domain(arc)):
                    # print('c: %s, x:%s, y:%s' % (next(counter), (arc, x), (node, y)))
                    if self.csp.cons(x, y):
                        remove = False
                        break

                if remove:
                    to_be_removed.append(domain)

        for domain in to_be_removed:
            if domain in self.get_domain(node):
                self.get_domain(node).remove(domain)

        if to_be_removed:
            if not self.get_domain(node):
                self.contradiction = True
            return True

        return False

    def rerun(self, i):
        self.push_pairs(i)
        self.domain_filtering()

    def push_pairs(self, node, con=None):
        """ Finds (constraint, variable) pair affected by assumption
        and pushes pair to queue.
        """
        for arc in self.constraints[node].variables:
            if node != arc:
                self.queue.append((arc, node))
        '''
        for c in self.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.queue.append((j, c))
        '''