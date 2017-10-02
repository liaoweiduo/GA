import random
import time
import math
import sys

start = time.clock()

'''Initialization phase'''
xmin = -100
xmax = 100
alpha = 1

d = 5  #num of point in dataset
miu = 20
# fstar = 50
pm = 1 / d
x = [[0 for col in range(d)] for row in range(miu)]
f = [0 for row in range(miu)]
xbsf = [0 for col in range(d)]
fxbsf = -sys.maxsize - 1
t = 1
n = 0
nmax = 10000

'''randomly generating the initial solution x: Fisher-Yates's shuffle method'''
def init():
    for i in range(miu):
        for j in range(d):
            x[i][j] = (xmax - xmin) * random.random() + xmin

'''objective function'''
def evaluate(a):
    l = 0
    for i in range(d):
        l = l + a[i] * a[i]
    return -l   #the farther of distance, the less wanted of individual

'''Mating Selection'''
def biTournamentMS():   #return index
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
def BLX_alpha(xa, xb):   #xa and xb are index
    u = [0 for col in range(d)]
    for i in range(d):
        A = min(x[xa][i], x[xb][i]) - alpha * math.fabs(x[xa][i] - x[xb][i])
        B = max(x[xa][i], x[xb][i]) + alpha * math.fabs(x[xa][i] - x[xb][i])
        u[i] = max(min(((B - A) * random.random() + A), xmax), xmin)
    return u

'''Environmental Selection'''
def worstES(u):
    xc = f.index(min(f))
    fu = evaluate(u)
    if fu >= f[xc]:
        x[xc] = u.copy()
        f[xc] = fu

'''Initialize the population P = {x1, ..., xμ} randomly'''
init()

'''Evaluate each individual xi in P by equation(1)'''
for i in range(miu):
    f[i] = evaluate(x[i])
    if fxbsf < f[i]:
        xbsf = x[i]
        fxbsf = f[i]

while n < nmax:
    if n % (nmax / 10) == 0:
        print('n=', n)
        print('fxbsf=', fxbsf)
        print('xbsf=', xbsf)
    '''Mating selection'''
    (xa, xb) = biTournamentMS()
    '''Crossover'''
    u = BLX_alpha(xa, xb)
    # print('xa=', x[xa])
    # print('xb=', x[xb])
    # print('u=', u)
    '''Evaluate the child u'''
    fu = evaluate(u)
    n = n + 1
    '''Update the best-so-far solution xbsf'''
    if fxbsf < fu:
        xbsf = u
        fxbsf = fu

    '''Environmental selection'''
    worstES(u)

    t = t + 1

'''Result'''

print("Result:")
print("miu:", miu)
print("d:", d)
print("n:", n)
print("xbsf:", xbsf)
print("f(xbsf):", fxbsf)

elapsed = (time.clock() - start)
print("Time used:", elapsed)


fp = open("Sphere_Log.txt", "a") #追加方式打开
fp.write("Parameter:\n")
fp.write("binary tournament mating selection\n")
fp.write("BLX_alpha alpha=" + str(alpha) + "\n")
fp.write("PQ union environmental selection\n")
fp.write("Result:\n")
fp.write("miu:" + str(miu) + "\n")
fp.write("d:" + str(d) + "\n")
fp.write("n:" + str(n) + "\n")
fp.write("xbsf:" + str(xbsf) + "\n")
fp.write("f(xbsf):"+ str(fxbsf) + "\n")
fp.write("Time used:" + str(elapsed) + "\n\n")