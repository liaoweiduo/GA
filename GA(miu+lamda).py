import os
import random
import time

start = time.clock()

'''Initialization phase'''

miu = 20
lamda = 5
d = 50
fstar = d
pm = 1 / d
x = [[0 for col in range(d)] for row in range(miu)]
f = [0 for row in range(miu)]
xbsf = [0 for col in range(d)]
fxbsf = 0
t = 1
n = 1
nmax = 1000000000000000

def init():
    for i in range(miu):
        for j in range(d):
            ra = random.random()
            if ra < 0.5:
                x[i][j] = 0
            else:
                x[i][j] = 1

'''objective function'''
def oneMax(a):
    return sum(a)

def order3deceptive(a):
    s = 0
    j = 0
    fo = [[28, 26],[22, 0]], [[14, 0], [0, 30]]
    while j + 2 < d:
        s = s + fo[a[j]][a[j + 1]][a[j + 2]]
        j = j + 3
    return s

def evaluate(a):
    global fstar
    fstar = d
    #fstar = int(30 * d / 3)
    return oneMax(a)

'''Mating Selection'''
def randMS():
    xa = random.randint(0, miu - 1)
    xb = xa
    while xb == xa:
        xb = random.randint(0, miu  - 1)
    return (xa, xb)

def biTournamentMS():
    xd = random.randint(0, miu - 1)
    xe = xd
    xf = xd
    xg = xd
    while xe == xd:
        xe = random.randint(0, miu  - 1)
    while xf == xd or xf ==xe:
        xf = random.randint(0, miu  - 1)
    while xg == xd or xg == xe or xg == xf:
        xg = random.randint(0, miu  - 1)
    if f[xd] > f[xe]:
        xa = xd
    else:
        xa = xe
    if f[xf] > f[xg]:
        xb = xf
    else:
        xb = xg
    return (xa, xb)


'''Crossover'''
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
'''Environmental Selection'''
def randES(u):
    xc = random.randint(0, miu - 1)
    fu = evaluate(u)
    if fu >= f[xc]:
        x[xc] = u
        f[xc] = fu

def worstES(u):
    xc = f.index(min(f))
    fu = evaluate(u)
    if fu >= f[xc]:
        x[xc] = u
        f[xc] = fu

def pqUnionES(q):
    global x, f
    for i in range(q.__len__()):
        x.append(q[i])
    for i in range(miu, x.__len__()):
        f.append(evaluate(x[i]))
    fsorted = sorted(f, reverse = True)
    xtmp = []
    ftmp = []
    for i in range(miu):
        xtmp.append(x[f.index(fsorted[i])])
        ftmp.append(fsorted[i])
    x = xtmp
    f = ftmp

'''Initialize the population P = {x1, ..., xμ} randomly'''
init()

'''Evaluate each individual xi in P by equation(1)'''
for i in range(miu):
    f[i] = evaluate(x[i])
    if fxbsf < f[i]:
        xbsf = x[i]
        fxbsf = f[i]


while fxbsf < fstar and n < nmax:
    if n % 1000000 == 0:
        print('n=', n)
        print('fxbsf=', fxbsf)
        print('xbsf=', xbsf)
    q = []
    for i in range(lamda):
        '''Mating selection'''
        (xa, xb) = biTournamentMS()
        '''Crossover'''
        u = crossover(xa, xb)
        '''Mutation'''
        bitFlip(u, pm)
        '''Evaluate the child u'''
        fu = evaluate(u)
        n = n + 1
        q.append(u)
        '''Update the best-so-far solution xbsf'''
        if fxbsf < fu:
            xbsf = u
            fxbsf = fu

    '''Environmental selection'''
    pqUnionES(q)

    t = t + 1

'''Result'''

print("Result:")
print("miu:", miu)
print("lamda:", lamda)
print("d:", d)
print("n:", n)
print("xbsf:", xbsf)
print("f(xbsf):", fxbsf)

elapsed = (time.clock() - start)
print("Time used:", elapsed)


fp = open("GA(miu+lamda)_Log.txt", "a") #追加方式打开
fp.write("Parameter:\n")
fp.write("oneMax evaluation\n")
fp.write("binary tournament mating selection\n")
fp.write("PQ union environmental selection\n")
fp.write("Result:\n")
fp.write("miu:" + str(miu) + "\n")
fp.write("lamda:" + str(lamda) + "\n")
fp.write("d:" + str(d) + "\n")
fp.write("n:" + str(n) + "\n")
fp.write("xbsf:" + str(xbsf) + "\n")
fp.write("f(xbsf):"+ str(fxbsf) + "\n")
fp.write("Time used:" + str(elapsed) + "\n\n")