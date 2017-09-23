import random
import time

start = time.clock()


'''Initialization phase'''
miu = 20
d = 50
pm = 1 / d
x = [[0 for col in range(d)] for row in range(miu)]
f = [0 for row in range(miu)]
xbsf = [0 for col in range(d)]
fxbsf = 0
t = 1
n = 1
nmax = 1000000000000000

def evaluate(a):
  return sum(a)

def init():
    for i in range(miu):
        for j in range(d):
            if random.random() < 0.5:
                x[i][j] = 0
            else:
                x[i][j] = 1

def crossover(xa,xb):
    u = [0 for col in range(d)]
    for j in range(d):
        if random.random() < 0.5:
            u[j] = x[xa][j]
        else:
            u[j] = x[xb][j]
    return u

def bitFlip(u, pm):
    mutate = 0
    for j in range(d):
        if random.random() < pm:
            if u[j] == 0:
                u[j] = 1
            else:
                u[j] = 0
            mutate = 1
    return mutate


'''Initialize the population P = {x1, ..., xμ} randomly'''
init()

'''Evaluate each individual xi in P by equation(1)'''
for i in range(miu):
    f[i] = evaluate(x[i])
    if fxbsf < f[i]:
        xbsf = x[i]
        fxbsf = f[i]


while fxbsf < d and n < nmax:
    '''Mating selection'''
    xa = random.randint(0, miu - 1)
    xb = xa
    while xb == xa:
        xb = random.randint(0, miu - 1)
    '''Crossover'''
    u = crossover(xa, xb)
    '''Mutation'''
    bitFlip(u, pm)
    '''Evaluate the child u'''
    fu = evaluate(u)
    n = n + 1
    '''Update the best-so-far solution xbsf'''
    if fxbsf < fu:
        xbsf = u
        fxbsf = fu
    '''Environmental selection'''
    xc = random.randint(0, miu - 1)
    if fu >= f[xc]:
        x[xc] = u
    t = t + 1

'''Result'''
print("n:", n)
print("xbsf:", xbsf)
print("f(xbsf):", fxbsf)


elapsed = (time.clock() - start)
print("Time used:", elapsed)