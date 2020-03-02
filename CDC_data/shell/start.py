import pandas as pd
import json, os, time
# nation data
def get_date(i):
    y = i[3:7]
    m = i[7:9]
    d = i[9:11]
    return(f'{y}-{m}-{d}')

def prase_json(j,dat):
    l = []
    header = ['date'] + list(j['features'][0]['properties'].keys())
    for i in range(len(j['features'])):
        tmp = j['features'][i]['properties']
        l.append([dat] + list(tmp.values()))
    return(pd.DataFrame(l,columns=header))

json_path = 'nation/'
df = pd.DataFrame()
for r in sorted(os.listdir(json_path)):
    with open(json_path+r,'r') as f_in:
        j = json.load(f_in)
        dat = get_date(r)
        df = df.append(prase_json(j,dat))
column = ['date','name','省份','新增疑似','累计疑似','新增确诊','累计确诊','新增死亡','累计死亡']
clean = df[column]
CDC_cn = clean[clean['累计确诊'] > 0]
CDC_cn.drop_duplicates(inplace=True)
CDC_cn.to_csv('lastest/cdc_cn.csv',index=0)

# glabal data
def get_gb_date(i):
    y = i[6:10]
    m = i[10:12]
    d = i[12:14]
    return(f'{y}-{m}-{d}')

def prase_gb_json(j,dat):
    l = []
    header = ['date'] + list(j['features'][0]['properties'].keys())
    for i in range(len(j['features'])):
        tmp = j['features'][i]['properties']
        l.append([dat] + list(tmp.values()))
    return(pd.DataFrame(l,columns=header))

json_path = 'global/'
df = pd.DataFrame()
for r in sorted(os.listdir(json_path)):
    with open(json_path+r,'r') as f_in:
        j = json.load(f_in)
        dat = get_gb_date(r)
        df = df.append(prase_gb_json(j,dat))
column = ['date','NAME','CAPITAL','name_cn','地区国家','累计确诊','新增确诊']
clean = df[column]
CDC_gb = clean[clean['累计确诊'] > 0]
CDC_gb.drop_duplicates(inplace=True)
CDC_gb.to_csv('lastest/cdc_gb.csv',index=0)
