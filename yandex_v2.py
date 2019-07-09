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
            x = [j['from']['transport_type'], j['arrival'], j['departure'], round(j['duration']/3600, 2),
                  j['tickets_info']['places'][0]['price']['whole'],
                  j['thread']['carrier']['title'], j['thread']['carrier']['url']]
            transport.append(x)
            #print('------------------------------------------------')
    return transport
#print(bus(date='12.07.2019', from_city='Реж', to_city='Екатеринбург'))