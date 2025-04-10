# with open('test_case.txt','r') as file:
#     input_lines=[line.strip() for line in file]
# input=iter(input_lines).__next__
# T=int(input())

from collections import deque

# 0. 부서지지 않은 포탑의 개수가 1개인가?
def is_last(board):

    N=len(board)
    M=len(board[0])
    cnt=0
    for i in range(N):
        for j in range(M):
            if board[i][j]==0:
                cnt+=1
    if N*M-cnt==1:
        return True
    else:
        return False

#1.1. 약한 공격자 선정
# 가장 약한 공격자 선정
def find_weak(t,board, towers):
    N=len(board)
    M=len(board[0])
    # 1. 공격력이 가장 낮은 포탑 좌표 리스트를 찾고
    weak_list = []  # 가장 공격력이 낮은 녀석을 찾음
    for i in range(N):
        for j in range(M):
            at = board[i][j]
            # 0이 아니면 집어넣기
            if at != 0:
                weak_list.append(towers[(i, j)] + [i, j])
    '''
    weak_list의 한 요소 => (1, True, False, 0, 1),
    1. 맨앞의 것으로 먼저 오름차순
    2. 공격 시각이 가장 최신이거
    3. 그 중에서 합이 (i+j) 큰거
    4. 3 만족시 그 중 열 값이 가장 큰것

    '''
    # 정렬 lambda 조건(1,2,3,4)
    weak_list.sort(key=lambda x: (x[0], -x[1], -(x[3] + x[4]), -x[4]))
    sx,sy=weak_list[0][3], weak_list[0][4]
    towers[(sx,sy)][1]=t # 공격시각을 현재 시각으로 설정
    towers[(sx, sy)][0] += N+M # 공격력 증가
    board[sx][sy]+=N+M

    return sx,sy,towers

#1.2. 강한 공격자 선정
def find_strong(t,board, towers):
    N = len(board)
    M = len(board[0])
    # 1. 공격력이 가장 낮은 포탑 좌표 리스트를 찾고
    strong_list = []  # 가장 공격력이 낮은 녀석을 찾음
    for i in range(N):
        for j in range(M):
            at = board[i][j]
            # 0이 아니고, 현재 시각에 공격한 애가 아니면
            if at != 0 and towers[(i,j)][2]!=t:
                strong_list.append(towers[(i, j)] + [i, j])
    '''
    strong_list의 한 요소 => (1, True, False, 0, 1),
    1. 맨앞의 것으로 먼저 내림차순
    2. 공격 시각이 가장 오래된거 (오름차순)
    3. 그 중에서 합이 (i+j) 작은거
    4. 3 만족시 그 중 열 값이 가장 작은거

    '''
    # 정렬 lambda 조건(1,2,3,4)
    strong_list.sort(key=lambda x: (-x[0], +x[1], (x[3] + x[4]), x[4]))
    sx, sy = strong_list[0][3], strong_list[0][4]

    # print("strong_list:",strong_list)
    return sx, sy, towers


