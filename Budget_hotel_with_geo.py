#Выводит наиблишайшие отели к указанной точке
def hotels(city, check_in, check_out, budget, lon_point, lat_point, name_point):
    import requests
    import urllib
    import json
    from distances import haversine, best_located
    token = 'ee22fa29999330fa000fa56040169406'
    city = city
    hotels_id = []
    g = 0
    closest_dist = []
    indexes = []
    dis_list = []
    geo_list = []
    coor_list = []
    budget = budget
    check_in = check_in.split('.')
    check_out = check_out.split('.')
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
                hotel_list.append(i)
        for g in range(10):
            geo_url = 'http://engine.hotellook.com/api/v2/lookup.json?query=' + str(
                hotels_id[g]) + '&lang=ru&lookFor=both&limit=1'
            response = requests.get(geo_url)
            geo_hot = response.json()
            try:
                geo_list.append(geo_hot['results']['hotels'][0]['location'])
                # print(geo_hot['results']['hotels'][0]['location'])
                coor_list.append([geo_hot['results']['hotels'][0]['location']['lon'],
                                  geo_hot['results']['hotels'][0]['location']['lat'],
                                  geo_hot['results']['hotels'][0]['id']])
            except IndexError:
                pass
    the_best_located = best_located([[lon_point, lat_point, name_point]], coor_list)
    for dis in the_best_located:
        dis_list.append(the_best_located[dis])
    for dist in range(5):
        if min(dis_list) == 10 ** 5:
            continue
        else:
            closest_dist.append(min(dis_list))
            indexes.append(dis_list.index((min(dis_list))))
            dis_list[dis_list.index((min(dis_list)))] = 10 ** 5

    for ind in indexes:
        ch = hotel_list[ind]
        print('Название отеля: ' + ch['hotelName'], 'Количество звёзд: '
              + str(ch['stars']), 'Средняя цена за проживание в номере за указанный период: '
              + str(int(ch['priceAvg'])), 'Минимальная цена за проживание в номере отеля за указанный период: '
              + str(int(ch['priceFrom'])), sep='\n')
#hotels('Москва', '10.07.2019', '30.07.2019', budget=30000, lon_point=37.617635, lat_point=55.755814, name_point='Центр Москвы')
