import heapq

# 다익스트라 알고리즘을 사용해 start에서 모든 목표 노드까지의 최단 거리를 계산
def dijkstra_all_targets(start, n, graph):
    dist = [float('inf')] * n
    dist[start] = 0
    q = [(0, start)]  # (거리, 노드)

    while q:
        current_dist, current_node = heapq.heappop(q)

        if current_dist > dist[current_node]:
            continue

        for next_node, weight in graph.get(current_node, []):
            distance = current_dist + weight

            if distance < dist[next_node]:
                dist[next_node] = distance
                heapq.heappush(q, (distance, next_node))

    return dist


# 메인 함수 정의와 실행
Q = int(input())  # 명령 수
graph = {}  # 도시에 대한 그래프
products = {}  # 여행 상품 정보를 저장
start_city = 0  # 초기 출발 도시
n = 0  # 도시의 개수를 저장할 변수
dist = []  # 출발지로부터 모든 도시까지의 최단 거리 리스트

for _ in range(Q):
    command = list(map(int, input().split()))
    cmd_type = command[0]

    if cmd_type == 100:  # 코드트리 랜드 건설
        n, m = command[1], command[2]
        graph = {i: [] for i in range(n)}  # 그래프 초기화
        for i in range(m):
            v, u, w = command[3 + 3 * i], command[4 + 3 * i], command[5 + 3 * i]
            graph[v].append((u, w))
            graph[u].append((v, w))

        # 최초 출발지에서 모든 도시까지의 최단 거리 계산
        dist = dijkstra_all_targets(start_city, n, graph)

    elif cmd_type == 200:  # 여행 상품 생성
        id, revenue, dest = command[1], command[2], command[3]
        # 상품의 목표지점까지 최단 거리 저장 (이미 계산된 dist 리스트 활용)
        cost = dist[dest]
        products[id] = (revenue, dest, cost)

    elif cmd_type == 300:  # 여행 상품 취소
        id = command[1]
        if id in products:
            del products[id]

    elif cmd_type == 400:  # 최적의 여행 상품 판매
        best_product = None
        best_value = -float('inf')

        for id, (revenue, dest, cost) in products.items():
            profit = revenue - cost  # 이득

            if profit >= 0 and (best_product is None or profit > best_value or (profit == best_value and id < best_product)):
                best_product = id
                best_value = profit

        if best_product is not None:
            print(best_product)
            del products[best_product]
        else:
            print(-1)

    elif cmd_type == 500:  # 여행 상품의 출발지 변경
        start_city = command[1]
        # 새로운 출발지에서 모든 도시까지의 최단 거리 계산
        dist = dijkstra_all_targets(start_city, n, graph)

        # 모든 상품의 cost 값을 새 출발지에서의 최단 거리로 갱신
        for id in products:
            revenue, dest, _ = products[id]
            new_cost = dist[dest]
            products[id] = (revenue, dest, new_cost)