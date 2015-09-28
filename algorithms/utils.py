def memoize(f):
    memo = {}
    def helper(x, memo=memo):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper