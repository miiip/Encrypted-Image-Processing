import math

def expansion(x, alpha, limit):
    sum = 0
    prod = 1
    fact = 1
    pow = 1
    for i in range(limit):
        sum = sum + prod * pow / fact
        prod = prod * (alpha - i)
        pow = pow * x
        fact = fact * (i + 1)
    return sum

def exponential_expansion(x, limit):
    sum = 0
    prod = 1
    fact = 1
    for i in range(limit):
        sum = sum + prod / fact
        prod = prod * x
        fact = fact * (i + 1)
    return sum

def exponentiation(base, exp, limit):
    exp_int = int(exp)
    exp_frac = exp - exp_int
    if exp_int == 0:
        ans = 1
    else:
        ans = base**exp_int
    log = logarithm(base, limit)
    tmp = exponential_expansion(exp_frac*log, limit)
    ans = ans * tmp
    return ans

def logarithm(x, limit):
    a = 0.5
    sum = math.log(a)
    prod = 1
    pow = 1
    for i in range(1, limit):
        prod = prod * (x - a)
        pow = pow * a
        if i%2 == 1:
            sum = sum + prod / (i * pow)
        else:
            sum = sum - prod / (i * pow)
    return sum
base = 1/4
exp = 1/2
limit = 8
ans = exponentiation(base, exp, limit)
print(ans)
print(base**exp)

x = 1/4
ans = logarithm(x, 1000)
print(ans)
print(math.log(x))
