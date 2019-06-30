from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):            #finds distance between a couple of objects (navigation system wgs84)
    # haversine formula
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371* c
    return km
def best_located(points,hotels): #общий ввод [[[],[],[],[],...], [[],[],[],[],...]]
    distances={}                 #ввод объектов (пример): [57.1738066, 60.1983324,"Таватуй"]
    for i in hotels:
        lon_1=i[0]
        lat_1=i[1]
        total_d=0
        for j in points:
            lon_2=j[0]
            lat_2=j[1]
            total_d+=haversine(lon_1,lat_1,lon_2,lat_2)
        distances[i[2]]=total_d
    return(distances)
print(best_located([[57.1514213,60.2166384,'Уралочка'],[57.1560679,60.2212371,"Гора"]],[[57.1738066, 60.1983324,"Таватуй"],[57.1520709, 60.2160671,"Почта"]]))

