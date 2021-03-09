"""
Pseudo-code :

1) Ask for the user's address.
2) Retrieve the GPS coordinates of this address (latitude, longitude) thanks to the government API.
3) Loop on the CSV and calculate the distance between the address and the CSV's cities, to do so we have to convert Lambert 93 coordinates into GPS coordinates.
4) Display the datas corresponding to the minimum distance value for each operators.

"""

import pandas as pd
import numpy as np
import requests

#We install the environment to be able to convert Lambert 93 coordinates into GPS coordinates.
from pyproj import CRS
crs_4326 = CRS("WGS84")
crs_proj = CRS("EPSG:2154")
from pyproj import Transformer
transformer = Transformer.from_crs(crs_proj, crs_4326)

address = input ("Enter your address: ") #We ask for the adress of the user.

#We retrieve the GPS coordinates thanks to the Government API.
url = f'https://api-adresse.data.gouv.fr/search/?q={address}'
urlfile = requests.get(url)
data_coordinates = urlfile.json()
x = data_coordinates['features'][0]['geometry']['coordinates'][0]
y = data_coordinates['features'][0]['geometry']['coordinates'][1]

#We convert the CSV into a dataframe
df_csv = pd.read_csv("/Users/Tom/Downloads/Papernest test/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv", delimiter= ";")
#We create a colomn named 'Distance' and initialize the value to 1000.00
df_csv['Distance'] = 1000.00

#The following line of code is to avoid the SettingWithCopyWarning warning
pd.options.mode.chained_assignment = None

#We loop on the csv/dataframe to calculate the distance between the address and the cities present in the csv.
for i in range(1, df_csv.shape[0]):
  y2,x2 = transformer.transform(df_csv['X'][i],df_csv['Y'][i])
  dist = np.sqrt((x-x2)**2 + (y-y2)**2)
  df_csv['Distance'][i] = dist

result = {}

#We look for the index of the minimum distance for each operator and we retrieve the data of the corresponding row.
idx_orange = df_csv[df_csv['Operateur'] == 20801].idxmin(axis=0)
result['Orange'] = {'2G': df_csv['2G'][idx_orange['Distance']] == 1, '3G': df_csv['3G'][idx_orange['Distance']] == 1, '4G': df_csv['4G'][idx_orange['Distance']] == 1}

idx_sfr = df_csv[df_csv['Operateur'] == 20810].idxmin(axis=0)
result['SFR'] = {'2G': df_csv['2G'][idx_sfr['Distance']] == 1, '3G': df_csv['3G'][idx_sfr['Distance']] == 1, '4G':df_csv['4G'][idx_sfr['Distance']] == 1}

idx_free = df_csv[df_csv['Operateur'] == 20815].idxmin(axis=0)
result['Free'] = {'2G': df_csv['2G'][idx_free['Distance']] == 1, '3G': df_csv['3G'][idx_free['Distance']] == 1, '4G':df_csv['4G'][idx_free['Distance']] == 1}

idx_bouygues = df_csv[df_csv['Operateur'] == 20820].idxmin(axis=0)
result['Bouygues'] = {'2G': df_csv['2G'][idx_bouygues['Distance']] == 1, '3G': df_csv['3G'][idx_bouygues['Distance']] == 1, '4G':df_csv['4G'][idx_bouygues['Distance']] == 1}

#We display the data in a dictionnary.
print(result)


#Note:
#We can add a condition to check if the minimum distance between the address and the cities are not too important.
#For example if we don't have data about Corse, it's maybe not pertinent to display the result of the closest french metropolitan city.







