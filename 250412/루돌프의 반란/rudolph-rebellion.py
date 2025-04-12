# with open('test_case.txt','r') as file:
#     input_lines=[line.strip() for line in file]
# input=iter(input_lines).__next__

# T=int(input())

from collections import deque

N, M, P, C, D = map(int, input().split())  # 격자판 및 정보
rx, ry = map(int, input().split())  # 루돌프 위치
santas = {} # 산타 번호 (x(0),y(1),기절 시각(2), 탈락 유무(3), 루돌프와 거리(4), 점수(5))
rudols={} # -1

board=[[0]*N for _  in range(N)]
for i in range(P):
    n, sx, sy = map(int, input().split())
    santas[n] = [sx-1, sy-1,-1,False,0,0]
    board[sx-1][sy-1]=n
rx,ry=rx-1,ry-1
rudols[-1]=(rx,ry) # 처음산타와 루돌프는 안겹침
board[rx][ry]=-1
# 거리 계산
def cal_dis(sx,sy,ex,ey):
    dis= (sx-ex)**2+(sy-ey)**2
    return dis # 거리반환
# 매턴 종료 후 값 갱신
def update_dis(rx,ry,santas):
    # 산타들의 루돌프와의 현재 거리

    for santa,v in santas.items():
        sx,sy=v[0],v[1]
        dis=cal_dis(sx,sy,rx,ry)
        santas[santa][4]=dis

    return santas

def find_santa(ex,ey,santas):
    n=0
    for k,v in santas.items():
        sx,sy=v[0],v[1]
        if (sx,sy)==(ex,ey)and not v[3]:  # 탈락 안한 산타만 찾기
            n=k
            break
    return n

def update_board(N, rudols, santas):
    board = [[0] * N for _ in range(N)]
    rx, ry = rudols[-1]
    board[rx][ry] = -1
    for k, v in santas.items():
        if v[3]: continue
        sx, sy = v[0], v[1]
        board[sx][sy] = k
    return board

# 연쇄작용
def contract(N, santa, santas, dx, dy):
    q = deque()
    q.append(santa)

    while q:
        cur = q.popleft()
        x, y = santas[cur][0], santas[cur][1]

        # 이동 전에 해당 위치 산타 번호 저장
        prev = board[x][y]

        nx, ny = x + dx, y + dy # 한칸 이동

        # 격자 밖으로 나가면 탈락
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            santas[cur][3] = True
            continue

        # 현재 산타 이동 처리
        santas[cur][0], santas[cur][1] = nx, ny

        # 만약 다른 산타가 있었다면 연쇄 처리
        if board[nx][ny] != 0:
            q.append(board[nx][ny])

    return santas



def rudolph_crash(C, t, dx, dy, rudols, santas, board):
    # 일단 겹치는게 있는지 찾아보기
    N = len(board)
    rx, ry = rudols[-1]

    temp_s = 0  # 산타가 아니면 0
    c_sanat=-1
    # print(santas)
    for k, v in santas.items():
        sx, sy = v[0], v[1]
        if (sx, sy) == (rx, ry) and not v[3]:
            c_santa=find_santa(sx, sy,santas)
            # 밀려난 산타에 대한 정보 업데이트
            santas[k][5] += C  # 점수 얻음
            santas[k][2] = t  # 기절 시각 체크

            nsx, nsy = sx + (dx * C), sy + (dy * C)
            # 해당 좌표의 산타를 찾고,
            temp_s = find_santa(nsx, nsy,santas)
            # 격자 밖에 있으면 탈락
            if nsx < 0 or nsx >= N or nsy < 0 or nsy >= N:
                santas[k][3] = True
            else:
                # 현재 산타 값 갱신
                santas[k][0], santas[k][1] = nsx, nsy  # 위치변경

            break
    # 만약 부딪힌 산타가 있으면?
    if temp_s != 0 and temp_s!=c_santa:
        santas = contract(N, temp_s, santas, dx, dy)

    # 충돌 및 연쇄 상호 작업 후에 rudols와 sants로 board 재마킹
    board=update_board(N, rudols, santas)
    # board = [[0] * N for _ in range(N)]
    # board[rx][ry] = -1
    # for k, v in santas.items():
    #     if v[3]:  # 탈락한 산타 패스
    #         continue
    #     sx, sy = v[0], v[1]
    #     if 0 <= sx < N and 0 <= sy < N:
    #         board[sx][sy] = k
    return board, rudols, santas



