import random
import time
import math
import sys

start = time.clock()

'''Initialization phase'''
# f = open("database/wi29.tsp.txt", "r")

d = 29  #num of point in dataset
D = []
D.append((20833.3333, 17100.0000))
D.append((20900.0000, 17066.6667))
D.append((21300.0000, 13016.6667))
D.append((21600.0000, 14150.0000))
D.append((21600.0000, 14966.6667))
D.append((21600.0000, 16500.0000))
D.append((22183.3333, 13133.3333))
D.append((22583.3333, 14300.0000))
D.append((22683.3333, 12716.6667))
D.append((23616.6667, 15866.6667))
D.append((23700.0000, 15933.3333))
D.append((23883.3333, 14533.3333))
D.append((24166.6667, 13250.0000))
D.append((25149.1667, 12365.8333))
D.append((26133.3333, 14500.0000))
D.append((26150.0000, 10550.0000))
D.append((26283.3333, 12766.6667))
D.append((26433.3333, 13433.3333))
D.append((26550.0000, 13850.0000))
D.append((26733.3333, 11683.3333))
D.append((27026.1111, 13051.9444))
D.append((27096.1111, 13415.8333))
D.append((27153.6111, 13203.3333))
D.append((27166.6667, 9833.3333))
D.append((27233.3333, 10450.0000))
D.append((27233.3333, 11783.3333))
D.append((27266.6667, 10383.3333))
D.append((27433.3333, 12400.0000))
D.append((27462.5000, 12992.2222))


miu = 20
lamda = 5
# fstar = 50
pm = 1 / d
x = [[0 for col in range(d)] for row in range(miu)]
f = [0 for row in range(miu)]
xbsf = [0 for col in range(d)]
fxbsf = -sys.maxsize - 1
t = 1
n = 0
nmax = 1000000

'''randomly generating the initial solution x: Fisher-Yates's shuffle method'''
def init():
    for i in range(miu):
        for j in range(d):
            x[i][j] = D[j]
    for xindex in range(miu):
        for i in range(d - 1):     #  0 ~ d - 2
            j = random.randint(i, d - 1)
            tmp = x[xindex][i]
            x[xindex][i] = x[xindex][j]
            x[xindex][j] = tmp

'''objective function'''
def distance(a, b): #a and b are tuple
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))

def evaluate(a):    #a is tuple list
    l = 0
    for i in range(d - 1):
        l = l + distance(a[i], a[i + 1])
    l = l + distance(a[d - 1], a[0])
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
def OXcrossover(xa, xb):   #xa and xb are index    要保证每一个tuple都有，即不走重复路
    c1 = random.randint(0, d-1)
    c2 = c1
    while c2 == c1:
        c2 = random.randint(0, d-1)
    if c1 > c2:
        tmp = c1
        c1 = c2
        c2 = tmp
    u = x[xa].copy()
    uindex = (c2 + 1) % d
    xbindex = (c2 + 1) % d
    while uindex != c1:
        uuindex = c1
        while uuindex != uindex:
            if u[uuindex] == x[xb][xbindex]:
                break
            uuindex = (uuindex + 1) % d
        if uuindex == uindex:
            u[uindex] = x[xb][xbindex]
            uindex = (uindex + 1) % d
        xbindex = (xbindex + 1) % d
    return u

'''mutation'''
def invMutation(u):
    m1 = random.randint(0, d - 1)
    m2 = m1
    while m2 == m1:
        m2 = random.randint(0, d - 1)
    if m1 > m2:
        tmp = m1
        m1 = m2
        m2 = tmp
    h = (m2 - m1) / 2
    m1 = m1 + 1
    for k in range(1, int(h + 1)):
        l = u[m1 + k]
        u[m1 + k] = u[m2 - k]
        u[m2 - k] = l
    return u

'''Environmental Selection'''
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

while n < nmax:
    if n % 100 == 0:
        print('n=', n)
        print('fxbsf=', fxbsf)
        print('xbsf=', xbsf)
    q = []
    for i in range(lamda):
        '''Mating selection'''
        (xa, xb) = biTournamentMS()
        '''Crossover'''
        u = OXcrossover(xa, xb)
        '''Mutation'''
        invMutation(u)
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


fp = open("TSP_Log.txt", "a") #追加方式打开
fp.write("Parameter:\n")
fp.write("wi29")
fp.write("Fisher-Yates's shuffle init method\n")
fp.write("oneMax evaluation\n")
fp.write("binary tournament mating selection\n")
fp.write("OXcrossover\n")
fp.write("invMutation\n")
fp.write("PQ union environmental selection\n")
fp.write("Result:\n")
fp.write("miu:" + str(miu) + "\n")
fp.write("lamda:" + str(lamda) + "\n")
fp.write("d:" + str(d) + "\n")
fp.write("n:" + str(n) + "\n")
fp.write("xbsf:" + str(xbsf) + "\n")
fp.write("f(xbsf):"+ str(fxbsf) + "\n")
fp.write("Time used:" + str(elapsed) + "\n\n")