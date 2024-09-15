from collections import deque
from copy import deepcopy

# 3x3 구역을 회전시키는 함수
def rotate(board, center_x, center_y):
    """
    3x3 구역을 시계방향으로 90도 회전시키는 함수.
    :param board: 5x5 격자판
    :param center_x: 3x3 구역의 중심 x좌표
    :param center_y: 3x3 구역의 중심 y좌표
    :return: 회전이 적용된 새로운 보드
    """
    temp_board = deepcopy(board)  # 깊은 복사로 보드 상태를 유지
    sub_board = []

    # 3x3 구역 추출
    for i in range(center_x - 1, center_x + 2):
        row = board[i][center_y - 1:center_y + 2]
        sub_board.append(row)

    # 90도 회전 처리
    sub_board = [
        [sub_board[2][0], sub_board[1][0], sub_board[0][0]],
        [sub_board[2][1], sub_board[1][1], sub_board[0][1]],
        [sub_board[2][2], sub_board[1][2], sub_board[0][2]]
    ]

    # 회전한 구역을 다시 보드에 반영
    for i in range(3):
        for j in range(3):
            temp_board[center_x - 1 + i][center_y - 1 + j] = sub_board[i][j]

    return temp_board

# 유물을 탐색하고 제거한 후 점수를 계산하는 함수
def get_artifacts(board):
    total_score = 0
    visited = [[False] * 5 for _ in range(5)]  # 방문 여부
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]  # 상하좌우 탐색 방향

    # 보드의 모든 좌표 탐색
    for i in range(5):
        for j in range(5):
            if not visited[i][j] and board[i][j] != 0:  # 방문하지 않았고 유물이 있으면
                queue = deque([(i, j)])  # BFS 탐색을 위한 큐
                trace = deque([(i, j)])  # 연결된 유물 기록
                visited[i][j] = True

                while queue:
                    cur_y, cur_x = queue.popleft()
                    for k in range(4):  # 상하좌우 탐색
                        ny, nx = cur_y + dy[k], cur_x + dx[k]
                        if 0 <= ny < 5 and 0 <= nx < 5 and not visited[ny][nx] and board[ny][nx] == board[cur_y][cur_x]:
                            queue.append((ny, nx))
                            trace.append((ny, nx))
                            visited[ny][nx] = True

                # 3개 이상 연결된 유물 제거
                if len(trace) >= 3:
                    total_score += len(trace)  # 유물 개수만큼 점수 추가
                    for ty, tx in trace:
                        board[ty][tx] = 0  # 유물 제거

    return total_score

# 빈 칸에 벽면 유물로 채우는 함수
def fill_empty_spaces(board, wall_nums):
    for col in range(5):  # 열 순서대로
        for row in range(4, -1, -1):  # 아래에서 위로 빈 칸 채우기
            if board[row][col] == 0 and wall_nums:
                board[row][col] = wall_nums.popleft()  # 벽면 유물로 채움
    return board

# 입력 받기
K, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(5)]
wall_nums = deque(list(map(int, input().split())))

# 턴 진행
for turn in range(K):
    best_score = 0  # 이번 턴에서 얻을 수 있는 최대 점수
    best_rotated_board = None  # 최적의 회전 결과 보드

    # 3x3 구간을 선택하고 회전 각도에 따른 점수 계산
    for i in range(1, 4):  # 중심 좌표 (1,1) ~ (3,3)
        for j in range(1, 4):
            temp_board = deepcopy(board)  # 보드를 깊은 복사
            for k in range(3):  # 90도씩 3번 회전하여 점수 계산
                temp_board = rotate(temp_board, i, j)  # 회전
                score = get_artifacts(temp_board)  # 유물 점수 계산

                # 최대 점수를 얻는 구간 선택
                if score > best_score:
                    best_score = score
                    best_rotated_board = deepcopy(temp_board)  # 최대 점수일 때 보드 저장

    if best_rotated_board is None:  # 더 이상 유물이 없으면 종료
        break

    # 최적의 회전 결과를 보드에 적용
    board = best_rotated_board

    # 추가 유물 제거 및 빈 칸 채우기 반복
    while True:
        board = fill_empty_spaces(board, wall_nums)  # 빈 칸 채우기
        additional_score = get_artifacts(board)  # 추가 유물 획득
        if additional_score == 0:  # 더 이상 유물이 없으면 종료
            break
        best_score += additional_score  # 추가 점수 합산

    # 각 턴의 결과 출력
    print(best_score, end=" ")