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
    data=[int(i) for i in data]
    avia = json.loads(requests.get(url).text)
    flies=avia['best_prices']
    newlist=[]
    for k in flies:
        if datetime.date(int(k['depart_date'].split('-')[0]),int(k['depart_date'].split('-')[1]),int(k['depart_date'].split('-')[2]))==datetime.date(data[2],data[1],data[0]):
            newlist.append(int(k['value']))

    return(min(newlist))
#print(avia('Екатеринбург',"Москва","03.07.2019"))
