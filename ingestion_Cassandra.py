import pandas as pd
import warnings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import date
from datetime import datetime

warnings.filterwarnings('ignore')
today = date.today()

CASSANDRA_HOST = ['localhost'] 
CASSANDRA_PORT = 9042
CASSANDRA_DB = "weather"
CASSANDRA_TABLE = "France"
CASSANDRA_LOGIN = "cassandra"
CASSANDRA_PWD = "cassandra"
auth_provider = PlainTextAuthProvider(username=CASSANDRA_LOGIN, password=CASSANDRA_PWD)



def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)
#on force ici a repecter le datframe de pandas lors de la recuperation des données
try:
    cluster = Cluster(protocol_version=3,contact_points=CASSANDRA_HOST,load_balancing_policy=None,port=CASSANDRA_PORT, auth_provider=auth_provider)
    session =cluster.connect()
    session.row_factory = pandas_factory
    print("Connection established")
except ValueError:
    print("Oops!  échec de connexion cluster.  Try again...")

#creation du key space
session.execute("CREATE KEYSPACE IF NOT EXISTS france WITH REPLICATION={'class':'SimpleStrategy','replication_factor':1};")

#Creation de type Covid
# session.execute("CREATE TYPE IF NOT EXISTS  France.villeType ( city text, country text, temp float, temp_max float,  temp_min float, humidity float, pressure float, sky text, sunrise float, sunset float, wind float, wind_deg float, dt date, cloudiness int);")
session.execute("CREATE TABLE IF NOT EXISTS  france.villes (city text, country text, temp float, temp_max float,  temp_min float, humidity float, pressure float, sky text, sunrise text, sunset text, wind float, cloudiness int, dt text, primary key (city));")


rows=session.execute('Select * from france.villes;')
df_results = rows._current_rows
# df_results.head()
# print(type(df_results))
# print(df_results.head())

session = cluster.connect('france')  
session.row_factory = pandas_factory
session.default_fetch_size = 10000000 #needed for large queries, otherwise driver will do pagination. Default is 50000.

query_insert="INSERT INTO france.villes  (city, country, temp, temp_max,temp_min, humidity,pressure, sky,sunrise, sunset,  wind,cloudiness,dt) VALUES ($${}$$, '{}', {}, {},{}, {}, {}, '{}','{}', '{}', {}, {},'{}');"

df_weather = pd.read_csv("./weatherOpenMap.csv", sep = ",")

for ct in df_weather.index:
     
    CQL_query = query_insert.format(df_weather["city"][ct].replace("'", ""),df_weather["country"][ct],df_weather['temp'][ct],\
                df_weather["temp_max"][ct],df_weather["temp_min"][ct],df_weather['humidity'][ct],df_weather["pressure"][ct],\
                df_weather["sky"][ct],df_weather['sunrise'][ct],df_weather['sunset'][ct],df_weather['wind'][ct],df_weather["cloudiness"][ct],\
                df_weather["dt"][ct]) 
    #print(CQL_query)
    #break
    # print(CQL_query)
    # break
    session.execute(CQL_query)


#Executer une requete pour tester
rows = session.execute('SELECT * FROM france.villes ;')
df_countries = rows._current_rows
df_countries.head()
# print(df_weather.head())




cluster.shutdown()