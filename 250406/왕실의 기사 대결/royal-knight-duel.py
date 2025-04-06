# with open('test_case.txt','r') as file:
#     input_lines =[line.strip() for line in file]
# # input()을 다음줄에서부 읽어 오도록 하는 코드
# input=iter(input_lines).__next__ # __next__: 이터레이터에서 다음줄을 꺼내는 역할

# T=int(input())


def move(k_pos, k, d):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상 우 하 좌
    dx, dy = directions[d]
    (sx, sy), (ex, ey) = k_pos[k]
    nsx, nsy, nex, ney = sx + dx, sy + dy, ex + dx, ey + dy
    k_pos[k] = (nsx, nsy), (nex, ney)
    return k_pos


# 보드안에 있고, 벽이 아닌 경우
def is_ok(board, L, sx, sy, ex, ey):
    # 만약 하나라도 잘못되면 False
    if sx < 0 or sx >= L or sy < 0 or sy >= L or ex < 0 or ex >= L or ey < 0 or ey >= L:
        return False
    # 만약 보드안의 내용이 벽이면 False
    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            if board[x][y] == 2:
                return False
    return True


def is_knight(k_board, k, sx, sy, ex, ey):
    k_list = set()
    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            knight = k_board[x][y]
            # 자기 자신이 아니고
            if knight > 0 and knight != k:
                k_list.add(k_board[x][y])
    return list(k_list)  # 안의 기사들의 번호 집합


def update_k_board(L, k_pos):
    k_board = [[0] * L for _ in range(L)]

    for key, values in k_pos.items():
        (sx, sy), (ex, ey) = values
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                k_board[i][j] = key
    return k_board


# 해당 기사에 포함되어있는 함정의 수 찾는 함수
def find_bomb(k, k_pos):
    n = 0

    (sx, sy), (ex, ey) = k_pos[k]
    for i in range(sx, ex + 1):
        for j in range(sy, ey + 1):
            if board[i][j] == 1:
                n += 1
    return n


def minus(k_pos, k_board, knights, k, moved_k):
    deleted_list = []
    # 밀려난 기사들만 셈
    for key in moved_k:
        if key == k:
            continue
        if key not in k_pos:
            continue
        n= find_bomb(key, k_pos)
        knights[key][4] -= n
        # if n>0 and (key==6 or key==9):
        #     # print(str(key) +"가 받은 피해: "+str(n))
        if knights[key][4] <= 0:
            deleted_list.append(key)
            (sx, sy), (ex, ey) = k_pos[key]
            for i in range(sx, ex + 1):
                for j in range(sy, ey + 1):
                    k_board[i][j] = 0
            del k_pos[key]

    for key in deleted_list:
        del knights[key]

    return k_pos, k_board, knights


'''
18:40 종료

4 3 3
0 0 1 0
0 0 1 0
1 1 0 1
0 0 2 0
1 2 2 1 5
2 1 2 1 1
3 2 1 2 3
1 2
2 1
3 3


LXL 격자판에서 대결
1,1로 시작
각 칸은 빈칸, 함정, 벽으로 구성(체스판 밖도 벽)
각 초기위치 => r,c
각 기사는 r,c의 좌상단에 hxw 크기의 직사각형으로 있음.
체력은 각각 k이고, 마력으로 상대방을 밀쳐낼 수 있음.

1. 기사이동

1. 상하좌우로만 한칸씩 움직임.
2. 이동하는 위치에 기사 존재시 그 방향으로 한칸 밀려남.
3. 만약 그 옆에 또 기사가 있으면 또 연쇄적으로 한칸 밀려남
4. 만약 기사가 이동하려는 방향 끝에 벽이 있다면 모든 기사는 원상 복구
5. 체스판에 사라진 기사에게는 명령을 내려도 반응 x

4. 입력
L, N, Q
[LxL 체스판] =>0: 빈칸, 1: 함정, 2: 벽
[r,c,h,w,k] =>N개, 좌측 상단 꼭지점(r,c)로부터 h,w 의 직사각형, k라는 체력
[i,d] => i번 기사에게 d로 한칸 이동하라는 이동 (d: 0,1,2,3 => 상,우,하,좌)

'''
# for _ in range(T):
# 입력
L, N, Q = map(int, input().split())
# board=[[0]*L for _ in range(L)]
board = []
knights = {}  # 기사들
q_list = []  # 명령어 리스트

for _ in range(L):
    row = list(map(int, input().split()))
    board.append(row)

