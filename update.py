# 每日1:00新更新前一日数据
import os, time
import pandas as pd
import requests, json
from datetime import timedelta
def get_yesterday():
    t = time.localtime(time.time())
    d, m = t.tm_mday - 1,  t.tm_mon
    if d == 0:
        if m in [1,3,5,7,8,10,12]:
            d = 31
        elif m == 2:
            if t.tm_year % 4 == 0:
                d = 29
            else:
                d = 28
        else:
            d = 30
        m -=1
    return m, d
def get_today():
    t = time.localtime(time.time())
    d, m = t.tm_mday,  t.tm_mon
    return m, d

def extract_data(clean):
    a = clean
    wordwide_his = a[a['province'].isnull()]
    prov_his = a[(-a['province'].isnull()) & (a['city'].isnull())]
    city_his = a[-a['province'].isnull() & -a['city'].isnull()]
    wordwide_his.to_csv('lastest/worldwide_history.csv',index=False)
    prov_his.to_csv('lastest/province_history.csv',index=False)
    city_his.to_csv('lastest/city_history.csv',index=False)

m, d = get_yesterday()
M, D = get_today()
yesterday = '2020-%02d-%02d' % (m, d)
today = '2020-%02d-%02d' % (M, D)

# 备份数据
os.system('cp lastest/clean.csv archive/clean' + yesterday + '.backup')
clean = pd.read_csv('lastest/clean.csv')
# 提取头条上一日的数据；实时数据，所以最新一日的还没记录完整
# 例如：20号上午1:00 获取 19号 数据最可靠。
#tturl_orig = 'https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839'
print('getting data ...')
tturl_github = 'https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv'
tt = pd.read_csv(tturl_github)
tt.to_csv('lastest/'+today+'.csv')
columns = ['date','country','province','city','confirmed','suspected', 'cured', 'dead']
tt = tt[columns]
tt = tt[tt.date == yesterday]

# 是否需要更新：
if max(clean.date) < yesterday:
    clean = clean.append(tt)
    clean.to_csv('lastest/clean.csv')
    extract_data(clean)
    os.system('Rscript update.R')
    open('lastest/update.log','a').write('Added '+yesterday+ ' data')
else:
    print('You have updated!')
