import lxml, requests,time
import pandas as pd
from lxml import html 
from datetime import timedelta


url = 'https://coronavirus.1point3acres.com/'
source = requests.get(url).text
today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
yesterday = pd.to_datetime(today) - timedelta(days=1)
yesterday = str(yesterday).split()[0]
sel = html.fromstring(source) 
# America data table
city = sel.xpath('//*[@id="map"]/div[2]/div[1]/div[4]/div/div/span[1]/text()')
cum_confirm = sel.xpath('//*[@id="map"]/div[2]/div[1]/div[4]/div/div/span[2]/text()')
cum_dead = sel.xpath('//*[@id="map"]/div[2]/div[1]/div[4]/div/div/span[3]/text()')
dead_rate = sel.xpath('//*[@id="map"]/div[2]/div[1]/div[4]/div/div/span[4]/text()')
# America data header
header = sel.xpath('//*[@id="map"]/div[2]/div[1]/div[4]/header/span/text()')
table = pd.DataFrame({
    '时间':yesterday,
    '国家':'美国',
    header[0]:city,
    header[1]:cum_confirm,
    header[2]:cum_dead,
    header[3]:dead_rate,
})
# Canada data table
city = sel.xpath('//*[@id="map"]/div[2]/div[2]/div[4]/div/div/span[1]/text()')
cum_confirm = sel.xpath('//*[@id="map"]/div[2]/div[2]/div[4]/div/div/span[2]/text()')
cum_dead = sel.xpath('//*[@id="map"]/div[2]/div[2]/div[4]/div/div/span[3]/text()')
dead_rate = sel.xpath('//*[@id="map"]/div[2]/div[2]/div[4]/div/div/span[4]/text()')
# Canada data header
header = sel.xpath('//*[@id="map"]/div[2]/div[2]/div[4]/header/span/text()')
table2 = pd.DataFrame({
    '时间':yesterday,
    '国家':'加拿大',
    header[0]:city,
    header[1]:cum_confirm,
    header[2]:cum_dead,
    header[3]:dead_rate,
})
table2.append(table).to_csv('daily/northamerica_'+today+'.csv',index = 0)
