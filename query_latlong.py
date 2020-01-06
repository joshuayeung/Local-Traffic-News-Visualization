import sqlalchemy
yourdb = sqlalchemy.create_engine('mssql+pyodbc://USER:PASSWORD@DATABASE_IP\\INSTANCE_NAME/database?driver=SQL+Server+Native+Client+11.0')

import pandas as pd

df = pd.read_sql('SELECT [news_id],[title],[publish_time] FROM [cmhk].[dbo].[nqm_web_traffic_news] WHERE [publish_time] >= DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()), -1)', yourdb)

queue_end = df.title.str.extract(r'龍尾：(\w+)')

from geopy.geocoders import Nominatim

locator = Nominatim(user_agent='myGeocoder', timeout=3)

import numpy as np
not_found_place = []

from sqlalchemy import exc

for record in queue_end[0]:
    if record is not np.nan:
        location = locator.geocode(record)
        if location is not None:
            #print("{} Latitude = {}, Longitude = {}".format(record, location.latitude, location.longitude))
            try:
                yourdb.execute('''INSERT INTO relation_table_location_position (location, latitude, longitude)
                VALUES (N'{}', '{}', '{}')'''.format(record, location.latitude, location.longitude))
            except exc.IntegrityError:
                pass #or any other action
        else:
            #print("{}".format(record))
            try:
                yourdb.execute('''INSERT INTO relation_table_location_position (location, latitude, longitude)
                VALUES (N'{}', NULL, NULL)'''.format(record))
            except exc.IntegrityError:
                pass #or any other action
            not_found_place.append(record)
