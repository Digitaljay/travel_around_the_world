def general(you_native_city,to_visit,date_to_go):     # в поле to_visit должен быть массив городов, которые вы собираетесь посетить,
    def avia(d_city,a_city,data):                     # date_to_go вводится в формате ДД.ММ.ГГГГ
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
        for k in flies:
            if datetime.date(int(k['depart_date'].split('-')[0]),int(k['depart_date'].split('-')[1]),int(k['depart_date'].split('-')[2]))==datetime.date(data[2],data[1],data[0]):
                newlist.append(int(k['value']))

        return(min(newlist))
    #print(avia('Екатеринбург',"Москва","03.07.2019"))

    def tutu(depart, arrive, date_to_go): #depart - город отбытия, arrive - город прибытия, date_to_go - дата формате ДД.ММ.ГГГГ
        import json
        import requests
        from bs4 import BeautifulSoup
        import pickle

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
                        except:
                            pass
                except:
                    pass
        return min(costs_for_trains)
    #print(tutu('Екатеринбург',"Москва","03.07.2019"))

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
                    path_train=tutu(city[1],point[1],date_to_go)
                except:
                    path_train=1000000000
                try:
                    path_avia=avia(city[1],point[1],date_to_go)
                except:
                    path_avia=1000000000
                #print(start,finish,min(path_train,path_avia))
                edges.append([start,finish,min(path_train,path_avia)])


    result=path(len(all_cities),edges)
    order=[]
    # print('Цена маршрута (в рублях): ',result[0])
    # print('Порядок посещения городов: ')
    for i in result[1]:
        order.append(cities[i-1][1])
    return [result[0],order]