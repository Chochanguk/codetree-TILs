from collections import deque

dx=[-1,0,1,0]
dy=[0,-1,0,1]

# 입력
n,m,K=map(int,input().split())
forest=[[0]*m for _ in range(n)]
answer=0

# 출구 위치
def getExit(x,y,d):
    if d==0:
        return [x-1,y]
    elif d==1:
        return [x,y+1]
    elif d==2:
        return [x+1,y]
    else:
        return [x,y-1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<m:
        return True
    return False

# 골렘이 어떤 좌표로 이동 가능한 상태인지 확인
def check(x,y):
    if not inBoard(x,y): # 좌표가 보드 밖에 위치하면
        if x<n and 0<=y<m: # 좌표가 위쪽이 뚫린 바구니 같은 공간에 있는지
            return True
    else: # 좌표가 보드 안에 위치하면
        if forest[x][y]==0: # 다른 골렘이 없는지
            return True
    return False

# 골렘 이동
def move(c,d,id):
    global forest

    x,y=-2,c # 골렘 내 중앙의 정령 위치. 보드 맨 위에서 두 칸 위인 x==-2 지점부터 내려온다.
    while True:
        # 골렘 수직 이동
        if check(x+2,y) and check(x+1,y-1) and check(x+1,y+1):
            x+=1
        # 골렘 왼쪽 이동
        elif check(x+1,y-1) and check(x-1,y-1) and check(x,y-2) and check(x+1,y-2) and check(x+2,y-1):
            # 중심 좌표 이동 및 방향 회전
            x+=1
            y-=1
            d=(d+3)%4 # 반시계 회전
        # 골렘 오른쪽 이동
        elif check(x+1,y+1) and check(x-1,y+1) and check(x,y+2) and check(x+1,y+2) and check(x+2,y+1):
            # 중심 좌표 이동 및 방향 회전
            x+=1
            y+=1
            d=(d+1)%4 # 시계 회전
        else:
            break

    # 골렘 지도에 표시(이동완료)
   
    # 골렘이 맵을 벗어난 경우 
    if not inBoard(x, y) or not inBoard(x + 1, y) or not inBoard(x-1,y) or not inBoard(x,y+1) or not inBoard(x,y-1):
        return [False, -1, -1]
    # 골렘이 맵을 벗어나지 않은 경우
    else:
        # 골렘 id로 초기화
        forest[x][y]=forest[x+1][y]=forest[x-1][y]=forest[x][y+1]=forest[x][y-1]=id
        # 출구 위치 계산
        ex, ey = getExit(x, y, d)# 출구 위치
        # 출구 위치만 음수로 둠
        forest[ex][ey]=-id

        return [True,x,y]

# 정령 이동
def bfs(sx,sy):
    global answer
    can_positioned=[]
    q=deque()
    q.append((sx,sy))
    visit=[[False]*m for _ in range(n)]
    visit[sx][sy]=True

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            # 다음 위치가 골렘이 없거나 맵을 벗어났거나 방문 했던 적이면 다음 방향 탐색
            if not inBoard(nx,ny) or visit[nx][ny] or forest[nx][ny]==0:
                continue
            # 절댓값이 같은 칸(ID로 표시)으로 움직이거나, 출구 칸(-1)에서 다른 골렘(id가 다른)으로 이동 가능
            if abs(forest[x][y])==abs(forest[nx][ny]) or (forest[x][y]<0 and abs(forest[nx][ny])!=abs(forest[x][y])):
                q.append((nx,ny))
                visit[nx][ny]=True
                # 정령이 움직인 행 위치를 추가
                can_positioned.append(nx)
                
    # 움직였던 위치에서 행값이 가장 큰 값을 출력
    return max(can_positioned)+1

# 시뮬레이션 시작 (골렘마다)
for id in range(1,K+1):
    c,d=map(int,input().split())
    c-=1

    # 골렘 이동
    res=move(c,d,id)
    inBound,x,y=res

    # 골렘 몸 일부가 숲 벗어나있는지 확인
    if inBound:
        # 정령 이동
        answer+=bfs(x,y)
    else:
        # 숲 재 초기화
        forest=[[0]*m for _ in range(n)]

print(answer)