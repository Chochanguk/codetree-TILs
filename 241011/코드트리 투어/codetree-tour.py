import heapq
import sys

INF = float('inf')  # 무한대 값을 정의합니다.
MAX_N = 2000  # 코드트리 랜드의 최대 도시 개수입니다.
MAX_ID = 30005  # 여행상품 ID의 최대값입니다.

# 입력을 빠르게 받기 위한 설정입니다.
input = sys.stdin.readline

N, M = 0, 0  # 도시의 개수 N과 간선의 개수 M을 초기화합니다.
A = []  # 코드트리 랜드의 간선을 인접 행렬로 저장합니다.
D = []  # 다익스트라 알고리즘을 통해 시작도시부터 각 도시까지의 최단경로를 저장합니다.
isMade = []  # 여행상품이 만들어진적 있는지 저장합니다.
isCancel = []  # 여행상품이 취소되었는지 저장합니다.
S = 0  # 여행 상품의 출발지입니다.

class Package:
    def __init__(self, id, revenue, dest, profit):
        self.id = id
        self.revenue = revenue
        self.dest = dest
        self.profit = profit

    def __lt__(self, other):
        if self.profit == other.profit:
            return self.id < other.id
        return self.profit > other.profit

pq = []  # 우선순위 큐 초기화

# dijkstra 알고리즘을 heapq를 이용해 개선한 함수입니다.
def dijkstra():
    global D
    D = [INF] * N
    D[S] = 0
    pq = [(0, S)]  # (거리, 도시) 형식으로 우선순위 큐에 시작 도시를 넣음

    while pq:
        current_dist, v = heapq.heappop(pq)

        # 이미 처리된 도시라면 건너뜁니다.
        if current_dist > D[v]:
            continue

        # v 도시와 인접한 모든 도시를 확인하여 최단 거리 갱신
        for u in range(N):
            if A[v][u] != INF:  # 연결된 도시인 경우
                next_dist = current_dist + A[v][u]
                if next_dist < D[u]:
                    D[u] = next_dist
                    heapq.heappush(pq, (next_dist, u))

# 코드트리랜드를 입력받고 주어진 코드트리 랜드를 인접행렬에 저장합니다
def buildLand(n, m, arr):
    global A, N, M
    N, M = n, m
    A = [[INF] * N for _ in range(N)]
    for i in range(N):
        A[i][i] = 0  # 도시 자신에게 가는 비용은 0입니다.
    for i in range(M):
        u, v, w = arr[i * 3], arr[i * 3 + 1], arr[i * 3 + 2]
        A[u][v] = min(A[u][v], w)
        A[v][u] = min(A[v][u], w)

# 여행 상품을 추가합니다
def addPackage(id, revenue, dest):
    isMade[id] = True
    profit = revenue - D[dest]
    heapq.heappush(pq, Package(id, revenue, dest, profit))

# id에 해당하는 여행상품이 취소되었음을 기록합니다
def cancelPackage(id):
    if isMade[id]:
        isCancel[id] = True

# 최적의 여행상품을 판매합니다
def sellPackage():
    while pq:
        p = pq[0]
        if p.profit < 0:
            break
        heapq.heappop(pq)
        if not isCancel[p.id]:
            return p.id
    return -1

# 변경할 시작도시를 입력받고 변경됨에 따른 기존 여행상품 정보들을 수정합니다.
def changeStart(param):
    global S
    S = param
    dijkstra()  # 새로운 출발지에 대해 다익스트라 알고리즘을 다시 실행합니다.
    temp_packages = []
    while pq:
        temp_packages.append(heapq.heappop(pq))
    for p in temp_packages:
        addPackage(p.id, p.revenue, p.dest)

Q = int(input())
isMade = [False] * MAX_ID
isCancel = [False] * MAX_ID
for _ in range(Q):
    query = list(map(int, input().split()))
    T = query[0]

    if T == 100:
        buildLand(query[1], query[2], query[3:])
        dijkstra()
    elif T == 200:
        id, revenue, dest = query[1], query[2], query[3]
        addPackage(id, revenue, dest)
    elif T == 300:
        id = query[1]
        cancelPackage(id)
    elif T == 400:
        print(sellPackage())
    elif T == 500:
        changeStart(query[1])