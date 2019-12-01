"""
Script for coordinates getting by addresses and further distance matrices computation.
Not required, actually, as much of the work is done by hands. 
Final precomputed distance matrices are provided.
"""



import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim, GoogleV3, Yandex
from yandex_geocoder import Client
import seaborn as sns
from tqdm import tqdm_notebook as tqdm
import numpy as np
from geopy import distance

filename = "hackaton_data_5post.csv"
data = pd.read_csv(filename)

def get_addresses_sparsed(filename_in, filename_out, sub):
    addresses = []
    with open(filename_in, "r") as file_in:
        with open(filename_out, "w") as file_out:
            for line in file_in:
                if line[:len(sub)] == sub:
                    line = line.rstrip()
                    if line not in addresses:
                        addresses.append(line)
                        file_out.write(line + "\n")
    print(len(addresses), addresses[:2])
    return addresses

geolocator = Nominatim()
def get_coord(x): 
    location = geolocator.geocode(x, timeout=100)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None
        
replace_list = ["г.", "рп.", "п.", "стр.", 
                "пр-т", "-й", "пр-д", "мкр.", "мкр", "б-р", "пгт.", "с.", "д."]
addresses = []
filename = "coordinates_1.csv"
file = open(filename, "w")
for i, row in tqdm(data.iterrows(), total=len(data)):
    address = row["ADDRESS"]
    for r in replace_list:
        if r[-1] == ",":
            address = address.replace(r, ",")
        else:
            address = address.replace(r, "")
    address = address.split(",")[:3]
    if len(address) > 2:
        address[2] = address[2].lstrip().split(" ")[0]
        address[2] = address[2].split("/")[0]
    if len(address) > 1:
        if len(address[1].split()) > 1:
            address[1] = " ".join(address[1].split()[:-1])
    address = [v.strip() for v in address]
    address = ", ".join(address)
    location = get_coord(address)
    file.write(str(i) + " ")
    if location:
        print("{:d} {:3d} {:50s}".format(1, i, row["ADDRESS"]), location, address)
        addresses.append(location)
        file.write(str(location[0]) + " " + str(location[1])for c in coordinates:)
    else:
        print("{:d} {:3d} {:50s} {:40s}".format(0, i, row["ADDRESS"], address), "NONE")
        addresses.append(None)
        file.write("-100000 -100000")
    file.write("\n")
        
file.close()


addresses = []
file = open("coordinates_1.csv", "r")
for line in file:
    addresses.append([float(line.split()[1]), float(line.split()[2])])
file.close()

distance_matrix = np.zeros((len(addresses), len(addresses)))
for i in tqdm(range(len(addresses))):
    for j in range(len(addresses)):
        distance_matrix[i, j] = distance.distance(addresses[i], addresses[j]).km=
        
np.save("distance_matrix.npy", distance_matrix)

min_distances = []
for i in range(len(addresses)):
    min_distance = 1e9
    for j in range(len(addresses)):
        if i == j:
            continue
        min_distance = min(distance_matrix[i, j], min_distance)
    min_distances.append(min_distance)
min_distances = np.array(min_distances)

np.save("min_distances.npy", min_distances)


def dum(x):
    if str(x) == 'nan':
        return 0
    else :
        return 1 
data['dum0'] = data['Postamat_daily'].apply(dum)
data['dum1'] = data['cashbox_daily'].apply(dum)
data['sum_dum'] = data['dum0'] + data['dum1']
data_exs = data[data['sum_dum'] > 0]

values = data.sum_dum.values
indices = np.where(values > 0)
indices = indices[0].tolist()

distance_matrix_1 = np.zeros((len(indices), len(indices)))
for i in range(len(indices)):
    for j in range(len(indices)):
        distance_matrix_1[i, j] = distance_matrix[indices[i], indices[j]]
        
np.save("distance_matrix_1.npy", distance_matrix_1)

file = open("coordinates_streets.csv", "w")
for i, row in data.iterrows():
    file.write("\t".join([str(i), str(coordinates[i, 0]), str(coordinates[i, 1]), row["ADDRESS"]]) + "\n")
file.close()

coordinates_ozon = []
indices_ozon = []
replace_list = ["г.", "п.", "мкр.", " мкр", "с.", "пгт", " по ", " рп ",
                "пл.", "пр.", "ул.", "ш.", "пер.", "проезд", " прос",
                " дом ", "д.", "к.", "стр.", "корп."]
file = open("coordinates_ozon_2.csv", "w")
for i, aaa in enumerate(addresses_ozon):
    a = aaa.split(",")
    aa = []
    for v in a:
        for r in replace_list:
            v = v.replace(r, "")
        aa.append(v.strip())
    aa = aa[1:]
    if len(aa) > 3:
        if "р-н" in aa[0]:
            aa = aa[1:]
        elif aa[0] == "Тула":
            aa = [aa[0]] + aa[2:]
        else:
            aa = aa[:3]
    aa[-1] == str([v for v in aa[-1] if v.isdigit()])
            
    a = ", ".join(aa)
    c = get_coord(a)
    print(i, a, c)
    if c:
        file.write(aaa + "\t" + a + "\t" + str(c[0]) + "\t" + str(c[1]) + "\n")
        indices_ozon.append(i)
    coordinates_ozon.append(c)
    
file.close()

coordinates_ozon = np.array(coordinates_ozon)[indices_ozon]
distance_matrix_ozon = np.zeros((len(coordinates), len(coordinates_ozon)))
for i in range(len(coordinates)):
    for j in range(len(coordinates_ozon)):
        distance_matrix_ozon[i, j] = distance.distance(coordinates[i], coordinates_ozon[j]).km
        
min_distances_ozon = np.min(distance_matrix_ozon, axis=-1)

np.save("distance_matrix_ozon.npy", distance_matrix_ozon)
np.save("min_distances_ozon.npy", min_distances_ozon)