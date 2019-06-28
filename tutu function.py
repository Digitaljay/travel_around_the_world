def tutu(depart, arrive, date_to_go): #depart - город отбытия, arrive - город прибытия, date_to_go - дата формате ДД.ММ.ГГГГ
    import json
    import requests
    from bs4 import BeautifulSoup
    import pickle

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
            # print(p_d)
            # print(p_a)
            url = 'https://www.tutu.ru/poezda/rasp_d.php?nnst1='+p_d+'&nnst2='+p_a+'&date='+date_to_go
            #print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            needed=soup.find_all('script')[18]
            try:
                preobr=str(needed).split('\n')[1].strip()
                j=json.loads(preobr[16:-1])

                for train in j['componentData']['searchResultList'][0]['trains']:
                    try:

                        for type in train['params']['withSeats']['categories']:
                            costs_for_trains.append(int(type['params']['price']['RUB']))

                    except:
                        pass
            except:
                pass
    return min(costs_for_trains)
#print(tutu('Екатеринбург',"Москва","03.07.2019"))
