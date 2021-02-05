from typing import List
import numpy as np
import pandas as pd
import re

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


