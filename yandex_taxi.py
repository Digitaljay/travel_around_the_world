def taxi(d_city,a_city):
    import requests
    import json
    import datetime
    from geopy.geocoders import Nominatim
    clid=''
    apikey=''
    geolocator = Nominatim(user_agent="my-application")
    location_d = geolocator.geocode(d_city)
    location_a = geolocator.geocode(a_city)
    #print((location.latitude, location.longitude))
    url='https://taxi-routeinfo.taxi.yandex.net/taxi_info?rll='+str(location_d.longitude),str(location_d.latitude)+'~'+str(location_a.longitude),str(location_a.latitude)+'&clid='+clid+'&apikey='+apikey
    response = json.loads(requests.get(url).text)
    price=response['options'][0]['price']

    return(price)
print(taxi('Екатеринбург',"Москва"))
