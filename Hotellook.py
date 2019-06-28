def hotels(city, check_in, check_out):#city - город, check_in - дата приезда, check_out - дата отъезда (ДД.ММ.ГГГГ)
    import requests
    import json
    token = 'ee22fa29999330fa000fa56040169406'
    marker = '233500'
    city = city
    check_in = check_in.split('.')
    check_out = check_out.split('.')

    def find_id(city=city, check_in = check_in, check_out=check_out):
        url = 'http://engine.hotellook.com/api/v2/cache.json?location=' + city +'&currency=rub&checkIn=' + str(check_in[2])+'-'+str(check_in[1])+'-'+str(check_in[0]) + '&checkOut=' + str(check_out[2])+'-'+str(check_out[1])+'-'+str(check_out[0]) + '&limit=1'
        response = requests.get(url)
        try:
            cityid = response.json()[0]['locationId']
            return cityid
        except:
            print('Указанного города не найдено')
            return False

    if find_id():
        url = 'http://engine.hotellook.com/api/v2/cache.json?locationId=' + str(find_id()) + '&currency=rub&checkIn=' + str(check_in[2])+'-'+str(check_in[1])+'-'+str(check_in[0]) + '&checkOut=' + str(check_out[2])+'-'+str(check_out[1])+'-'+str(check_out[0]) + '&token=' + token + '&limit=10000'
        response = requests.get(url)
        hotel = response.json()

        print('------------------------------------------------------')
        min_price = 100000
        for i in hotel:
            if i['priceFrom'] < min_price:
                min_price = i['priceFrom']
                ch = i

        print('Название отеля: ' + ch['hotelName'], 'Количество звёзд: ' + str(ch['stars']), 'Средняя цена за проживание в номере за указанный период: ' + str(int(ch['priceAvg'])), 'Минимальная цена за проживание в номере отеля за указанный период: ' + str(int(ch['priceFrom'])), sep='\n')
        print('------------------------------------------------------')
#hotels('Москва', '29.06.2019', '29.06.2019')
