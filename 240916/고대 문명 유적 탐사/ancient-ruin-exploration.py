from collections import deque
from copy import deepcopy


def rotate(sy, sx, cnt):
    result = deepcopy(board)
    for _ in range(cnt):
        tmp = result[sy + 0][sx + 2]
        result[sy + 0][sx + 2] = result[sy + 0][sx + 0]
        result[sy + 0][sx + 0] = result[sy + 2][sx + 0]
        result[sy + 2][sx + 0] = result[sy + 2][sx + 2]
        result[sy + 2][sx + 2] = tmp
        tmp = result[sy + 1][sx + 2]
        result[sy + 1][sx + 2] = result[sy + 0][sx + 1]
        result[sy + 0][sx + 1] = result[sy + 1][sx + 0]
        result[sy + 1][sx + 0] = result[sy + 2][sx + 1]
        result[sy + 2][sx + 1] = tmp
    return result


def cal_score(board):
    score = 0
    # 방문여부 체크
    visit = [[False] * 5 for _ in range(5)]
    # BFS 방향
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]

    for i in range(5):
        for j in range(5):
            if not visit[i][j]:
                dq, trace = deque([(i, j)]), deque([(i, j)])
                visit[i][j] = True
                while dq:
                    cur = dq.popleft()
                    for k in range(4):
                        ny, nx = cur[0] + dy[k], cur[1] + dx[k]
                        if 0 <= ny < 5 and 0 <= nx < 5 and visit[ny][nx] == False and board[ny][nx] == board[cur[0]][
                            cur[1]]:
                            dq.append((ny, nx))
                            trace.append([ny, nx])
                            visit[ny][nx] = True
                if len(trace) >= 3:
                    score += len(trace)
                    while trace:
                        t = trace.popleft()
                        board[t[0]][t[1]] = 0
    return score


def fill(b, qq):
    for j in range(5):
        for i in range(4, -1, -1):
            if b[i][j] == 0:
                b[i][j] = qq.popleft()
    return b


K, M = map(int, input().split())
board = []
for i in range(5):
    board.append(list(map(int, input().split())))
M_list = list(map(int, input().split()))
M_list = deque(M_list)

for _ in range(K):
    maxScore = 0
    maxScoreBoard = None
    for cnt in range(1, 4):
        for j in range(3):
            for i in range(3):
                rotated = rotate(i, j, cnt)
                score = cal_score(rotated)
                if maxScore < score:
                    maxScore = score
                    maxScoreBoard = rotated
    if maxScoreBoard is None:
        break
    board = maxScoreBoard
    while True:
        board = fill(board, M_list)
        newScore = cal_score(board)
        if newScore == 0:
            break
        maxScore += newScore

    print(maxScore, end=" ")