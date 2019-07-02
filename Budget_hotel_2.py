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
                print('Название отеля: ' + ch['hotelName'], 'Количество звёзд: '
                      + str(ch['stars']), 'Средняя цена за проживание в номере за указанный период: '
                      + str(int(ch['priceAvg'])), 'Минимальная цена за проживание в номере отеля за указанный период: '
                      + str(int(ch['priceFrom'])), sep='\n')

        except ValueError:
            print('Сорри, вам не хватает денег:(')

#hotels('Москва', '30.06.2019', '30.07.2019', budget=50000)