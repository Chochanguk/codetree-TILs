# # 입력 및 초기화
# with open ('test_case.txt','r') as file:
#     input_lines=[line.strip() for line in file]
# input=iter(input_lines).__next__
#
#
# T=int(input())

# 이동 함수
def find_d(sx,sy,exit_x,exit_y):
    dx=exit_x-sx
    dy=exit_y-sy
    # 먼저 나오는거 찾음
    if dx>0:
        return 0
    elif dx<0:
        return 1
    elif dy > 0:
        return 2
    elif dy < 0:
        return 3
def find_distance(sx,sy,ex,ey):
    return abs(sx-ex)+abs(sy-ey)

def move(N,board,runner):
    cnt=0 # 총 움직인 거리 수
    # 바뀐 좌표와 러너들의 위치 변경
    to_delete = []
    exit_x, exit_y =runner[-1]
    #1. runner를 먼저 수정후에
    for r,v in runner.items():
        # 만약 탈출구라면 러너만 탐색
        if r==-1:
            continue

        # 만약 도달했으면 runner는 없앰
        sx, sy, _ = v
        d=find_d(sx,sy,exit_x,exit_y)

        dx,dy=directions[d]
        nx,ny=sx+dx,sy+dy
        # 빈칸인 경우에만 이동
        if 0<=nx<N and 0<=ny<N and board[nx][ny]==0:
            cnt+=1
            runner[r]=(nx,ny,d)
            # 만약 도달했으면 runner는 없앰=
            if (nx, ny) == (exit_x, exit_y):
                to_delete.append(r)
            # 다음 러너 탐색
            continue
        # 빈칸이 아니면 다른 방향도 고려.
        for i,(dx,dy) in enumerate(directions):
            # 찾은 방향이랑 다르면
            if i == d:
                continue
            ax, ay = sx + dx, sy + dy
            if 0 <= ax < N and 0 <= ay < N and board[ax][ay] == 0:
                if find_distance(ax, ay, exit_x, exit_y) < find_distance(sx, sy, exit_x, exit_y):
                    cnt += 1
                    runner[r] = (ax, ay, i)  #  i로 방향 업데이트

    for r in to_delete:
        del runner[r]
    return runner,cnt #러너와 이동 거리 반환


# 돌릴 시점,종료으로 보드판을 돌려 board, exit, runner를 반환
def right_rotate(sx, sy, ex, ey, board, runner):
    M = ex - sx + 1  # 정사각형 한 변 길이

    # 1. 회전된 board 만들기
    temp = []
    for j in range(sy, ey+1):
        row = []
        for i in range(ex, sx-1, -1):
            val = board[i][j]
            if val>=1:
                row.append(val-1)
            else:
                row.append(val)
        temp.append(row)

    # 2. 원본 board에 회전된 값 덮어쓰기
    for i in range(sx, ex + 1):
        for j in range(sy, ey + 1):
            board[i][j] = temp[i - sx][j - sy]

    # 3. 러너들 좌표 회전
    new_runner = {}
    for r, v in runner.items():
        if r == -1:
            x, y = v
        else:
            x, y, d = v

        if sx <= x <= ex and sy <= y <= ey:
            # 회전 공식 적용
            new_x = sx + (y - sy)
            new_y = ey - (x - sx)
            if r == -1:
                new_runner[-1] = (new_x, new_y)
            else:
                new_runner[r] = (new_x, new_y, d)
        else:
            # 회전 영역 바깥은 그대로 유지
            new_runner[r] = v

    exit_x, exit_y = new_runner[-1]
    return board, new_runner, exit_x, exit_y


def find_square(n,runner, exit_x, exit_y):
    max_n = n  # 최대 격자 크기 (문제 조건에 따라 다르게 조정)

    for size in range(2, max_n + 1):  #정사각형 크기: 2x2부터 시작
        for sx in range(0, max_n - size + 1):
            for sy in range(0, max_n - size + 1):
                ex, ey = sx + size - 1, sy + size - 1

                # 출구가 정사각형 안에 없으면 스킵
                if not (sx <= exit_x <= ex and sy <= exit_y <= ey):
                    continue

                found_runner = False
                for r, v in runner.items():
                    if r == -1:
                        continue  # 출구는 패스
                    rx, ry, _ = v
                    # 출구에 있는 러너는 제외
                    if rx == exit_x and ry == exit_y:
                        continue
                    if sx <= rx <= ex and sy <= ry <= ey:
                        found_runner = True
                        break

                if found_runner:
                    min_square = (sx, sy, ex, ey)  #  ex, ey 그대로 반환
                    return min_square

    return 0, 0, max_n-1, max_n-1


N,M,K=map(int,input().split())
board=[]
runner={}# 탈출자 위치

for i in range(N):
    row=list(map(int,input().split()))
    board.append(row)

# 방향 (남,북,동,서), (0,1,2,3)
directions=[(1,0),(-1,0),(0,1),(0,-1)]

for i in range(M):
    r,c=map(int, input().split())
    runner[i]=(r-1,c-1,-1)
# 출구 좌표와 총 이동거리
exit_x,exit_y=map(int, input().split())
exit_x,exit_y=exit_x-1,exit_y-1
runner[-1]=(exit_x,exit_y)
answer=0

# 초기 러너들 방향 잡기
for r,v in runner.items():
    sx,sy=v[0],v[1]
    d=find_d(sx,sy,exit_x,exit_y)
    if r>=0:
        runner[r]=(sx,sy,d)
# print()
# print("init board:",board)
# print("init runner: ",runner)
# print()


for t in range(K):
    runner,moved =move(N,board, runner)
    answer += moved
    if len(runner) == 1:
        break  # 모두 탈출했으면 시뮬레이션 종료
    sx,sy,ex,ey=find_square(N,runner,exit_x,exit_y)
    board, runner, exit_x, exit_y = right_rotate(sx,sy,ex,ey, board, runner)
    # print("현재시각: ",t+1,"초")
    # print()
    # print("선택된 정사각형 좌표:",sx,sy,ex,ey)
    # print("after board:", board)
    # print("after runner: ", runner)
    # print("answer:", answer)
    # print("탈출 좌표: ", exit_x, exit_y)
    # print()

print(answer)
print(exit_x+1,exit_y+1)


