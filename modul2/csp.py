from algorithms.search import PriorityNode
from algorithms.csp import GAC
from itertools import count, product
counter = count()
DEBUG = True


class GAC_(GAC):
    def __init__(self, csp):
        self.csp = csp
        self.node_domain = csp.node_domain
        self.constraints = csp.constraints
        self.queue = []
        self.contradiction = False

        GAC.__init__(self, self.csp)

    def initialize(self):
        self.queue = [(node, cons) for cons in self.constraints for node in cons.variables]

    def revise(self, node, cons=None):
        combinations = [self.csp.get_domain(j) for j in cons.variables if j != node]

        def constraint_cmp(x, var_combs=combinations):
            return any(map(lambda vs: cons.method(vs, [x]), var_combs))

        old_len = len(self.csp.get_domain(node))
        self.csp.set_domain(node, [item for item in self.csp.get_domain(node) if constraint_cmp(item)])
        if not self.csp.get_domain(node):
            self.contradiction = True
            return False

        return old_len > len(self.csp.get_domain(node))

    def push_pairs(self, node, con=None):
        """ Finds (constraint, variable) pair affected by assumption
        and pushes pair to queue.
        """
        for c in self.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.queue.append((j, c))


class GACPriorityNode(GAC_, PriorityNode):
    def __init__(self, csp):
        GAC_.__init__(self, csp)
        PriorityNode.__init__(self, csp, csp)