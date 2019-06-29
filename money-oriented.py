# как можно быстрее при ограниченном бюджете
def general(you_native_city,to_visit,date_to_go,budget):     # в поле to_visit должен быть массив городов, которые вы собираетесь посетить,
    time_trav=[]                                      # date_to_go вводится в формате ДД.ММ.ГГГГ
    transp=[]
    from dateutil.relativedelta import relativedelta
    def avia(d_city,a_city,data,nextt):
        import requests
        import json
        import datetime
        data=data.split('.')
        ask_url='https://www.travelpayouts.com/widgets_suggest_params?q=Из%20'+d_city+'%20в%20'+a_city
        ask=json.loads(requests.get(ask_url).text)
        d_code=ask['origin']['iata']
        a_code=ask['destination']['iata']
        if a_code=='NVR':
            a_code='GOJ'
        elif d_code=='NVR':
            d_code='GOJ'
        url = 'http://min-prices.aviasales.ru/calendar_preload?origin='+d_code+'&destination='+a_code+'&depart_date='+data[2]+'-'+data[1]+'-'+data[0]+'&one_way=true'
        data=[int(i) for i in data]
        avia = json.loads(requests.get(url).text)
        flies=avia['best_prices']
        newlist=[]
        dist=0
        for k in flies:
            if datetime.date(int(k['depart_date'].split('-')[0]),int(k['depart_date'].split('-')[1]),int(k['depart_date'].split('-')[2]))==datetime.date(data[2],data[1],data[0])+datetime.timedelta(days=nextt):
                newlist.append(int(k['value']))
                dist=int(k['distance'])

        return [min(newlist),round(dist/950 + 0.49)]
    #print(avia('Екатеринбург',"Москва","03.07.2019"))

    # def avia_next(d_city,a_city,data):
    #     import requests
    #     import json
    #     import datetime
    #     data=data.split('.')
    #     ask_url='https://www.travelpayouts.com/widgets_suggest_params?q=Из%20'+d_city+'%20в%20'+a_city
    #     ask=json.loads(requests.get(ask_url).text)
    #     d_code=ask['origin']['iata']
    #     a_code=ask['destination']['iata']
    #     if a_code=='NVR':
    #         a_code='GOJ'
    #     elif d_code=='NVR':
    #         d_code='GOJ'
    #     url = 'http://min-prices.aviasales.ru/calendar_preload?origin='+d_code+'&destination='+a_code+'&depart_date='+data[2]+'-'+data[1]+'-'+data[0]+'&one_way=true'
    #     data=[int(i) for i in data]
    #     avia = json.loads(requests.get(url).text)
    #     flies=avia['best_prices']
    #     newlist=[]
    #     dist=0
    #     for k in flies:
    #         if datetime.date(int(k['depart_date'].split('-')[0]),int(k['depart_date'].split('-')[1]),int(k['depart_date'].split('-')[2]))==datetime.date(data[2]+1,data[1],data[0]):
    #             newlist.append(int(k['value']))
    #             dist=int(k['distance'])
    #
    #     return [min(newlist),round(dist/950 + 0.49)]

    def tutu(depart, arrive, date_to_go,nextt): #depart - город отбытия, arrive - город прибытия, date_to_go - дата формате ДД.ММ.ГГГГ
        import json
        import requests
        from bs4 import BeautifulSoup
        import pickle

        times=[]



        costs_for_trains=[]
        with open("depart.txt", "rb") as myFile:
            dep = pickle.load(myFile)

        with open("arrive.txt", "rb") as myFile:
            arr = pickle.load(myFile)

        p_dl=set()
        p_al=set()

        for i in dep:
            if depart in i:
                p_dl.add(dep[i])

        for i in arr:
            if arrive in i:
                p_al.add(arr[i])

        for p_d in p_dl:
            for p_a in p_al:
                if nextt!=0:
                    date_to_go=date_to_go.spit('.')
                    url = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1='+p_d+'&nnst2='+p_a+'&date='+str(int(date_to_go[0]+nextt))+'.'+str(date_to_go[1])+'.'+str(date_to_go[2])
                else:
                    url = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1='+p_d+'&nnst2='+p_a+'&date='+date_to_go
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                needed=soup.find_all('script')[18]
                try:
                    preobr=str(needed).split('\n')[1].strip()
                    j=json.loads(preobr[16:-1])

                    for train in j['componentData']['searchResultList'][0]['trains']:
                        try:
                            for type in train['params']['withSeats']['categories']:
                                costs_for_trains.append(int(type['params']['price']['RUB']))
                            times.append(round(int(train['params']['trip']['travelTimeSeconds'])/3600))
                        except:
                            pass
                except:
                    pass
        return [min(costs_for_trains),min(times)]
    #print(tutu('Екатеринбург',"Москва","03.07.2019"))

    table={}

    def path(n,edges):
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

                if type(aims)!=list or len(aims)==0:
                    #print(nodes[point-1])
                    path.append(point)
                    path.append(1)
                    return nodes[point-2]
                else:
                    minn=10000000000
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
                        if co<=minn:
                            minn=co
                            path.append(aim)
                    return(minn)

            cc=cost(POINT,AIMS)

            if cc>general_cost:
                general_cost=cc
            POINT=path[-1]
            #print(POINT)
            try:
                AIMS.remove(POINT)
            except:
                pass
            real_path.append(POINT)
        #print(general_cost)
        real_path[0]=1
        #print(*real_path[::-1])
        return [general_cost,real_path[::-1]]

    you_native_city=[you_native_city]
    all_cities=you_native_city+to_visit

    cities=[]
    for city in range(len(all_cities)):
        cities.append([city+1,all_cities[city]])

    edges=[]

    for city in cities:

        for point in cities:

            if city!=point:
                start=city[0]
                finish=point[0]
                try:
                    path_train=tutu(city[1],point[1],date_to_go,0)
                except:
                    try:
                        path_train=tutu(city[1],point[1],date_to_go,3)
                    except:
                        path_train=[1000000000,1000000000]

                try:
                    path_avia=avia(city[1],point[1],date_to_go,0)
                except:
                    try:
                        path_avia=avia(city[1],point[1],date_to_go,7)
                    except:
                        try:
                            path_avia=avia(city[1],point[1],date_to_go,1)
                        except:
                            path_avia=[1000000000,1000000000]
                #print(start,finish,min(path_train,path_avia))

                if path_train[0]==path_avia[0]==1000000000:
                    time_trav.append(0)
                    edges.append([start,finish,0])
                    transp.append('местный транспорт (автобус, такси и т.д.)')
                    table[str(start)+' '+str(finish)]=[[100,100],[100,100]]
                    time_trav.append(1)
                elif path_train[0]<path_avia[0]:
                    time_trav.append(path_train[1])
                    edges.append([start,finish,path_train[0]])
                    transp.append('поезд')
                    table[str(start)+' '+str(finish)]=[path_train,path_avia]
                else:
                    time_trav.append(path_avia[1])
                    edges.append([start,finish,path_avia[0]])
                    transp.append('самолёт')
                    table[str(start)+' '+str(finish)]=[path_train,path_avia]
    #print('table is ready')
    # for i in table:
    #    print(i,table[i])
    result=path(len(all_cities),edges)
    order=[]
    # print('Цена маршрута (в рублях): ',result[0])
    # print('Порядок посещения городов: ')
    total_time=0
    #print(result)
    new_table=[]
    for i in range(len(result[1])-1):
        order.append([cities[result[1][i]-1][1]])
        pair=[result[1][i],result[1][i+1]]
        new_table.append(table[str(pair[0])+' '+str(pair[1])])
        for j in range(len(edges)):
            if edges[j][0]==pair[0] and edges[j][1]==pair[1]:
                total_time+=time_trav[j]
                order[-1].append(transp[j])
    order.append(you_native_city)
    #print(time_trav)
    coins=result[0]
    time_lost=total_time
    ind_t=0
    while coins<budget and ind_t!=len(new_table)-1:
        if new_table[ind_t][1][1]<new_table[ind_t][0][1] and new_table[ind_t][1][0]>=new_table[ind_t][0][0] and new_table[ind_t][1][1]!=100:
            order[ind_t][1]='самолёт'
            time_lost-=new_table[ind_t][0][1]
            time_lost+=new_table[ind_t][1][1]
            coins-=new_table[ind_t][0][0]
            coins+=new_table[ind_t][1][0]
        ind_t+=1
     #   print(ind_t)
    #print(coins,time_lost)
    return [coins,order,time_lost]
RESULT=general('Екатеринбург',['Челябинск','Нижний Тагил','Тюмень'],'11.07.2019',40000)
print('Цена: от',RESULT[0],"руб")
for i in RESULT[1]:
    print(' | '.join(i))
print('Затраченное время: ', RESULT[2], 'ч')

# print(RESULT[2],'ч')
# print('Порядок городов в маршруте: ')
# for i in RESULT[1]:
#     print(*i)
# print("Цена маршрута: ",RESULT[0],'руб')


