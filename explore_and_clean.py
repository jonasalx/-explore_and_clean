from typing import List
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import time

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

print("PRIMER ANALISIS, COLUMNAS CON NAN")
time.sleep(3)

#PARTE 2

def setSnakeCase(list):
    rename = {}
    for l in list:
        rename[l] = re.sub(r'(?<!^)(?=[A-Z])', '_', l).lower()
    return rename

# luego aplico el metodo rename con el diccionario creado en la funcion
new_columns = setSnakeCase( autos.columns )
autos.rename( columns = new_columns, inplace=True )

print("Cree la funcion setSnakeCase porque automaticamente me hace la transformacion... en cualquier caso, dataframe o lista cualquiera")
print( autos.columns )
time.sleep(5)



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

print("Muestro values_count() por cada columna")
obs = """
        month_of_registration, QUE REPRESENTA MES 0 ??
        nr_of_pictures, TODOS EN 0, se podria eliminar columna
        year_of_registration, valores no logicos 1000 al 9999
        price, valores muy bajos e incluso 0
        price, valores muy altos no logicos (2147483647)
        """
print(obs)
time.sleep(5)

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

print("Renombro columnas")
print( autos.columns )
time.sleep(5)


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
#la fila entera
#autos[autos["price"].between(0, 500)]= np.nan
#autos[autos["price"] > 5000000 ] = np.nan

#solo el valor en la columna
autos.loc[autos["price"] <= 500, "price"] = np.nan
autos.loc[autos["price"] > 5000000, "price"] = np.nan

#depende las operaciones que siguen, pandas no considerar nan para algunas operaciones

#observacion de valores restantes
print("")
print( autos.price.describe() )
print("Dejo en NAN price <= 500 y > 5000000")
time.sleep(5)


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

print("")
print( "2016-03-05 14:00:00 - 2016-03-05 15:00:00" )
print("Que tiene de especial esta fecha, por que tiene tantos rastreos ?? ")
time.sleep(5)


################
# date_crawled #
################
autos.ad_created.str[: 10].value_counts().sort_index()
autos.ad_created.str[: 10].value_counts().sort_values(ascending=False).head(50)
autos.ad_created.str[: 10].value_counts().sort_index(ascending=False).head(50)
#se marca un incremendo desde 2016-03-03      415
print("Analisando ad_created se marca un incremento desde 2016-03-03      415")
print("Grafico de dispersion")
time.sleep(3)

#podemos graficar la dispersion
c = autos.ad_created.str[: 10].value_counts().sort_index()
df = pd.DataFrame([[key, c[key]] for key in c.keys()], columns=['date', 'count'])
disp = df.plot( "date","count",  kind="scatter" )
plt.show()



#autos.last_seen.value_counts().sort_index()
#autos.last_seen.value_counts(normalize = True, dropna = False).sort_index()
autos.last_seen.value_counts(normalize = True, dropna = False).sort_index().describe()

#TERMINAR


#registration_year
#autos[autos["registration_year"] < 1900 ] = np.nan
#autos[autos["registration_year"] > 2022 ] = np.nan

autos.loc[autos["registration_year"] < 1900, "registration_year"] = np.nan
autos.loc[autos["registration_year"] > 2022, "registration_year"] = np.nan

autos.registration_year.describe()

obs = """
count    371346.000000              bajo la cantidad debido a no considerar nan (<1900 & >2022)
mean       2003.348489              min y max coinciden por las reglas de nan aplicadas
std           7.776980
min        1910.000000
25%        1999.000000              el 25% se encuentra hasta 1999
50%        2003.000000              el 50% se encuentra hasta 2003
75%        2008.000000
max        2019.000000
"""
print("Limpio registration_year < 1900 & > 2022 (primera limpieza)")
print(obs)
print("Adicional agrego histograma uqe permite comparar los datos graficamente")
time.sleep(3)


#para ver mejor los minimos, maximos y por que el promedio
#histograma
plt.hist(autos.registration_year)



#PARTE 6

#considerando valores iniciales
fuera = autos[ (autos["registration_year"] < 1900) | (autos["registration_year"] > 2016 )]
#total de fuera de limites 14748 
#detalle
fuera.registration_year.value_counts().sort_values(ascending=False)

