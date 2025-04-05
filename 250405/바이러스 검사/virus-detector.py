# 입력받기

n=int(input())
rests=list(map(int,input().split()))
ldr, mbr=map(int,input().split())

# print(n)
# print(rests)
# print(ldr, mbr)
# print()
# 일단 팀장 개수뺌

answer=n

for i,rest in enumerate(rests):
    after=rest-ldr
    if after<0:
        after=0
    rests[i]=after
# print(rests)
for rest in rests:
    # 만약 멤버 혼자 처리 가능하면
    if rest<=0:
        continue
    if rest <= mbr:
        answer+=1
    else:
        q=rest//mbr
        r=rest%mbr
        if r!=0:
            answer+=(q+1)
        else:
            answer += q

# print(rests)
# print()

print(answer)