# 루돌프의 움직임
def r_move(t, rudols,santas):
    rx,ry=rudols[-1]

    # 이동한 곳이 산타랑 가장
    min_dis_list = []  # 루돌프와 산타 중 거리가 가장 가까운 리스트 모음
    for santa, v in santas.items():
        if v[3]:  # 탈락
            continue
        min_dis_list.append([santa] + v)
    # 탈락하지 않았고, 거리가 가까우면서, r,c가 큰것
    min_dis_list.sort(key=lambda x: (x[4], x[5], -x[1], -x[2]))
    # print(min_dis_list)
    n, ex, ey = min_dis_list[0][0], min_dis_list[0][1], min_dis_list[0][2]

    # 루돌프가 해당 방향으로 움직임
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    # 선택한 산타랑 가까운 방향으로 이동
    dx,dy=ex-rx,ey-ry

    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    rnx,rny=rx+dx,ry+dy

    rudols[-1]=(rnx,rny)

    return rudols,dx,dy


def s_move(t, N, rudols, santas, board):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상 우 하 좌
    rx, ry = rudols[-1]

    for k, v in santas.items():
        if t <= santas[k][2] + 1 or santas[k][3]:  # 기절 or 탈락
            continue

        sx, sy = v[0], v[1]
        dis_list = []

        for i, (dx, dy) in enumerate(directions):
            nx, ny = sx + dx, sy + dy
            if nx < 0 or nx >= N or ny < 0 or ny >= N: continue
            if board[nx][ny] >= 1: continue

            dis1 = cal_dis(nx, ny, rx, ry)
            dis2 = cal_dis(sx, sy, rx, ry)
            if dis1 >= dis2: continue

            dis_list.append((i, dis1))

        dis_list.sort(key=lambda x: (x[1], x[0]))  # 거리 짧고, 상우하좌

        if dis_list:
            d = dis_list[0][0]
            dx, dy = directions[d]
            nx, ny = sx + dx, sy + dy
            santas[k][0], santas[k][1] = nx, ny
            # 루돌프랑 충돌?
            if (nx, ny) == (rx, ry) and not v[3]:
                santas[k][5] += D
                santas[k][2] = t

                # 반대 방향으로 D만큼 밀기
                dx, dy = -dx, -dy
                nsx, nsy = nx + dx * D, ny + dy * D
                if nsx < 0 or nsx >= N or nsy < 0 or nsy >= N:
                    santas[k][3] = True

                # 다른 산타 있다면 연쇄작용
                another_s = find_santa(nsx, nsy, santas) # 다른 산타 찾고

                santas[k][0], santas[k][1] = nsx, nsy # 값 갱신

                if another_s != 0 and not santas[another_s][3]:
                    santas = contract(N, another_s, santas, dx, dy)

        # 매 산타 이동 후 board 갱신
        board=update_board(N, rudols, santas)
    return rudols, santas, board


# 게임종료인가
def is_end(santas):
    for k, v in santas.items():
        if not v[3]:  # 탈락 안한 산타 1명이라도 존재하면 계속 진행
            return False
    return True

# 산타 점수 출력하기
def print_score(santas):
    for k in santas:
        print(santas[k][5],end=' ')
    return

def plus_score(santas):
    for k, v in santas.items():
        # 살아남은 경우에 값 갱신
        if v[3]==False:
            santas[k][5]+=1
    return santas

is_over=False

# 산타 딕셔너리 정렬 처리
new_santas = {}
for k in sorted(santas.keys()):
    new_santas[k] = santas[k]
santas = new_santas


for t in range(1,M+1):

    rx,ry=rudols[-1]
    santas=update_dis(rx, ry, santas)
    # print("==========="+str(t)+"===========")
    # print("초기 rudols: ", rudols)
    # print("초기 santas:", santas)  # 산타들의 정보
    # print("초기 board:", board)
    # print()

    # 1. 루돌프 움직임
    rudols, dx, dy = r_move(t, rudols, santas)
    # 2. 루돌프의 충돌시
    board, rudols, santas = rudolph_crash(C, t, dx, dy, rudols, santas, board)
    # print("루돌프 이동 후 rudols:", rudols)
    # print("루돌프 충돌 후 santas:",santas)
    if is_end(santas):
        # print("루돌프 충돌로 인한 끝")
        print_score(santas)
        is_over=True
        break

    # 3. 산타의 움직임
    rudols, santas, board = s_move(t, N, rudols, santas, board)
    # print("산타 움직인 후 santas:", santas)
    if is_end(santas):
        # print("산타 충돌로 인한 끝")
        print_score(santas)
        is_over = True
        break
    # 4.
    santas=plus_score(santas)
    # print("after rudols: ", rudols)
    # print("after santas:", santas)  # 산타들의 정보
    # print()

if not is_over:
    print_score(santas)

