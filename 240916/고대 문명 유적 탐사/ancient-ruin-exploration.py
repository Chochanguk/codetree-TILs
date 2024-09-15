from collections import deque
from copy import deepcopy

# 3x3 구역을 회전시키는 함수
def rotate(board, center_x, center_y):
    """
    주어진 5x5 격자에서 3x3 구역을 시계방향으로 90도 회전시키는 함수.
    :param board: 5x5 격자판 (리스트)
    :param center_x: 3x3 구역의 중심 x좌표
    :param center_y: 3x3 구역의 중심 y좌표
    :return: 회전이 적용된 새로운 보드 (deepcopy로 원본은 유지)
    """
    # deepcopy를 사용하여 보드를 복사하여 원본 데이터를 보존
    temp_board = deepcopy(board)
    sub_board = []

    # 3x3 구역을 추출하여 리스트에 저장
    for i in range(center_x - 1, center_x + 2):
        row = board[i][center_y - 1:center_y + 2]
        sub_board.append(row)

    # 시계 방향 90도 회전
    sub_board = [
        [sub_board[2][0], sub_board[1][0], sub_board[0][0]],
        [sub_board[2][1], sub_board[1][1], sub_board[0][1]],
        [sub_board[2][2], sub_board[1][2], sub_board[0][2]]
    ]

    # 회전한 3x3 구역을 temp_board에 다시 적용
    for i in range(3):
        for j in range(3):
            temp_board[center_x - 1 + i][center_y - 1 + j] = sub_board[i][j]

    return temp_board

# 유물을 탐색하고 점수를 계산하는 함수
def get_artifacts(board):
    """
    격자에서 상하좌우로 3개 이상 연결된 유물을 찾아 제거하고 점수를 계산하는 함수.
    :param board: 유물들이 배치된 5x5 격자판 (리스트)
    :return: 총 획득한 유물 점수
    """
    total_score = 0  # 총 점수
    visited = [[False] * 5 for _ in range(5)]  # 방문 여부를 저장하는 2차원 리스트
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]  # 상하좌우 이동을 위한 방향 리스트

    # 보드의 모든 좌표를 탐색
    for i in range(5):
        for j in range(5):
            if not visited[i][j] and board[i][j] != 0:  # 방문하지 않았고 유물이 있는 경우
                queue = deque([(i, j)])  # 탐색을 위한 큐
                trace = deque([(i, j)])  # 연결된 유물을 저장할 리스트
                visited[i][j] = True  # 현재 위치 방문 처리

                # BFS를 사용하여 상하좌우로 같은 유물 찾기
                while queue:
                    cur_y, cur_x = queue.popleft()
                    for k in range(4):
                        ny, nx = cur_y + dy[k], cur_x + dx[k]
                        if 0 <= ny < 5 and 0 <= nx < 5 and not visited[ny][nx] and board[ny][nx] == board[cur_y][cur_x]:
                            queue.append((ny, nx))
                            trace.append((ny, nx))
                            visited[ny][nx] = True

                # 3개 이상의 유물이 연결되었으면 유물 제거 및 점수 추가
                if len(trace) >= 3:
                    total_score += len(trace)  # 유물의 개수만큼 점수 추가
                    for ty, tx in trace:
                        board[ty][tx] = 0  # 유물 제거 (0으로 설정)

    return total_score  # 총 획득한 점수 반환

# 빈 칸에 벽면 유물로 채우는 함수
def fill_empty_spaces(board, wall_nums):
    """
    빈 칸(0) 자리에 벽면 유물을 채우는 함수. 열이 작은 순서대로, 같은 열이면 아래에서 위로 채움.
    :param board: 유물들이 배치된 5x5 격자판 (리스트)
    :param wall_nums: 벽면에서 제공된 유물들의 번호 리스트 (deque)
    :return: 채워진 격자판
    """
    for col in range(5):  # 열 순서대로 채움
        for row in range(4, -1, -1):  # 아래에서 위로 빈 칸을 탐색
            if board[row][col] == 0:  # 빈 칸이면 벽면 유물로 채움
                board[row][col] = wall_nums.popleft()  # 벽면에서 유물 번호를 가져와 채움
    return board

# 입력 받기
K, M = map(int, input().split())  # 탐사 횟수 K와 벽면 유물의 개수 M 입력 받기
board = [list(map(int, input().split())) for _ in range(5)]  # 5x5 보드 입력 받기
wall_nums = deque(list(map(int, input().split())))  # 벽면 유물 번호를 입력 받아 deque로 저장

# 턴을 진행
for turn in range(K):
    best_score = 0  # 이번 턴에서 얻을 수 있는 최대 점수
    best_rotated_board = None  # 최적의 회전 결과를 저장할 보드

    # 3x3 구간을 선택하고 회전 각도에 따른 점수 계산
    for i in range(1, 4):  # 중심 좌표는 (1,1) ~ (3,3)에서 가능
        for j in range(1, 4):
            temp_board = deepcopy(board)  # 보드의 깊은 복사
            for k in range(3):  # 90도씩 3번 회전하여 각 경우의 점수 계산
                temp_board = rotate(board, i, j)  # 3x3 구간을 회전
                score = get_artifacts(temp_board)  # 회전 후 유물 점수 계산

                # 최대 점수를 얻는 구간을 선택
                if score > best_score:
                    best_score = score
                    best_rotated_board = temp_board

    if best_rotated_board is None:  # 더 이상 유물이 없으면 종료
        break

    # 최적의 회전 결과를 보드에 적용
    board = best_rotated_board

    # 추가적으로 빈 칸을 채우고 유물을 연속해서 제거
    while True:
        board = fill_empty_spaces(board, wall_nums)  # 빈 칸을 채움
        additional_score = get_artifacts(board)  # 추가 유물 획득
        if additional_score == 0:  # 더 이상 유물이 없으면 종료
            break
        best_score += additional_score  # 추가 점수 합산

    # 각 턴의 결과 출력
    print(best_score, end=" ")