#limpiando
#autos[autos["registration_year"] > 2016 ] = np.nan
autos.loc[autos["registration_year"] > 2016, "registration_year"] = np.nan
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

autos.registration_year.value_counts(normalize = True).sort_values(ascending=False)


#PARTE 7

list_brand = autos.brand.value_counts(normalize = True).sort_values(ascending=False).head(20)
# solo aplico un conteo y ordeno descendentemente, las marcas a analizar son las primeras 20
"""
volkswagen        0.211634
bmw               0.115898
mercedes_benz     0.103787
opel              0.098398
audi              0.094281
ford              0.063324
renault           0.043263
peugeot           0.029848
fiat              0.023625
seat              0.018388
skoda             0.016721
smart             0.015395
mazda             0.015003
toyota            0.013854
citroen           0.013848
nissan            0.013074
hyundai           0.010368
mini              0.010204
sonstige_autos    0.009386
volvo             0.009115
"""

brand_mean = {}
for b in list_brand.index:
    brand_mean[b] =  round( autos[ autos["brand"] == b ].price.mean() ,2 )

print(brand_mean)

#grafico
df = pd.DataFrame([[key, brand_mean[key]] for key in brand_mean.keys()], columns=['brand', 'amount'])
df.plot( "brand","amount",  kind="scatter" )
plt .show()

df.sort_values("amount",ascending=False)


"""
18  sonstige_autos  24644.12
17            mini  10144.93
4             audi   9515.96
1              bmw   8885.65
2    mercedes_benz   8785.91
10           skoda   6697.20
0       volkswagen   5939.42
16         hyundai   5842.70
19           volvo   5718.82
13          toyota   5447.91
15          nissan   5316.48
9             seat   5009.86
12           mazda   4532.59
5             ford   4444.91
14         citroen   4086.17
11           smart   3694.98
7          peugeot   3578.17
3             opel   3527.65
8             fiat   3383.03
6          renault   2865.77
"""

# el promedio de precios sigue el comun a las marcas, los precios mas altos estan en marcas como mini, audi,bmw
# mientas que los precios mas bajos estan en marcas como peugeot, fiat, renault entre otras



#PARTE 8
#puedo crear las series de la sigueinte forma
s1 = pd.Series(brand_mean, index= list_brand.index )

# pero creo que este proceso tiene menos pasos
data_mean = {}
for b in list_brand.index:
    data_mean[b] =  [ round( autos[ autos["brand"] == b ].price.mean() ,2 ) ,
                        round( autos[ autos["brand"] == b ].odometer_km.mean() ,2 ) ]
    
df = pd.DataFrame([[key, data_mean[key][0], data_mean[key][1]] for key in data_mean.keys()], columns=['brand', 'amount','km'])

df.km.mean()
# el promedio de km es  118.222
# no se ve una relacion entre el precio y el kilometraje, tanto altos y bajos precios tienen kilometraje similar


#PARTE 9

#recorro para ver datos de columnas en aleman
for c in autos.columns:
    print( autos.eval(c).head(10) )

#vehicle_type
autos.vehicle_type.unique()

autos.loc[autos["vehicle_type"] == "andere", "vehicle_type"] = "other"
autos.loc[autos["vehicle_type"] == "kleinwagen", "vehicle_type"] = "small car"
autos.loc[autos["vehicle_type"] == "cabrio", "vehicle_type"] = "convertible"

#gearbox
autos.gearbox.unique()
#autos[autos["gearbox"] == "manuell" ] = "manually"
#autos[autos["gearbox"] == "automatik" ] = "automatic"
autos.loc[autos["gearbox"] == "manuell", "gearbox"] = "manually"
autos.loc[autos["gearbox"] == "automatik", "gearbox"] = "automatic"



#fuel_type
autos.fuel_type.unique()
autos.loc[autos["fuel_type"] == "benzin", "fuel_type"] = "gasoline"
autos.loc[autos["fuel_type"] == "andere", "fuel_type"] = "other"
autos.loc[autos["fuel_type"] == "elektro", "fuel_type"] = "electro"



#pasar fecha ad_created a int
#no siempre funciona ??

#col_created = autos.ad_created
#for f in col_created.index:
#    col_created[f] = int( col_created[f][:10].replace("-",""))