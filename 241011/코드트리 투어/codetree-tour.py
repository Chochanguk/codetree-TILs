from collections import deque

# BFS를 사용해 최단 거리를 계산
def bfs(start, n, graph):
    dist = [float('inf')] * n
    dist[start] = 0
    q = deque([start])

    while q:
        current_node = q.popleft()
        current_dist = dist[current_node]

        for next_node, weight in graph[current_node]:
            if current_dist + weight < dist[next_node]:
                dist[next_node] = current_dist + weight
                q.append(next_node)

    return dist

# 메인 함수 정의와 실행
Q = int(input())  # 명령 수
graph = {}  # 도시에 대한 그래프 (defaultdict 사용 안함)
products = {}  # 여행 상품 정보를 저장
start_city = 0  # 초기 출발 도시

for _ in range(Q):
    command = list(map(int, input().split()))
    cmd_type = command[0]

    if cmd_type == 100:  # 코드트리 랜드 건설
        n, m = command[1], command[2]
        for i in range(m):
            v, u, w = command[3 + 3 * i], command[4 + 3 * i], command[5 + 3 * i]
            
            # graph에 v와 u가 없으면 빈 리스트로 초기화
            if v not in graph:
                graph[v] = []
            if u not in graph:
                graph[u] = []

            graph[v].append((u, w))
            graph[u].append((v, w))

        dist = bfs(start_city, n, graph)  # BFS로 초기 출발지에서 각 도시까지의 최단 거리 계산

    elif cmd_type == 200:  # 여행 상품 생성
        id, revenue, dest = command[1], command[2], command[3]
        cost = dist[dest]  # 현재 출발지에서 도착지까지의 최단 거리
        products[id] = (revenue, dest, cost)  # 관리 품목

    elif cmd_type == 300:  # 여행 상품 취소
        id = command[1]
        if id in products:
            del products[id]  # 해당 배열 삭제

    elif cmd_type == 400:  # 최적의 여행 상품 판매
        best_product = None
        best_value = -float('inf')

        # 모든 여행 상품을 탐색하여 가장 이득이 큰 상품을 찾습니다.
        for id, (revenue, dest, cost) in products.items():
            profit = revenue - cost  # 이득

            # 이득이 0 이상이고 best_product가 None이 아닌 경우에만 비교
            if profit >= 0 and (best_product is None or profit > best_value or (profit == best_value and id < best_product)):
                best_product = id  # id 갱신
                best_value = profit  # 이득 갱신

        # 값이 있다면 출력가능
        if best_product is not None:
            print(best_product)
            del products[best_product]
        else:
            print(-1)

    elif cmd_type == 500:  # 여행 상품의 출발지 변경
        start_city = command[1]
        dist = bfs(start_city, n, graph)  # 새로운 출발지에서 각 도시까지 최단 거리 다시 계산
        # 모든 상품의 cost 값을 갱신
        for id in products:
            revenue, dest, _ = products[id]
            new_cost = dist[dest]
            products[id] = (revenue, dest, new_cost)