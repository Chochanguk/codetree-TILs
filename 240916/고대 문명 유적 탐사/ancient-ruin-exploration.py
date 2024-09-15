from collections import deque
from copy import deepcopy


# 3x3 구역을 회전시키는 함수
def rotate(board, center_x, center_y):
    # temp_board = [row[:] for row in board] # 2차원 배열 깊은 복사
    temp_board=deepcopy(board)
    sub_board = []

    for i in range(center_x - 1, center_x + 2):
        row = board[i][center_y - 1:center_y + 2]
        sub_board.append(row)

    # 90도 회전
    sub_board = [
        [sub_board[2][0], sub_board[1][0], sub_board[0][0]],
        [sub_board[2][1], sub_board[1][1], sub_board[0][1]],
        [sub_board[2][2], sub_board[1][2], sub_board[0][2]]
    ]

    for i in range(3):
        for j in range(3):
            temp_board[center_x - 1 + i][center_y - 1 + j] = sub_board[i][j]

    return temp_board


# 유물을 탐색하고 점수를 계산하는 함수
def get_artifacts(board):
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
                    for d in range(4):
                        ny, nx = cur[0] + dy[d], cur[1] + dx[d]
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

# 빈 칸에 벽면 유물로 채우는 함수
def fill_empty_spaces(board, wall_nums):
    for col in range(5):  # 열 순서대로
        for row in range(4, -1, -1):  # 아래에서 위로 빈 칸 채우기
            if board[row][col] == 0:
                board[row][col] = wall_nums.popleft()  # 벽면에서 가져온 유물로 채움
    return board


# 입력 받기
K, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(5)]
wall_nums = deque(list(map(int, input().split())))

# 턴을 진행
for turn in range(K):
    best_score = 0
    best_rotated_board = None

    # 3x3 구간을 선택하고 회전 각도에 따른 점수 계산
    for i in range(1, 4):
        for j in range(1, 4):
            # 각 중심 좌표 별로 한번씩 돌려서 값을 구함
            temp_board = deepcopy(board)
            for k in range(3):
                temp_board = rotate(board, i, j)  # 돌림
                score = get_artifacts(temp_board)

                # 최대 점수를 얻는 구간을 선택
                if score > best_score:
                    best_score = score
                    best_rotated_board = temp_board

    if best_rotated_board is None:  # 더 이상 유물이 없으면 종료
        break

    board = best_rotated_board  # 최적의 회전 결과를 보드에 적용
    while True:
        board = fill_empty_spaces(board, wall_nums)  # 빈 칸을 채움
        additional_score = get_artifacts(board)  # 추가 유물 획득
        if additional_score == 0:  # 더 이상 유물이 없으면 종료
            break
        best_score += additional_score  # 추가 점수 합산

    print(best_score, end=" ")  # 각 턴의 결과 출력