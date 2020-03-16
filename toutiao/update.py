import requests, json
import pandas as pd
import time
from datetime import timedelta
today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
yesterday = pd.to_datetime(today) - timedelta(days=1)

# 今日头条
url = 'https://i.snssdk.com/ugc/hotboard_fe/hot_list/template/hot_list/forum_tab.html'
a = requests.get('https://i.snssdk.com/forum/ncov_data/?data_type=%5B2%2C4%5D').json()
# 国家级别
b = json.loads(a['overseas_data'])['country']
for i in range(len(b)):
    b[i]['confirmedTotal'] = b[i]['countryTotal']['confirmedTotal']
    b[i]['suspectedTotal'] = b[i]['countryTotal']['suspectedTotal']
    b[i]['curesTotal'] = b[i]['countryTotal']['curesTotal']
    b[i]['deathsTotal'] = b[i]['countryTotal']['deathsTotal']
    b[i]['treatingTotal'] = b[i]['countryTotal']['treatingTotal']
    _ = b[i].pop('countryTotal','404')
    _ = b[i].pop('countryIncr','404')
b = pd.DataFrame(b)
b.to_csv('daily/country_'+yesterday+'.csv',index=0)

for id,name in zip(b.id,b.name):
    url = 'https://i.snssdk.com/forum/ncov_data/?country_id=["%s"]&country_name=%s&click_from=overseas_epidemic_tab_list&data_type=[1,4,5,6]'
    url2 = url % (id,name)
    print(url2)
    c = requests.get(url2).json()
    d = json.loads(c['country_data'][id])['provinces']
    try:
        for i in range(len(d)):
            d[i]['updateDate'] = yesterday
            d[i]['confirmedTotal'] = d[i]['total']['confirmedTotal']
            d[i]['suspectedTotal'] = d[i]['total']['suspectedTotal']
            d[i]['curesTotal'] = d[i]['total']['curesTotal']
            d[i]['deathsTotal'] = d[i]['total']['deathsTotal']
            d[i]['treatingTotal'] = d[i]['total']['treatingTotal']
            _ = d[i].pop('total','404')
            _ = d[i].pop('incr','404')
        pd.DataFrame(d).to_csv('daily/'+name+id+'.csv',index=0)
    except:
        print('no data')
