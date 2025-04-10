# with open('test_case.txt','r') as file:
#     input_lines=[line.strip() for line in file]
# input=iter(input_lines).__next__
# T=int(input())
from collections import deque

def is_last(board):
    return sum(1 for row in board for v in row if v > 0) == 1

def find_weak(t, board, towers):
    N, M = len(board), len(board[0])
    weak = []
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0:
                weak.append(towers[(i, j)] + [i, j])
    weak.sort(key=lambda x: (x[0], -x[1], -(x[3]+x[4]), -x[4]))
    sx, sy = weak[0][3], weak[0][4]
    towers[(sx, sy)][1] = t
    towers[(sx, sy)][0] += N + M
    board[sx][sy] += N + M
    return sx, sy, towers

def find_strong(sx, sy, board, towers, is_final=False):
    N, M = len(board), len(board[0])
    strong = []
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0 and (is_final or (i, j) != (sx, sy)):
                strong.append(towers[(i, j)] + [i, j])
    strong.sort(key=lambda x: (-x[0], x[1], x[3]+x[4], x[4]))
    return strong[0][3], strong[0][4], towers

def laser_attack(board, towers, sx, sy, ex, ey):
    N, M = len(board), len(board[0])
    q = deque([(sx, sy)])
    visited = [[False]*M for _ in range(N)]
    prev = [[None]*M for _ in range(N)]
    visited[sx][sy] = True
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    is_ok = False
    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            is_ok = True
            # continue
        for dx, dy in dirs:
            nx, ny = (x+dx)%N, (y+dy)%M
            if board[nx][ny] == 0 or visited[nx][ny]:
                continue
            visited[nx][ny] = True
            prev[nx][ny] = (x, y)
            q.append((nx, ny))

    if not is_ok:
        return False, board, towers

    path = []
    cx, cy = ex, ey
    while (cx, cy) != (sx, sy):
        path.append((cx, cy))
        cx, cy = prev[cx][cy]
    path.append((sx, sy))
    path.reverse()

    power = towers[(sx, sy)][0]
    for x, y in path:
        if (x, y) == (sx, sy):
            continue
        dmg = power if (x, y) == (ex, ey) else power // 2
        board[x][y] = max(0, board[x][y] - dmg)
        towers[(x, y)][0] = board[x][y]
        towers[(x, y)][2] = True
    return True, board, towers

def cannon_attack(board, towers, sx, sy, ex, ey):
    N, M = len(board), len(board[0])
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    power = board[sx][sy]

    for dx, dy in dirs:
        nx, ny = (ex+dx)%N, (ey+dy)%M
        if (nx, ny) == (sx, sy):
            continue
        board[nx][ny] = max(0, board[nx][ny] - power//2)
        towers[(nx, ny)][0] = board[nx][ny]
        towers[(nx, ny)][2] = True

    board[ex][ey] = max(0, board[ex][ey] - power)
    towers[(ex, ey)][0] = board[ex][ey]
    towers[(ex, ey)][2] = True
    return board, towers

def recover(t, sx, sy, ex, ey, board, towers):
    N, M = len(board), len(board[0])
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0 and (i, j) not in [(sx, sy), (ex, ey)] and not towers[(i, j)][2]:
                board[i][j] += 1
                towers[(i, j)][0] += 1
            towers[(i, j)][2] = False
    return board, towers

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
towers = {(i, j): [board[i][j], 0, False] for i in range(N) for j in range(M)}

for t in range(1, K+1):
    sx, sy, towers = find_weak(t, board, towers)
    ex, ey, towers = find_strong(sx, sy, board, towers)
    is_ok, board, towers = laser_attack(board, towers, sx, sy, ex, ey)
    if not is_ok:
        board, towers = cannon_attack(board, towers, sx, sy, ex, ey)
    if is_last(board):
        ex, ey, towers = find_strong(-1, -1, board, towers, is_final=True)
        print(towers[(ex, ey)][0])
        break
    board, towers = recover(t, sx, sy, ex, ey, board, towers)
else:
    ex, ey, towers = find_strong(-1, -1, board, towers, is_final=True)
    print(towers[(ex, ey)][0])
