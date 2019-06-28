n=int(input())
edges=[]
for i in range(n*(n-1)):
    edges.append([int(i) for i in input().split()])
nodes=[]
for i in range(n-1):
    nodes.append(0)
rebs=[[]]*n
for i in edges:
    rebs[i[0]-1].append(i)
    rebs[i[1]-1].append(i)
    if i[0]==1:
        nodes[i[1]-2]=i[2]
real_path=[0]
general_cost=0
AIMS=[]
for i in range(2,n+1):
    AIMS.append(i)
POINT=1
while real_path[-1]!=1:
    path=[1]
    #print(nodes)
    def cost(point,aims):
        #print('****************************')
        #print(point,aims)
        #print(aims)
        if type(aims)!=list or len(aims)==0:
            #print(nodes[point-1])
            path.append(point)
            path.append(1)
            return nodes[point-2]
        else:
            minn=1000000000
            for aim in aims:
                #print(aim,aims)
                ai=aims[:]
                ai.remove(aim)
                #print(aim,ai,aims)
                ed=[]
                for i in edges:
                    if i[0]==aim and i[1]==point:
                        ed=i
                        break
                co=cost(aim,ai)+ed[2]

                #print(point,cost(aim,ai))
                if co<minn:
                    minn=co
                    path.append(aim)
            return(minn)

    cc=cost(POINT,AIMS)
    #print(path)
    if cc>general_cost:
        general_cost=cc
    POINT=path[-1]
    #print(POINT)
    try:
        AIMS.remove(POINT)
    except:
        pass
    real_path.append(POINT)
print(general_cost)
real_path[0]=1
print(*real_path[::-1])
