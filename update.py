# 每日早上 1:00 更新前一日的全部数据
import pandas as pd
import os, time
from datetime import timedelta

# 获取前一日的日期
def get_time():
    t = time.localtime(time.time())
    d, m = t.tm_mday,  t.tm_mon
    return m, d
m, d = get_time()

# 判断是否已经更新
update_time = open('lastest/update','r').read()
if update_time != '2020-%02d-%02d' % (m, d):
    update_time = '2020-%02d-%02d' % (m, d)
    # 加载 lastest historical data
    df = pd.read_csv('lastest/city.csv')
    # 增量更新
    shell = "wget http://69.171.70.18:5000/data/city_level_2020-%02d-%02dT10.csv -P lastest/" % (m,d)
    os.system(shell)
    columns = ['date','provinceShortName','city.cityName','city.confirmedCount','city.curedCount','city.deadCount','city.suspectedCount',
               'confirmedCount','suspectedCount','curedCount','deadCount','comment']
    tmp = pd.read_json('lastest/' + 'city_level_2020-%02d-%02dT10.csv' % (m,d))
    tmp['date'] = update_time
    tmp['date'] = pd.to_datetime(tmp['date']) - timedelta(days=1)
    df = df.append(tmp[columns])
    #df.sort_values("date",inplace=True)
    df.to_csv('lastest/city.csv',index=0)
    # 导出 rds 
    os.system('Rscript csv2rds.R')
    # clear
    open('lastest/update','w').write(update_time)
else:
    print('everything is updated')
