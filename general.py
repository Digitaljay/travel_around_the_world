def general(you_native_city,to_visit,date_to_go,budget):     # в поле to_visit должен быть массив городов, которые вы собираетесь посетить,
    time_trav=[]                                      # date_to_go вводится в формате ДД.ММ.ГГГГ
    transp=[]
    def bus(date, from_city, to_city):
        import requests
        transport = []
        from_list = []
        to_list = []
        def city_code(city):
            url_2 = 'https://api.rasp.yandex.net/v3.0/stations_list/?apikey=' + api_key + '&lang=ru_RU&format=json'
            response_2 = requests.get(url_2)
            code = response_2.json()
            for i in code['countries']:
                for g in i['regions']:
                    for x in g['settlements']:
                        if x['title'] == city:
                            #print(x['codes']['yandex_code'])
                            return x['codes']['yandex_code']
        date = date.split('.')
        api_key = 'cafb041f-753a-4572-8e33-b8be52d5a05d'
        url = 'https://api.rasp.yandex.net/v3.0/search/?apikey=' + api_key + '&format=json&from='\
              + city_code(city=from_city) + '&to='+ city_code(city=to_city) + '&lang=ru_RU&page=1&date=' + \
              str(date[2])+'-'+str(date[1])+'-'+str(date[0])
        response = requests.get(url)
        bus_json = response.json()
        for j in bus_json['segments']:
            if j['tickets_info']['places'] != []:
                #print('------------------------------------------------')
                #print(j['arrival'], j['departure'], round(j['duration']/3600, 2),
                      #j['tickets_info']['places'][0]['price']['whole'],
                      #j['thread']['carrier']['title'], j['thread']['carrier']['url'], sep='\n')
                x = [j['from']['transport_type'],
                      #j['arrival'], j['departure'],
                      j['tickets_info']['places'][0]['price']['whole'],
                      round(j['duration']/3600, 2),
                      j['thread']['carrier']['title'], j['thread']['carrier']['url']]
                transport.append(x)
                #print('------------------------------------------------')
        if len(transport)==0:
            transport.append(['нет подходящего транспорта',1000000000,'время и цена неизвестны'])
        return transport[0]
    #print(bus(date='12.07.2019', from_city='Реж', to_city='Екатеринбург'))
    def avia(d_city,a_city,data):
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
            #print(url)
            data=[int(i) for i in data]
            avia = json.loads(requests.get(url).text)
            flies=avia['best_prices']
            newlist=[]
            dist=0
            for k in flies:
                    if datetime.date(int(k['depart_date'].split('-')[0]),int(k['depart_date'].split('-')[1]),int(k['depart_date'].split('-')[2]))==datetime.date(data[2],data[1],data[0])+datetime.timedelta(days=14):
                        newlist.append(int(k['value']))
                        dist=int(k['distance'])
            minn=0
            try:
                minn=min(newlist)
            except:
                try:
                    for k in flies:
                            newlist.append(int(k['value']))
                            dist=int(k['distance'])
                    minn=min(newlist)
                except:
                    minn=1000000000000
            return ['plane',minn,round(dist/950 + 0.49)]
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

    routes=[]
    params={}
    you_native_city=[you_native_city]
    all_cities=you_native_city+to_visit
    cities=[]
    for city in range(len(all_cities)):
        cities.append([city+1,all_cities[city]])

    for i in cities:
        for j in cities:
            if i[0]!=j[0]:
                yand=bus(date_to_go,i[1],j[1])
                air=avia(i[1],j[1],date_to_go)
                inform=[]
                if yand[1]<air[1]:
                    inform=yand
                    routes.append([i[1],j[1],yand[1]])
                else:
                    inform=air
                    routes.append([i[0],j[0],air[1]])
                params[i[1]+j[1]]=inform
    #print(routes)
    result=path(len(all_cities),routes)
    q=result[1]
    RESULT=[]
    total_time=0
    total_cost=0
    for i in range(len(q)-1):
        #city1=cities[q[i]-1]
        charact=params[cities[q[i]-1][1]+cities[q[i+1]-1][1]]
        total_cost+=charact[1]
        total_time+=charact[2]
        RESULT.append([cities[q[i]-1][1],charact])
    return[RESULT,total_cost,total_time]
print(general('Екатеринбург',['Санкт-Петербург','Казань'],'24.07.2019',60000))