# 영역 표시 추가해야함
k_pos = {}
k_board = [[0] * L for _ in range(L)]
for i in range(N):
    r, c, h, w, k = list(map(int, input().split()))
    knights[i + 1] = [r, c, h, w, k]
    r, c = r - 1, c - 1
    er, ec = r + (h - 1), c + (w - 1)  # 시점
    k_pos[i + 1] = ((r, c), (er, ec))

    for x in range(r, er + 1):
        for y in range(c, ec + 1):
            k_board[x][y] = (i + 1)

# print("board:", board)  # 현재 함점, 벽의 상황
# print("k_pos: ", k_pos)  # 기사의 시점, 종점 직사각형
# print("k_board:, ", k_board)  # 기사위치를 마킹 있으면 기사번호 없으면 0
# print("knights: ", knights)  # 기사 정보
# print("q_list: ", q_list)  # 명령 집합

# 이동 함수
'''
1. 기사이동

1. 상하좌우로만 한칸씩 움직임.
2. 이동하는 위치에 기사 존재시 그 방향으로 한칸 밀려남.
3. 만약 그 옆에 또 기사가 있으면 또 연쇄적으로 한칸 밀려남
4. 만약 기사가 이동하려는 방향 끝에 벽이 있다면 모든 기사는 원상 복구
5. 체스판에 사라진 기사에게는 명령을 내려도 반응 x
'''

from copy import deepcopy
from collections import deque
# 시뮬레이션 시작
init_damages={}
for k in  knights:
    init_damages[k]=knights[k][4]

for i in range(Q):
    k, d = map(int, input().split())
    # print("===="+str(k)+"의 이동 방향:"+str(d)+"====")

    can_damage = True
    if k not in k_pos:
        continue

    init_pos = deepcopy(k_pos)
    k_pos = move(k_pos, k, d)
    moved_k = deque()  # 이동한 기사들을 넣음
    visited=set() # 움직였던 기사들을 넣음
    (sx, sy), (ex, ey) = k_pos[k]
    # 움직여도 괜찮으면
    if is_ok(board, L, sx, sy, ex, ey):
        # 다음 위치에 기사가 있냐?`
        moved_k.extend( is_knight(k_board, k, sx, sy, ex, ey))

        '''
        1. k_list의 기사 하나씩 이동
        2. 그 친구가 안괜찮아?
        3. 반복문 종료
        4. 괜찮으면 
        '''
        #

        while moved_k:

            knight = moved_k.popleft()

            if knight not in visited:
                visited.add(knight)
            else:
                continue
            # 이동 후 이동한 위치에 기사가 있으면 추가
            k_pos = move(k_pos, knight, d)
            (sx, sy), (ex, ey) = k_pos[knight]
            if is_ok(board, L, sx, sy, ex, ey):
                moved_k.extend( is_knight(k_board, knight, sx, sy, ex, ey))
        # print("전부다 이동 한 후k_pos: ",k_pos)

        # 체크 했는데 하나라도 잘못된 기사 있으면 원상복구
        for key, values in k_pos.items():
            (nsx, nsy), (nex, ney) = values
            if not is_ok(board, L, nsx, nsy, nex, ney):
                k_pos = deepcopy(init_pos)
                can_damage = False
    else:
        k_pos = move(k_pos, k, (d + 2) % 4)  # 반대로 다시 back
        can_damage = False
        continue
    #
    # print("before knights: ", knights)  # 기사 정보
    # print("before k_pos: ", k_pos)
    # print("before k_board:", k_board)
    # print("before knights: ", knights)  # 기사 정보
    # k_pos를 통한 k_board 갱신
    k_board = deepcopy(update_k_board(L, k_pos))
    # 체력 감소

    if can_damage:
        # 실제 움직였던 기사들만 확인
        actual_moved=[]
        for key in visited:
            # 초기 위치와 다른 기사들 => 움직인 기사들만 추적 + 명령받은 기사는 피해 받지 않음
            if k_pos[key] != init_pos[key] and key!=k:
                actual_moved.append(key)
        k_pos, k_board, knights = minus(k_pos, k_board, knights, k, actual_moved)
    # print()
    # print("after knights: ", knights)  # 기사 정보
    # print("after k_pos: ", k_pos)
    # print("after k_board:", k_board)
    # print("after knights: ", knights)  # 기사 정보
    # print()
total_damage=0
for k in  knights:
    total_damage+= init_damages[k]-knights[k][4]

print(total_damage)


