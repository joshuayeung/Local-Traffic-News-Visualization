import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

r = requests.get("http://programme.rthk.hk/channel/radio/trafficnews/index.php")

if r.status_code == requests.codes.ok:
    r.encoding='utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

df_cols = ['title', 'pub_time', 'location']

df = pd.DataFrame(columns=df_cols)

stories = soup.find_all('li', class_='inner')

titles = []
times = []
for s in stories:
    title, time = list(filter(None, re.split(r'\t|\n', s.text)))
    titles.append(title)
    times.append(time)

locations = []
import sqlalchemy
yourdb = sqlalchemy.create_engine('mssql+pyodbc://USER:PASSWORD@DATABASE_IP\\INSTANCE_NAME/database?driver=SQL+Server+Native+Client+11.0')

loc = pd.read_sql("SELECT location FROM relation_table_location_position ORDER BY level, LEN(location) DESC", yourdb)

for title in titles:
    #queue_end
    m = re.search('龍尾：(\w+)', title)
    if m:
        location = m.group(1)
        locations.append(location)
    else:
        m = None
        for index, row in loc.iterrows():
            m = re.search(row[0], title)
            if m:
                location = m.group(0)
                locations.append(location)
                break
        if not m:
            locations.append(None)

dict = {'title': titles, 'publish_time': times, 'location': locations}

df = pd.DataFrame(data=dict)

df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%d HKT %H:%M')

df.sort_values(by=['publish_time'], inplace=True)

# set category
df.loc[df.title.str.contains('關閉'), 'category'] = 'service paused'
df.loc[df.title.str.contains('暫停'), 'category'] = 'service paused'
df.loc[df.title.str.contains('間封'), 'category'] = 'blocked'
df.loc[df.title.str.contains('繁忙'), 'category'] = 'busy'
df.loc[df.title.str.contains('多車'), 'category'] = 'busy'
df.loc[df.title.str.contains('車多'), 'category'] = 'busy'
df.loc[df.title.str.contains('慢車'), 'category'] = 'busy'
df.loc[df.title.str.contains('龍尾'), 'category'] = 'busy'
df.loc[df.title.str.contains('塞車'), 'category'] = 'congestion'
df.loc[df.title.str.contains('擠塞'), 'category'] = 'congestion'
df.loc[df.title.str.contains('意外'), 'category'] = 'accident'
df.loc[df.title.str.contains('回復暢順'), 'category'] = 'normal'
df.loc[df.title.str.contains('回復正常'), 'category'] = 'normal'
df.loc[df.title.str.contains('恢復運作'), 'category'] = 'normal'
df.loc[df.title.str.contains('禁止'), 'category'] = 'blocked'
df.loc[df.title.str.contains('受阻'), 'category'] = 'blocked'
df.loc[df.title.str.contains('不能通車'), 'category'] = 'blocked'
df.loc[df.title.str.contains('封閉'), 'category'] = 'blocked'
df.loc[df.title.str.contains('封路'), 'category'] = 'blocked'
df.loc[df.title.str.contains('恢復'), 'category'] = 'normal'
df.loc[df.title.str.contains('回復'), 'category'] = 'normal'
df.loc[df.title.str.contains('重開'), 'category'] = 'normal'
df.loc[df.title.str.contains('間封措施取消'), 'category'] = 'normal'
df.loc[df.category.isnull(), 'category'] = 'info'

from sqlalchemy import exc

for i in range(len(df)):
    try:
        df.iloc[i:i+1].to_sql(name="nqm_web_traffic_news", if_exists='append', con = yourdb, index=False)
    except exc.IntegrityError:
        pass # We have already extract that news
    except Exception:
        pass #or any other action
