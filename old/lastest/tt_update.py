import time, os, json
import pandas as pd

now_time = time.localtime()
now_time = time.strftime("%Y-%m-%d",now_time)
url= 'https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv'
os.system('wget '+ url + ' -O lastest/' + now_time )
a = pd.read_csv('lastest/'+now_time)

wordwide_his = a[a['province'].isnull()]
prov_his = a[(-a['province'].isnull()) & (a['city'].isnull())]
city_his = a[-a['province'].isnull() & -a['city'].isnull()]
wordwide_his.to_csv('worldwide_history.csv',index=False)
prov_his.to_csv('province_history.csv',index=False)
city_his.to_csv('city_history.csv',index=False)

os.system('Rscript update.R')
