from scipy.stats import binom

N = 1000
K = 300
p = 1/3
more_than_K_rocks_likelihood = 1 - binom.cdf(K, N, p)
print('more_than_K_rocks_likelihood', more_than_K_rocks_likelihood)

from collections import defaultdict
def defaultdicttype():
    return defaultdict(int)
amap = defaultdict(defaultdicttype)
for N in range(3, 1000):
    print('================== N', N)
    for K in range(N//3, N):
        prob = 1- binom.cdf(K, N, p)
        if prob > 0.4:
            continue
        # print('N', N, 'K', K, 'prob(#rocks >= K)', prob)
        amap[N][K] = int(prob * 10000) # in basis point
        if prob < 0.01:
            break

listmap = [{} for _ in range(1000)]
for N, nmap in amap.items():
    low_K = min(nmap.keys())
    high_K = max(nmap.keys())
    listmap[N]['L'] = low_K
    listmap[N]['H'] = high_K
    for k, v in nmap.items():
        listmap[N][k] = v


ss = str(listmap)


