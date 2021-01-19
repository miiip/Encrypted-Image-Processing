import math

def heaviside(x, r):
    tmp  = math.tanh((2**r)*x)
    tmp = 1 + tmp
    tmp = 1/2 * tmp
    return tmp

def sgn(x, r):
    tmp = heaviside(x, r)
    return 2*tmp - 1

def aprox_heaviside(x, r):
    for i in range(r):
        tmp = x * (1.9142 - (x**2))
        x = tmp
    return tmp

def aprox_sgn(x, r):
    tmp = aprox_heaviside(x,r)
    return 2*tmp -1

x = -0.01968
r = 6
print(aprox_heaviside(x,r))
print(sgn(x, r))
