from collections import deque
from copy import deepcopy

# 3x3 구역을 회전시키는 함수
def rotate(board, center_x, center_y, angle):
    """
    주어진 보드에서 3x3 구역을 시계방향으로 회전시키는 함수.
    :param board: 5x5 격자판 (리스트)
    :param center_x: 3x3 구역의 중심 x좌표
    :param center_y: 3x3 구역의 중심 y좌표
    :param angle: 회전 각도 (90, 180, 270도 중 하나)
    :return: 회전이 적용된 보드 (원본 보드는 손상되지 않음)
    """
    temp_board = deepcopy(board)  # 원본 보드를 손상시키지 않기 위해 깊은 복사
    subgrid = []  # 3x3 구역을 저장할 배열

    # 3x3 구역 추출
    for i in range(center_x - 1, center_x + 2):
        subgrid.append(board[i][center_y - 1:center_y + 2])

    # 각도에 따른 시계방향 회전 처리
    if angle == 90:
        subgrid = [
            [subgrid[2][0], subgrid[1][0], subgrid[0][0]],
            [subgrid[2][1], subgrid[1][1], subgrid[0][1]],
            [subgrid[2][2], subgrid[1][2], subgrid[0][2]]
        ]
    elif angle == 180:
        subgrid = [
            [subgrid[2][2], subgrid[2][1], subgrid[2][0]],
            [subgrid[1][2], subgrid[1][1], subgrid[1][0]],
            [subgrid[0][2], subgrid[0][1], subgrid[0][0]]
        ]
    elif angle == 270:
        subgrid = [
            [subgrid[0][2], subgrid[1][2], subgrid[2][2]],
            [subgrid[0][1], subgrid[1][1], subgrid[2][1]],
            [subgrid[0][0], subgrid[1][0], subgrid[2][0]]
        ]

    # 회전한 구역을 원본 보드에 다시 반영
    for i in range(3):
        for j in range(3):
            temp_board[center_x - 1 + i][center_y - 1 + j] = subgrid[i][j]

    return temp_board  # 회전이 적용된 새로운 보드 반환

# 유물을 탐색하고 점수를 계산하는 함수 (BFS 방식 사용)
def get_artifacts(board):
    """
    보드에서 상하좌우로 3개 이상 연결된 유물들을 찾아 제거하고, 점수를 계산하는 함수.
    :param board: 5x5 격자판
    :return: 총 획득한 유물 점수
    """
    score = 0  # 획득할 점수를 저장할 변수
    visited = [[False] * 5 for _ in range(5)]  # 방문 여부를 체크하는 배열
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]  # 상하좌우 탐색 방향 벡터

    # 5x5 보드의 모든 좌표를 탐색
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:  # 방문하지 않았고 유물이 있으면
                dq, trace = deque([(i, j)]), deque([(i, j)])  # BFS 탐색을 위한 큐
                visited[i][j] = True  # 현재 좌표 방문 처리

                # BFS 탐색으로 상하좌우로 같은 유물을 탐색
                while dq:
                    cur_y, cur_x = dq.popleft()
                    for d in range(4):  # 4방향 탐색
                        ny, nx = cur_y + dy[d], cur_x + dx[d]
                        if 0 <= ny < 5 and 0 <= nx < 5 and not visited[ny][nx] and board[ny][nx] == board[cur_y][cur_x]:
                            dq.append((ny, nx))
                            trace.append((ny, nx))
                            visited[ny][nx] = True  # 방문 처리

                # 3개 이상 연결된 유물 제거
                if len(trace) >= 3:
                    score += len(trace)  # 연결된 유물의 개수만큼 점수 추가
                    while trace:
                        t = trace.popleft()  # 연결된 유물들을 제거
                        board[t[0]][t[1]] = 0

    return score  # 총 획득한 점수를 반환

# 빈 칸에 벽면 유물로 채우는 함수
def fill_empty_spaces(board, wall_nums):
    """
    빈 칸에 벽면에서 가져온 유물들을 채우는 함수.
    :param board: 유물이 배치된 5x5 격자판
    :param wall_nums: 벽면에서 가져온 유물들의 리스트 (deque)
    :return: 빈칸이 채워진 보드
    """
    for col in range(5):  # 열을 기준으로 순차적으로 탐색
        for row in range(4, -1, -1):  # 각 열에서 아래에서 위로 탐색
            if board[row][col] == 0:  # 빈 칸이면
                board[row][col] = wall_nums.popleft()  # 벽면에서 유물 가져와 채우기
    return board

# 메인 로직

# 입력 받기
K, M = map(int, input().split())  # 턴 횟수 K와 벽면 유물 개수 M 입력 받기
board = [list(map(int, input().split())) for _ in range(5)]  # 5x5 보드 상태 입력
wall_nums = deque(list(map(int, input().split())))  # 벽면에서 가져올 유물 번호 입력

# 턴을 진행
for turn in range(K):  # 총 K번의 턴을 진행
    best_score = 0  # 이번 턴에서 얻을 수 있는 최대 점수를 저장할 변수
    best_rotated_board = None  # 최적의 회전 결과를 저장할 보드 (초기값은 None)

    # 3x3 구역을 선택하고 회전 각도에 따른 점수 계산
    for angle in [90, 180, 270]:  # 90도, 180도, 270도의 세 가지 회전 각도를 시도
        for i in range(1, 4):  # 3x3 구역의 중심 x좌표 (1, 2, 3)
            for j in range(1, 4):  # 3x3 구역의 중심 y좌표 (1, 2, 3)
                # 각 중심 좌표 별로 회전을 수행하고, 회전 결과 보드를 반환
                temp_board = rotate(board, i, j, angle)  # 중심 좌표 (i, j)에서 주어진 각도로 회전

                # 회전된 보드에서 유물 점수 계산
                score = get_artifacts(temp_board)  # BFS를 사용해 3개 이상 연결된 유물을 찾아 제거하고 점수 계산

                # 현재까지의 최대 점수와 비교하여 더 높은 점수를 가진 보드를 저장
                if score > best_score:
                    best_score = score  # 최대 점수 갱신
                    best_rotated_board = deepcopy(temp_board)  # 최적의 보드를 깊은 복사하여 저장

    # 만약 최적의 회전 결과가 없으면 (즉, 회전 후 얻을 유물이 없으면) 탐사를 종료
    if best_rotated_board is None:
        break  # 더 이상 탐사가 불가능하면 루프 종료

    # 최적의 회전 결과를 원본 보드에 적용
    board = best_rotated_board

    # 추가적으로 빈 칸을 채우고, 새로운 유물 점수를 계산하는 과정
    while True:
        board = fill_empty_spaces(board, wall_nums)  # 빈 칸을 벽면 유물로 채움
        additional_score = get_artifacts(board)  # 새로 채워진 보드에서 추가 유물을 탐색하고 점수 계산

        # 더 이상 유물이 없으면 종료 (유물이 연결되지 않으면 탐사 종료)
        if additional_score == 0:
            break

        # 추가로 획득한 점수를 기존 점수에 합산
        best_score += additional_score

        # 이번 턴의 결과(최종 점수)를 출력 (space로 구분해 출력)
    print(best_score, end=" ")