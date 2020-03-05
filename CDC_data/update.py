import pandas as pd
import json, os, time
def yesterday():
    t = time.localtime(time.time())
    d, m = t.tm_mday - 1,  t.tm_mon
    if d == 0:
        if m in [1,2,4,6,8,9,11]:
            d = 31
        elif m == 3:
            if t.tm_year % 4 == 0:
                d = 29
            else:
                d = 28
        else:
            d = 30
        m -=1
    return m, d
m, d = yesterday()
cn_url = 'https://ncportal.esrichina.com.cn/JKZX/yq_2020%02d%02d.json' % (m,d)
gb_url = 'https://ncportal.esrichina.com.cn/JKZX/gb_yq_2020%02d%02d.json' % (m,d)
def prase_json(j,dat='2020-%02d-%02d' % (m,d)):
    l = []
    header = ['date'] + list(j['features'][0]['properties'].keys())
    for i in range(len(j['features'])):
        tmp = j['features'][i]['properties']
        l.append([dat] + list(tmp.values()))
    return(pd.DataFrame(l,columns=header))

gb = pd.read_csv('lastest/cdc_gb.csv')
cn = pd.read_csv('lastest/cdc_cn.csv')
shell1 = 'wget ' + gb_url + ' -O global/gb_yq_2020%02d%02d.json' % (m,d)
shell2 = 'wget ' + cn_url + ' -O nation/yq_2020%02d%02d.json' % (m,d)
os.system(shell1)
os.system(shell2)

with open('global/gb_yq_2020%02d%02d.json' % (m,d)) as f_in:
    j = json.load(f_in)
    df = prase_json(j)
    column = ['date','name_cn','地区国家','累计确诊','新增确诊']
    clean = df[column]
    new_gb = clean[clean['累计确诊'] > 0]
    gb = gb.append(new_gb)
    gb.drop_duplicates(inplace=True)
    gb.to_csv('lastest/cdc_gb.csv',index=0)
    
with open('nation/yq_2020%02d%02d.json' % (m,d)) as f_in:
    j = json.load(f_in)
    df = prase_json(j)
    column = ['date','name','省份','新增疑似','累计疑似','新增确诊','累计确诊','新增死亡','累计死亡']
    clean = df[column]
    new_cn = clean[clean['累计确诊'] > 0]
    cn = cn.append(new_cn)
    cn.drop_duplicates(inplace=True)
    cn.to_csv('lastest/cdc_cn.csv',index=0)

os.system('Rscript csv2rds.R')
