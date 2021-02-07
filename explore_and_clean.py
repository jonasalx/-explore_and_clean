from typing import List
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

#PARTE 1
autos = pd.read_csv("autos.csv/autos.csv")
#print(autos.info())
#print(autos.head())
#print( autos.dtypes )

nan = autos.isna().sum().to_dict()
#    #print( len(autos[pd.isnull(  )]) ) 

#Columnas con valores NAN
for c in nan:
    if nan.get(c) > 0:
        print( c+" => "+ str( nan.get(c) ) )


#PARTE 2

def setSnakeCase(list):
    rename = {}
    for l in list:
        rename[l] = re.sub(r'(?<!^)(?=[A-Z])', '_', l).lower()
    return rename

new_columns = setSnakeCase( autos.columns )
autos.rename( columns = new_columns, inplace=True )
#autos.columns

# Cree la funcion setSnakeCase porque automaticamente me hace la transformacion... en cualquier caso, dataframe o lista cualquiera
# luego aplico el metodo rename con el diccionario creado en la funcion


#PARTE 3
autos.describe()
p = autos.price
k = autos.kilometer

"""
['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
'vehicle_type', 'year_of_registration', 'gearbox', 'power_p_s', 'model',
'kilometer', 'month_of_registration', 'fuel_type', 'brand',
'not_repaired_damage', 'date_created', 'nr_of_pictures', 'postal_code','last_seen']
"""

list = autos.columns
for o in list:
    print("=================================")
    #total valores distintos
    print( autos.eval(o).unique().size )

    #contador valores
    print( autos.eval(o).value_counts() )

    print("=================================")

#autos.month_of_registration.value_counts()
# QUE REPRESENTA MES 0 ??

#autos.nr_of_pictures.value_counts()
#TODOS EN 0 ??
#SE PODRIA DESCARTAR

#autos.year_of_registration.value_counts()
# 1000 al 9999
# VALORES EXCEDIDOS ???

# price TIENE VALOR 0???
# 0         10778
#autos.price.max()
#2147483647     ???


new_columns["kilometer"] = "odometer_km"
new_columns["year_of_registration"] = "registration_year"
new_columns["month_of_registration"] = "registration_month"
new_columns["not_repaired_damage"] = "unrepaired_damage"
new_columns["date_created"] =  "ad_created"
autos.rename( columns = new_columns, inplace=True )

autos.odometer_km.dtypes #int64
autos.price.dtypes #int64
#price y odometer_km ya me aparecen como enteros de 64 bits
# no seria necesario
#autos['price'] = autos['price'].astype('int64')



"""
date_crawled             object
name                     object
seller                   object
offer_type               object
price                     int64
abtest                   object
vehicle_type             object
year_of_registration      int64
gearbox                  object
power_p_s                 int64
model                    object
kilometer                 int64
month_of_registration     int64
fuel_type                object
brand                    object
not_repaired_damage      object
date_created             object
nr_of_pictures            int64
postal_code               int64
last_seen                object
"""

#PARTE 4

autos.price.value_counts().sort_index(ascending=True).head()
autos.price.value_counts().sort_index(ascending=False).head()

autos.odometer_km.value_counts().sort_index(ascending=True).head()
autos.odometer_km.value_counts().sort_index(ascending=False).head()


#paso a nan valores extremos de price
autos[autos["price"].between(0, 500)]= np.nan
autos[autos["price"] > 5000000 ] = np.nan

#depende las operaciones que siguen, pandas no considerar nan para algunas operaciones

#observacion de valores restantes
autos.price.describe()


#PARTE 5

################
# date_crawled #
################

#autos.date_crawled.value_counts().sort_index()
#autos.date_crawled.value_counts(normalize = True, dropna = False).sort_index()
autos.date_crawled.value_counts(normalize = True, dropna = False).sort_index().describe()
#los datos se ven bien distribuidos

#por minutos
autos.date_crawled.str[: 16].value_counts()

#por hora
autos.date_crawled.str[: 13].value_counts()
autos.date_crawled.str[: 13].value_counts().sort_values(ascending=False).head(20)
# 2016-03-05 14    2305
# Sale de lo normal, ese dia y esa hora 

# no identifico algo anormal en la distribucion de esa hora 
autos_hour_14 = autos[autos["date_crawled"].between("2016-03-05 14:00:00", "2016-03-05 15:00:00") ]
autos_hour_14.date_crawled.describe()
autos_hour_14.date_crawled.value_counts().sort_index().describe()

#que tiene de especial esta fecha, por que tiene tantos "rastreos"




################
# date_crawled #
################
autos.date_created.str[: 10].value_counts().sort_index()
autos.date_created.str[: 10].value_counts().sort_values(ascending=False).head(50)
autos.date_created.str[: 10].value_counts().sort_index(ascending=False).head(50)
#se marca un incremendo desde 2016-03-03      415

#podemos graficar la dispersion
c = autos.date_created.str[: 10].value_counts().sort_index()
df = pd.DataFrame([[key, c[key]] for key in c.keys()], columns=['date', 'count'])
disp = df.plot( "date","count",  kind="scatter" )
plt.show()



#autos.last_seen.value_counts().sort_index()
#autos.last_seen.value_counts(normalize = True, dropna = False).sort_index()
autos.last_seen.value_counts(normalize = True, dropna = False).sort_index().describe()

#TERMINAR


#registration_year
autos[autos["registration_year"] < 1900 ] = np.nan
autos[autos["registration_year"] > 2022 ] = np.nan

autos.registration_year.describe()
"""
count    371346.000000              bajo la cantidad debido a no considerar nan (<1900 & >2022)
mean       2003.348489              min y max coinciden por las reglas de nan aplicadas
std           7.776980
min        1910.000000
25%        1999.000000              el 25% se encuentra hasta 1999
50%        2003.000000              el 50% se encuentra hasta 2003
75%        2008.000000
max        2019.000000
"""

#para ver mejor los minimos, maximos y por que el promedio
#histograma
plt.hist(autos.registration_year)



#PARTE 6

autos[autos["registration_year"] > 2016 ] = np.nan
"""
count    356780.000000
mean       2002.779805
std           7.395775
min        1910.000000
25%        1999.000000
50%        2003.000000
75%        2008.000000
max        2016.000000
"""

#es seguro dejar como nan
#ver si se pueden eliminar por completo
