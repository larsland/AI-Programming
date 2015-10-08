class Constraint:
    def __init__(self, variables, method=None, description=None):
        self.variables = variables
        self.method = method
        self.description = description

    def __repr__(self):
        return "<Constraint (variables:%s, c:%s)>" % (self.variables, self.description or '')


class CSP:
    def __init__(self, nodes, domain, constraints):
        self.nodes = nodes
        self.domain = domain
        self.constraints = constraints

    def __repr__(self):
        return "<CSP (n: %s, d: %s, c: %s)>" % (self.nodes, self.domain, self.constraints)


class GAC(CSP):
    def __init__(self, nodes, problem, constraints):
        self.nodes = nodes
        self.problem = problem
        self.constraints = constraints
        self.queue = []

        CSP.__init__(self, nodes, nodes, constraints)

    def __repr__(self):
        return "<GAC(n:%s, q:%s, c:%s, q:%s)>" % (self.nodes, self.queue, self.constraints, self.queue)

    def initialize(self):
        self.queue = [(node, cons) for cons in self.constraints for node in cons.variables]

    def domain_filtering(self):
        while self.queue:
            node, cons = self.queue.pop()
            if self.revise(node, cons):
                self.push_pairs(node, cons)

    def revise(self, node, cons):
        combinations = [self.nodes[j] for j in cons.variables if j != node]

        def constraint_cmp(x, var_combs=combinations):
            return any(map(lambda vs: cons.method(vs, [x]), var_combs))

        old_len = len(self.nodes[node])
        self.nodes[node] = [item for item in self.nodes[node] if constraint_cmp(item)]
        if not self.nodes[node]:
            self.contradiction = True
            return False
        return old_len > len(self.nodes[node])

    def rerun(self, i):
        self.push_pairs(i)
        self.domain_filtering()

    def push_pairs(self, node, con=None):
        """ Finds (constraint, variable) pair affected by assumption
        and pushes pair to queue.
        """
        for c in self.constraints:
            if node in c.variables and (con is None or c != con):
                for j in c.variables:
                    if j != node:
                        self.queue.append((j, c))