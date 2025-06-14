from collections import deque

directions=[(1,0),(-1,0),(0,1),(0,-1)]

def bfs(x, y, visited, board):

    score = 0
    sames = []  # 3개이상 집합인 것들

    num = board[x][y]
    q = deque()

    q.append((x, y))
    visited[x][y] = True
    sames.append([x,y])

    while q:
        cx, cy = q.popleft()

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < 5 and 0 <= ny < 5 and board[nx][ny] == num and not visited[nx][ny]:
                q.append((nx, ny))
                visited[nx][ny] = True
                sames.append([nx, ny])
    # 3개 이상인 경우만
    if len(sames) >= 3:
        return len(sames), sames
    else:
        return 0, []

# 결과
def search(board):
    result=0
    dis_appealed=[] # 사라질 좌표들 모음(3개 이상인 녀석들)

    visited=[[False]*5 for _ in range(5)]

    for i in range(5):
        for j in range(5):
            # 방문한 적 없으면
            if not visited[i][j]:
                score, three_set = bfs(i, j, visited, board)
                result+=score
                dis_appealed.extend(three_set)

    dis_appealed.sort(key=lambda x: (x[1], - x[0])) # 열이작고, 행이 큰 순
    #
    # print("=== 결과 ===")
    # print(board)
    # print(result)
    # print(dis_appealed)

    return result, dis_appealed

from copy import deepcopy

def copy_board(x,y, board,new_board):
    for i in range(3):
        for j in range(3):
            board[i + x - 1][j + y - 1] = new_board[i][j]

    return board

def r_90(x,y,board):
    new_board=[]
    for j in range(y-1,y+2):
        row=[]
        for i in range(x+1,x-2,-1):
            row.append(board[i][j])
        new_board.append(row)

    board=copy_board(x,y, board,new_board)

    return board

def r_180(x,y,board):
    new_board = []
    for i in range(x + 1, x - 2, -1):
        row=[]
        for j in range(y+1,y-2,-1):
            row.append(board[i][j])
        new_board.append(row)

    board = copy_board(x, y, board, new_board)

    return board

def r_270(x,y,board):

    new_board = []
    for j in range(y + 1, y - 2, -1):
        row = []
        for i in range(x - 1, x + 2):
            row.append(board[i][j])
        new_board.append(row)

    board = copy_board(x, y, board, new_board)

    return board

# board = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
# print(board)
# r_270(1, 1, board)
# print(board)

def first_gain(board):
    original = deepcopy(board)
    result=[] # [-점수, 회전각, y, x ]
    total_score = 0
    finded=[]

    for x in range(1,4):
        for y in range(1,4):
            # 90도 회전
            # 1. 회전
            board=r_90(x,y,board)
            # 2. 탐색
            total_score,finded=search(board)
            # 3. 결과 삽입
            result.append([total_score,90,x,y,finded,board])
            board=deepcopy(original)

            # 180도 회전
            # 1. 회전
            board = r_180(x, y, board)
            # 2. 탐색
            total_score,finded=search(board)
            # 3.
            result.append([total_score,180,x,y,finded,board])
            board = deepcopy(original)

            # 270 도 회전
            # 1. 회전
            board = r_270(x, y, board)
            # 2. 탐색
            total_score,finded=search(board)
            # 3. 결과 삽입
            result.append([total_score,270,x,y,finded,board])
            board = deepcopy(original)

    result.sort(key=lambda x: (-x[0],x[1], x[3],x[2])) # 점수 높고, 회전각 작고, 열이 작고, 행이 작고

    return result[0][0],result[0][4],result[0][5] # 회전 후 최대 점수

# 격자판에 넣기
def add(board,waits,finded):

    for x,y in finded:
        num=waits.popleft() # waits는 부족하지 않게 넉넉함
        board[x][y]=num

    return board,waits

# board=[[7, 6, 7, 6, 7], [6, 6, 7, 7, 6], [6, 3, 1, 6, 4], [7, 2, 5, 7, 1], [5, 4, 3, 2, 7]]
# finded=[[2, 0], [1, 0], [1, 1], [0, 1], [1, 2], [0, 2], [1, 3]]
# q=[3, 2, 3, 5, 2, 4, 6, 1, 3, 2, 5, 6, 2, 1, 5, 6, 7, 1, 2, 3]
# waits=deque(q)
# board, waits = add(board,waits,finded)
#
# print()
# print(board)
# print(waits)

def print_answer(answer):

    for n in answer:
        if n!=0:
            print(n, end=' ')

from collections import deque



answer=[]
K,M=map(int,input().split())

board=[] #격자판
for i in range(5):
    row=list(map(int,input().split()))
    board.append(row)
arr=list(map(int,input().split()))
waits=deque(arr)


# print()
# print("===== 초기 격자판 =====")
# print(board)
# print("==== 초기 유리벽면 ====")
# print(waits)

''' 풀이법
1. 1차 획득
3x3에 모든 회전 후 bfs(점수)를 조합해 결과 리스트 반환
- 결과 정렬: [-점수, 회전각, y, x ] 
2. 결과 맨 앞의 점수가 0이면 종료
2.1. 결과 맨 앞의 점수가 0이 아니면 결과를 바탕으로 유물 획득
2.2. 벽면에서 pop해서 채워넣기

3. 현재 위치에서 bfs 탐색 후 점수 반환
3.1. bfs 점수가 0이 될때까지 반복

다음턴 수행

'''
is_end=False
for _ in range(K):
    total_score = 0
    # 1. 1차 획득
    max_score, finded, board=first_gain(board)
    total_score+=max_score
    if max_score==0:
        is_end = True
        answer.append(total_score)
        print_answer(answer)
        break # 턴 종료
    # 2. 유물 채우기
    board, waits =add(board, waits, finded)

    # 3. 유물 연쇄 획득
    while True:
        score, finded = search(board) # 사라질 것들과

        if score==0:
            break

        total_score += score
        board, waits = add(board, waits, finded) # 점수 추가

    # print()
    # print("결과")
    # print(f'최대: {total_score} ')
    # print(f'사라질 경로: {finded}')
    # print(f'격자판: {board}')
    # print(f'벽면유리조각: {waits}')
    answer.append(total_score)
# 안 끝났으면?
if not is_end:
    print_answer(answer)