#2. 레이저 공격
def laser_attack(board, towers, sx, sy, ex, ey):
    N, M = len(board), len(board[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우, 하, 좌, 상

    q = deque()
    visited = [[False] * M for _ in range(N)]
    prev = [[None] * M for _ in range(N)]

    q.append((sx, sy))
    visited[sx][sy] = True

    is_ok = False  # 레이저 공격 성공 여부

    while q:
        x, y = q.popleft()

        if (x, y) == (ex, ey):
            is_ok = True
            continue  # 우선순위 고려해야 하니까 break X

        for dx, dy in directions:
            nx, ny = (x + dx) % N, (y + dy) % M  # 맵을 넘어가면 반대편으로 이동
            if board[nx][ny] == 0:
                continue
            if visited[nx][ny]:
                continue
            visited[nx][ny] = True
            prev[nx][ny] = (x, y)  # nx,ny 도착 직전 좌푠
            q.append((nx, ny))

    if not is_ok:
        return False, board, towers  # 레이저 실패

    # 경로 복원
    path = []
    cx, cy = ex, ey
    # print("prev:", prev)
    while (cx, cy) != (sx, sy):
        path.append((cx, cy))
        cx, cy = prev[cx][cy]  # 현재 좌표 도달 전 좌표
    # 시점 넣고 반대로 뒤집음
    path.append((sx, sy))
    path.reverse()

    # 데미지 처리
    power = towers[(sx, sy)][0]

    for idx, (x, y) in enumerate(path):
        if (x, y) == (sx, sy):
            continue
        if (x, y) == (ex, ey):
            board[x][y] = max(0, board[x][y] - power)
            towers[(x, y)][0] = max(0, board[x][y])  # 공격력 갱신
            towers[(x, y)][2] = True  # 이번 턴에 공격 받음 (추후 회복시 체크용)

        else:
            board[x][y] = max(0, board[x][y] - (power // 2))
            towers[(x, y)][0] = max(0, board[x][y])  # 공격력 갱신
            towers[(x, y)][2] = True  # 이번 턴에 공격 받음 (추후 회복시 체크용)

    return True, board, towers


#2.2. 포탄 공격
def cannon_attack(board, towers, sx, sy, ex, ey):
    N, M = len(board), len(board[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1,-1), (-1,1), (1,-1), (1,1)]  # 우, 하, 좌, 상

    damage=board[ex][ey]
    # 주변 8개 공격 받음
    for dx, dy in directions:
        nx,ny=(ex+dx)%N,(ey+dy)%M

        if (nx,ny)!=(sx,sy):
            board[nx][ny] = max(0, board[nx][ny] - damage // 2)
            towers[(nx, ny)][0] = board[nx][ny]
            towers[(nx, ny)][2] = True
    # 자기 자신도 공격 받음

    board[ex][ey] = max(0, board[ex][ey]-damage)
    towers[(ex,ey)][0] = board[ex][ey]
    towers[(ex,ey)][2] = True

    return board, towers

#3. 회복
def recover(t,sx,sy,ex,ey,board,towers):
    N,M=len(board),len(board[0])
    for i in range(N):
        for j in range(M):
            if board[i][j]!=0 and (i,j)!=(sx,sy) and (i,j)!=(ex,ey) and  not towers[(i,j)][2]:
                board[i][j]+=1
                towers[(i, j)][0]+=1

    # 모든 피해 사실 원상 복구
    for i in range(N):
        for j in range(M):
            towers[(i, j)][2]=False

    return board,towers

# 입력 및 초기화
N,M,K=map(int,input().split())

board=[] # 격자판
towers={} # {(x,y)={ 공격력, 공격했던 시간 ,피해를 받았던 포탑인지:False }
plus_attack=N+M # 추가 공격력
answer=0 # 턴 종료 후 가장 강한 포탑의 공격력


for i in range(N):
    row=list(map(int,input().split()))
    for j in range(M):
        towers[(i,j)]=[row[j],0,False]
    board.append(row)

# print("init board: ",board)
# print("init towers: ",towers)
# print()

# 시뮬레이션 시작

for t in range(1,K+1):
    sx, sy, towers = find_weak(t, board, towers)
    ex, ey, towers = find_strong(t, board, towers)
    is_ok, board, towers = laser_attack(board, towers, sx, sy, ex, ey)
    if is_last(board):
        ex, ey, towers = find_strong(t, board, towers)
        print(towers[(ex, ey)][0])
        break
    # 레이저 공격이 가능한지 안한지 판단 공격이 가능하지않으면 폭격시작
    if not is_ok:
        board, towers = cannon_attack(board, towers, sx, sy, ex, ey)
        if is_last(board):
            ex, ey, towers = find_strong(t, board, towers)
            print(towers[(ex, ey)][0])
            break
    board, towers = recover(t, sx, sy, ex, ey, board, towers)

ex, ey, towers = find_strong(K, board, towers)
print(towers[(ex, ey)][0])

'''
NxM격자와 모든 위칭는 포탑이 존재 -> 포탑 개수 NM개

각 포탑에는 공격력이 존재, 상황에 따라 공격력이 왔다갔따.
공격력이 0이하기되면 해탕 포탑은 부서짐.(더이상 공격x) => 최초에 공격력이 0인 포탑존재 가능

하나의 턴은 4가지 액션을 순서대로 수행. K 번 반복
k 반복 중, 만약 부서지지 않은 포탑이 1개가 되면 그 즉시 중지

1.  공격자 선정
: 부서지지 않은 포탑(!=0) 중 가장 약한 포탑이 공격자로 선정
=> 공격자로 선정되면 가장 약한 포탑
=> N+M 공격력 증가

1.1. 약한 포탑 선정 기준
=> 공격력이 가장 낮은 포탑이 가장 약한 포탑임
=> 만약 공격력이 가장 낮은 포탑이 2개이상 이면, 가장 최근에 공격한 포탑이 가장 약함
=> => (모든 포탑은 시점 0에 모두 공격한 경험이 있다고 가정)
=> => 만약 그러한 포탑이 2개 이상이라면, 각 포탑 위치의 행과 열의 합이 가장 큰 포탑이 약함
=> => 만약 그러한 포탑이 2개 이상이면 각 포탑 위치의 열값이 가장 큰 포탑이 약함

2. 공격자의 공격
=> 자신을 제외한 가장 강한 포탑
1의 반대임
2.1.  만약 공격력이 가장 높은 포탑이 2개이상이라면 공격한지 가장 오래된 포탑이 가장 강함
(시점0에 모두 공격한 경험이 있음.)
=> 만약 그것도 같은면 행과 열 합이 가장 작은 포탑
=> 만약 그것도 같으면 열값이 가장 작은 포탑

2.2. 레이저 공격 먼저 시도
=> 상하좌우 4개 방향으로 이동
=>=> 부서진 포탑(0)이 있는 위치는 못지나감
=>=> 가장 자리에서 막히 방향으로 진행하면 반대편으로 나옴. (2,3)->(2,4)->(2,1)

=> 4방향 이동시 최단 경로로 이동(없으면 포탄 공격)
=>=> 최단경로 2개이상시 "우,하,좌,상" 우선순위대로 움직인 경로가 선택
=> 레이저 경로에 있는 포탑들은 공격자의 공격력의 절반만큼 깎이고, 공격대상은 공격력만큼 깎임

2.3. 포탄 공격
공격 대상에 포탄을 던짐
공격대상 주변 8개의 방향에 있는 포탑도 피해를 입음. (공격자의 절반(n//2) 만큼만 피해를 받음)
=> 공격자는 주위 8에 있어도 영향 x
만약 포탄이 떨어졌을 때, 주변 8에 반대편 격자도 포함해야함ㅋㅋ


3. 포탑 부서짐 처리 => 공격력 0임


4. 포탑 정비

4.1. 부서지지 않은 포탑 중 공격과 무관했던 포탑은 공격력이 1씩 올라감(공격자, 피해자x => 이전이랑 똑같네?)
턴 종료


4 4 1 =>N,M,K
0 1 4 4
8 0 10 13
8 0 11 26
0 0 0 0

'''