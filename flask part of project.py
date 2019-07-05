from flask import Flask, abort, request
def hotels(city, check_in, check_out, budget):#city - город, check_in - дата приезда, check_out - дата отъезда (ДД.ММ.ГГГГ), budget - бюджет пользователя
    import requests
    import urllib
    import json
    token = 'ee22fa29999330fa000fa56040169406'
    fake_token = '1cb0607996357c86276243b68d4ff258'
    marker = '233500'
    city = city
    hotels_id = []
    #property_type=[]
    #hotels_price = []
    rating = []
    budget = budget
    check_in = check_in.split('.')
    check_out = check_out.split('.')

    min_c=1000000000
    name_min=''
    stars_min=0

    def find_id(city=city, check_in = check_in, check_out=check_out):
        url = 'http://engine.hotellook.com/api/v2/cache.json?location=' + city +'&currency=rub&checkIn=' + str(check_in[2])+'-'+str(check_in[1])+'-'+str(check_in[0]) + '&checkOut=' + str(check_out[2])+'-'+str(check_out[1])+'-'+str(check_out[0]) + '&limit=1'
        response = requests.get(url)

        try:
            cityid = response.json()[0]['locationId']
            return cityid
        except:
            print('За указанный период жилья в этом городе найдено не было!')
            return False

    if find_id():
        url = 'http://engine.hotellook.com/api/v2/cache.json?locationId=' + str(find_id()) + \
              '&currency=rub&checkIn=' + str(check_in[2])+'-'+str(check_in[1])+'-'+str(check_in[0]) + \
              '&checkOut=' + str(check_out[2])+'-'+str(check_out[1])+'-'+str(check_out[0]) + '&token=' + token + '&limit=10000'
        response = requests.get(url)

        hotel = response.json()
        hotel_list = []
        for i in hotel:
            if int(i['priceFrom']) < budget:
                hotels_id.append(i['hotelId'])
                rating.append(i['stars'])
                hotel_list.append(i)
        #print(hotels_id)
        #print(rating)


        try:

            g = 0
            max_rating = []
            indexes = []
            for g in range(5):

                if max(rating) == -1:
                    continue
                else:
                    max_rating.append(max(rating))
                    indexes.append(rating.index((max(rating))))
                    rating[rating.index((max(rating)))] = -1




            #print(max_rating)

            for ind in indexes:
                ch = hotel_list[ind]
                # print('Название отеля: ' + ch['hotelName'], 'Количество звёзд: '
                #       + str(ch['stars']), 'Средняя цена за проживание в номере за указанный период: '
                #       + str(int(ch['priceAvg'])), 'Минимальная цена за проживание в номере отеля за указанный период: '
                #       + str(int(ch['priceFrom'])), sep='\n')
                if int(ch['priceFrom'])<min_c:
                    min_c=int(ch['priceFrom'])
                    name_min=ch['hotelName']
                    stars_min=ch['stars']

        except ValueError:
            print('Сорри, вам не хватает денег:(')
    return(min_c,name_min,stars_min)
#print(hotels('Москва', '05.07.2019', '30.07.2019', budget=50000))
# как можно быстрее при ограниченном бюджете
from geopy.geocoders import Nominatim
import time
import re
from math import radians, cos, sin, asin, sqrt
geolocator = Nominatim(user_agent="my-application")
#location = geolocator.reverse("52.509669, 13.376294")
#print(location.address)
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
def haversine(lon1, lat1, lon2, lat2):            #finds distance between a couple of objects (navigation system wgs84)
    # haversine formula
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371* c
    return km
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

    def tutu(depart, arrive, date_to_go, nextt): #depart - город отбытия, arrive - город прибытия, date_to_go - дата формате ДД.ММ.ГГГГ
        import json
        import requests
        from bs4 import BeautifulSoup
        import pickle

        times=[]

        pattern = re.compile('CAPTCHA')
        # result = pattern.findall('AV Analytics Vidhya AV')
        # print result

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
                if nextt==0:
                    url = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1='+p_d+'&nnst2='+p_a+'&date='+date_to_go
                else:
                    date_to_go=date_to_go.split('.')
                    url = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1='+p_d+'&nnst2='+p_a+'&date='+str(int(date_to_go[0])+nextt)+'.'+date_to_go[1]+'.'+date_to_go[2]
                page = requests.get(url,headers=headers)
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

                    while len(pattern.findall(str(soup)))!=0:
                        time.sleep(1)
                        print(pattern.findall(str(soup)))
                        page = requests.get(url,headers=headers)
                        soup = BeautifulSoup(page.text, 'html.parser')
                        print(pattern.findall(str(soup)))
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
        print([min(costs_for_trains),min(times)])
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
    hotels_d={}

    for i in to_visit:
        cost_for_hotel=hotels(i,date_to_go,date_to_go,budget)
        budget-=cost_for_hotel[0]
        hotels_d[i]=cost_for_hotel

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
                    # time.sleep(10)
                    try:
                        path_train=tutu(city[1],point[1],date_to_go,1)
                    except:
                        # time.sleep(10)
                        try:
                            path_train=tutu(city[1],point[1],date_to_go,2)
                        except:
                            # time.sleep(10)
                            try:
                                path_train=tutu(city[1],point[1],date_to_go,3)
                            except:
                                location1 = geolocator.geocode(city[1])
                                location2 = geolocator.geocode(point[1])
                                lat1,lon1=[location1.latitude, location1.longitude]
                                lat2,lon2=[location2.latitude, location2.longitude]
                                if haversine(lon1, lat1, lon2, lat2)>350:
                                    path_train=[1000000000000,1000000000000]
                                else:
                                    path_train=[1000000000,1000000000]
                                # time.sleep(10)

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
                #print(str(start)+' '+str(finish),[path_train,path_avia])
                if path_train[0]==1000000000 and path_avia[0]==1000000000:
                    edges.append([start,finish,100])
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
    #     print(i,table[i])
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
    while coins+new_table[ind_t][1][0]-new_table[ind_t][0][0]<=budget and ind_t!=len(new_table)-1:
        if new_table[ind_t][1][1]<new_table[ind_t][0][1] and new_table[ind_t][1][0]>=new_table[ind_t][0][0] and new_table[ind_t][1][1]!=100:
            order[ind_t][1]='самолёт'
            time_lost-=new_table[ind_t][0][1]
            time_lost+=new_table[ind_t][1][1]
            coins-=new_table[ind_t][0][0]
            coins+=new_table[ind_t][1][0]
        ind_t+=1
    for i in order:
        if i[0]!=you_native_city:
            i[0]+=' (Отель: '+str(hotels_d[i][1])+' Звёзды: '+str(hotels_d[i][2])+' Стоимость: '+str(hotels_d[i][0])+') '
     #   print(ind_t)
    #print(coins,time_lost)
    return [coins,order,time_lost]

############################################################
#there Flask starts


born_city=''
cities_visit=[]
start_date=''

budget=0

app = Flask(__name__)
from flask import request

@app.route('/',methods=['POST'])
def index():
    if not request.json:
        abort(400)
    born_city=request.json['city_start']
    cities_visit=request.json['cities_to_visit']
    start_date=request.json['date_to_go_travelling']
    budget=request.json['users_budget']
    return 'Это будет главная страница, здесь вводятся города, бюджет и т.д.'


@app.route('/result')
def result():
    return general(born_city,cities_visit,start_date,budget)

if __name__ == "__main__":
    #app.run(debug=True)


    app.run(host='192.168.5.31')

########################################################
