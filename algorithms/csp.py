from algorithms.search import Problem, PriorityNode
from algorithms.utils import unique_permutations
from copy import deepcopy
from abc import abstractclassmethod
from itertools import count, product
# For debugging purposes:
counter = count()
DEBUG = False


class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description

    def __repr__(self):
        return "<Constraint (variables:%s, c:%s)>" % (self.variables, self.description or '')


class CSP(Problem):
    def __init__(self, node_domain, constraints):
        self.node_domain = node_domain
        self.constraints = constraints

        Problem.__init__(self, (node_domain, constraints))

    def get_domain(self, node):
        return self.node_domain[node]

    def set_domain(self, node, domain):
        self.node_domain[node] = domain

    def actions(self, state):
        """
        Fetches all successor nodes from a given CSP state
        In this spesific problem that means all states with a domain
        length greater than 1 for a random node
        :return: The generated successor nodes
        """
        actions = []
        for node, dom in state.node_domain.items():
            if len(dom) > 1:
                for j in range(len(dom)):
                    child = deepcopy(state)
                    child.node_domain[node] = [dom[j]]
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
        return "<CSP (n: %s, c: %s)>" % (self.node_domain, self.constraints)


class GAC:
    def __init__(self, csp):
        self.csp = csp
        self.node_domain = csp.node_domain
        self.constraints = csp.constraints
        self.queue = []
        self.contradiction = False

    def __repr__(self):
        return "<GAC(n:%s, q:%s, c:%s)>" % (self.node_domain, self.queue, self.constraints)

    def get_domain(self, node):
        return self.node_domain[node]

    def set_domain(self, node, domain):
        self.node_domain[node] = domain

    def initialize(self):
        self.queue = [(node, con) for node, con in self.constraints.items()]

    def domain_filtering(self):
        while self.queue:
            node, cons = self.queue.pop()
            if self.revise(node, cons):
                self.push_pairs(node, cons)

    def revise(self, node, cons=None):
        """
        Removes all inconsistent values in a domain for all possible arc from an node
        It also saves to the csp_state if the current state is a contradiction
        :param from_node: The node to run revise from
        :return: Boolean telling whether the domain was revised or not
        """
        removals = False

        constraint = self.constraints[node]
        for var in constraint.variables:
            for domain in self.get_domain(node):
                remove = True
                for x, y in product([domain], self.get_domain(var)):
                    if DEBUG:
                        print('c: %s, x:%s, y:%s' % (next(counter), x, y))

                    if constraint.method(x, y):
                        remove = False
                        break

                if remove:
                    self.prune(self.get_domain(node), domain)
                    removals = True

        if removals:
            if not self.get_domain(node):
                self.contradiction = True
            return True

        return False

    def prune(self, domains, domain):
        if domain in domains:
            domains.remove(domain)

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


class GACPriorityNode(GAC, PriorityNode):
    def __init__(self, csp):
        GAC.__init__(self, csp)
        PriorityNode.__init__(self, csp, csp)