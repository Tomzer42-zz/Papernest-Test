"""
Pseudo-code :

1) Demander à l'utilisateur d'entrée une adresse
2) Récupérer les données GPS (latitude, longitude) grâce à l'api du gouvernement.
3) Convertir ses données en Lambert 93.
4) Boucler sur le csv et calculer la distance entre toutes l'adresse et les villes du csv
5) Renvoyer les données correspondant à la distance minimale pour chaque opérateur. Si distance trop grande alors on renvoit rien.

"""

import pandas as pd
import numpy as np
import requests


from pyproj import CRS
crs_4326 = CRS("WGS84")
crs_proj = CRS("EPSG:2154")
from pyproj import Transformer
transformer = Transformer.from_crs(crs_proj, crs_4326)

address = input ("Enter your address: ")
url = f'https://api-adresse.data.gouv.fr/search/?q={address}'
urlfile = requests.get(url)
data_coordinates = urlfile.json()
x = data_coordinates['features'][0]['geometry']['coordinates'][0]
y = data_coordinates['features'][0]['geometry']['coordinates'][1]


df_csv = pd.read_csv("/Users/Tom/Downloads/Papernest test/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv", delimiter= ";")
df_csv['Distance'] = 1000.00


pd.options.mode.chained_assignment = None
for i in range(1, df_csv.shape[0]):
  y2,x2 = transformer.transform(df_csv['X'][i],df_csv['Y'][i])
  dist = np.sqrt((x-x2)**2 + (y-y2)**2)
  df_csv['Distance'][i] = dist

result = {}

idx_orange = df_csv[df_csv['Operateur'] == 20801].idxmin(axis=0)
result['Orange'] = {'2G': df_csv['2G'][idx_orange['Distance']] == 1, '3G': df_csv['3G'][idx_orange['Distance']] == 1, '4G': df_csv['4G'][idx_orange['Distance']] == 1}
idx_sfr = df_csv[df_csv['Operateur'] == 20810].idxmin(axis=0)
result['SFR'] = {'2G': df_csv['2G'][idx_sfr['Distance']] == 1, '3G': df_csv['3G'][idx_sfr['Distance']] == 1, '4G':df_csv['4G'][idx_sfr['Distance']] == 1}
idx_free = df_csv[df_csv['Operateur'] == 20815].idxmin(axis=0)
result['Free'] = {'2G': df_csv['2G'][idx_free['Distance']] == 1, '3G': df_csv['3G'][idx_free['Distance']] == 1, '4G':df_csv['4G'][idx_free['Distance']] == 1}
idx_bouygues = df_csv[df_csv['Operateur'] == 20820].idxmin(axis=0)
print(idx_bouygues)
print(idx_bouygues['Distance'])
print(df_csv.iloc[[idx_bouygues['Distance']]])
result['Bouygues'] = {'2G': df_csv['2G'][idx_bouygues['Distance']] == 1, '3G': df_csv['3G'][idx_bouygues['Distance']] == 1, '4G':df_csv['4G'][idx_bouygues['Distance']] == 1}

print(result)










