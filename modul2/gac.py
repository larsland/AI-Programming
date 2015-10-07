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


class GACState(CSP):
    def __init__(self, nodes, problem, constraints):
        self.nodes = nodes
        self.problem = problem
        self.constraints = constraints
        self.queue = []
        self.contradiction = False
        self.g = 1
        self.f = lambda: self.g + self.problem.h(self)

        CSP.__init__(self, nodes, nodes, constraints)

    def __lt__(self, other):
        return self.f() < other.f()

    def __repr__(self):
        return "<GACState(n:%s, q:%s, f:%s)>" % (self.nodes, self.queue, self.f())

    def initialize(self):
        self.queue = [(node, cons) for cons in self.constraints for node in cons.variables]

    def domain_filtering(self):
        while self.queue:
            node, cons = self.queue.pop()
            if self.revise(node, cons):
                self.push_pairs(node, cons)

    def revise(self, node, cons):
        combinations = [i for i in map(list, zip(*[self.nodes[j] for j in cons.variables if j != node]))]

        def constraint_cmp(x, var_combs=combinations):
            return any(map(lambda vs: cons.method(vs + [x]), var_combs))
            #return any(map(lambda vs: vs != x, var_combs))

        old_len = len(self.nodes[node])
        self.nodes[node] = [item for item in self.nodes[node] if constraint_cmp(item)]
        if not self.nodes[node]:
            self.contradiction = True
            return False
        return old_len > len(self.nodes[node])

    def domain_filtering_new(self):
        while self.queue:
            cons, node = self.queue.pop()
            if self.revise(node, cons):
                self.push_pairs(node, cons)

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
    """
    def unsat_cs(self):
        uc = 0
        for c in self.constraints:
            ds = []
            for i in c.vars:
                if len(self.nodes[i]) > 1:
                    break
                ds.append(self.nodes[i][0])

            if not c.method(ds):
                uc += 1
        return uc

    def uncolor_vs(self):
        return sum([1 for d in self.nodes.itervalues() if len(d) > 1])
    """
