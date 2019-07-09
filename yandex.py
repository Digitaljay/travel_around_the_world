def yandex(d_city,a_city):
    costs=[]
    import json,requests
    url_st='https://api.rasp.yandex.net/v3.0/stations_list/?apikey=8f701887-2356-46e9-9d31-dcb1a1bf6687&lang=ru_RU&format=json'
    ask_st=json.loads(requests.get(url_st).text)
    d_code=''
    a_code=''
    for i in ask_st['countries']:
        if i['title']=='Россия':
            for j in i['regions']:
                for f in j["settlements"]:
                    if f['title']==d_city:
                        d_code=f['codes']["yandex_code"]
                    elif f['title']==a_city:
                        a_code=f['codes']["yandex_code"]
    url='https://api.rasp.yandex.net/v3.0/search/?apikey=8f701887-2356-46e9-9d31-dcb1a1bf6687&format=json&from='+d_code+'&to='+a_code+'&lang=ru_RU&page=1&date=2019-07-25'
    #print(url)
    ask=json.loads(requests.get(url).text)
    #print(ask)
    for i in ask['interval_segments']:
        if len(i['tickets_info']['places'])!=0:
            for j in i['tickets_info']['places']:
                costs.append([j['price']['whole'],round(i['duration']/3600),i['thread']['transport_type']])
    for i in ask['segments']:
        if len(i['tickets_info']['places'])!=0:
            for j in i['tickets_info']['places']:
                costs.append([j['price']['whole'],round(i['duration']/3600),i['thread']['transport_type']])
    return(sorted(costs))
print(yandex('Москва','Санкт-Петербург'))
