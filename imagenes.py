# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:34:02 2023

@author: lixan
"""

import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import cv2
from exif import Image

def bus_direc(name,direc):
    d=list()
    for n in os.listdir(direc):
        try:
            for m in os.listdir(direc+r'/'+n):
                try:
                    for l in os.listdir(direc+r'/'+n+r'/'+m):
                        try:
                            for on in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l):
                                try:
                                    for off in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on):
                                        if name in off:
                                            d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off)
                                except:
                                    if name in on:
                                        d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on)
                        except:
                            if name in l:
                                d.append(direc+r'/'+n+r'/'+m+r'/'+l)
                except:
                    if name in m:
                        d.append(direc+r'/'+n+r'/'+m)
        except:
            if name in n:
                d.append(direc+r'/'+n)
    
    return (d)

def leer_sub(direc):
    n=list()
    Med=list()
    TimeOn=list()
    TimeOff=list()
    fecha=list()
    lati=list()
    long=list()

    with open (direc , 'r') as lec:
        #print(lec.readable())
        for linea in lec:
            n.append(linea)
        count = 0
        for i in range(len(n)):
            if count == 0:
                count=count+1
                Med.append(n[i][:1])
            elif count == 1:
                count=count+1
                TimeOn.append(datetime.strptime(n[i][:12],r'%H:%M:%S,%f').time())
                TimeOff.append(datetime.strptime(n[i][17:29],r'%H:%M:%S,%f').time())
            elif count == 2:
                count=count+1
            elif count == 3:
                count=count+1
                fecha.append(datetime.strptime(n[i][:23],r'%Y-%m-%d %H:%M:%S.%f').date())
            elif count == 4:
                count=count+1    
                lati.append(n[i].split()[18][1:-1])
                long.append(n[i].split()[20][1:-1])
            else: count = 0

    df= pd.DataFrame()
    df['Med']=Med
    df['TimeOn']=TimeOn
    df['TimeOff']=TimeOff
    df['fecha']=fecha
    df['lati']=lati
    df['long']=long
    return df


def poner_pos(img_filename,lat,lon,dirdest22):
    '''
    folder_path = f"C:/Users/lixan/Desktop/transelect/Py/Pics/"
    #img_filename = 'DJI_20230309161136_0001_V Latitud-20-8128900 Longitud-70-1776620 Min_00-02.jpg'
    img_filename = 'DJI_20230309092014_0002_V lat-20.8065000 lon-70_191030.jpg'
    #img_path = f'{folder_path}/{img_filename}'

    for img_filename in os.listdir(folder_path):
        '''
    try:
        with open(img_filename, 'rb') as img_file:
            img = Image(img_file)
        
        lat=float(lat)
        lon=float(lon)
        print (lat,lon)
        img.gps_latitude = (int(lat)
                            ,int((lat-int(lat))*60)
                            , (((lat-int(lat))*60)-int(((lat-int(lat))*60)))*60)
        img.gps_longitude = (int(lon)
                            ,int((lon-int(lon))*60)
                            , (((lon-int(lon))*60)-int(((lon-int(lon))*60)))*60)
        img.gps_latitude_ref = 'S'
        img.gps_longitude_ref = 'W'
        with open(f'{dirdest22}/{img_filename.split("/")[-1:][0]}', 'wb') as new_image_file:
                new_image_file.write(img.get_file())
    except: pass

#%%

root = tk.Tk()
root.withdraw()
coord_path = filedialog.askdirectory(title='Seleccione directorio con videos')
dirdest = filedialog.askdirectory(title='Seleccione destino frames')
dirdest2 = filedialog.askdirectory(title='Seleccione destino frames con posicion')
exc = filedialog.askopenfilename(title='Seleccione excel con nombres y minutos')

'''
vid='DJI_20230223160059_0001_V'#test
imag='Captura de pantalla 2023-04-03 120249.png'#test
hora=0#test
minuto=2#test
segundo=10#test
milisegundo=4#test
'''
#%%
detec=pd.read_excel(exc)
#Empezar a buscar

for vid,ft in zip(detec['Vid'],detec['ft']):
    
    #Buscar Video e Path
    directorios=bus_direc(vid,coord_path)
    
    #Leer Subtitulos
    for ss in directorios:
        if 'SRT' in ss:
            SB=leer_sub(ss).reset_index()
            

    lati=SB.query('index==@ft').iloc[0]['lati']
    longi=SB.query('index==@ft').iloc[0]['long']
    nFrame=ft

    minu=SB.query('index==@ft').TimeOn.iloc[0].minute
    seco=SB.query('index==@ft').TimeOn.iloc[0].second
    #Buscar Frame y guardar:
        
    for V in directorios:
        if 'MP4' in V:
            if '{vid}_{minu}_{seco}_{nFrame}.jpg' not in os.listdir(f"{dirdest}"):
                video=cv2.VideoCapture(V)
                video.set(cv2.CAP_PROP_POS_FRAMES, nFrame-1)
                success,image = video.read()  
                frame=f"{dirdest}/{vid}_{minu}_{seco}_{nFrame}.jpg"
                cv2.imwrite(f"{dirdest}/{vid}_{minu}_{seco}_{nFrame}.jpg", image)
                poner_pos(frame, lati, longi, dirdest2)
            '''
            while success:
                count += 1
                if count==nFrame:
                    frame=f"{dirdest}/{vid}_{mm}_{s}_{count}.jpg"
                    cv2.imwrite(f"{dirdest}/{vid}_{mm}_{s}_{count}.jpg", image)
                    poner_pos(frame, lati, longi, dirdest2)
                    break
                if count==10000:
                    break
                success,image = video.read()
                print(f'Read {count}')
               ''' 
        

    
    



'''
direc = r'C:/Users/lixan/Desktop/transelect/Fotografias/Segunda Visita/M1/DJI_202302231458_001/DJI_20230223145954_0001_V.SRT'

n=list()
Med=list()
TimeOn=list()
TimeOff=list()
fecha=list()
lati=list()
long=list()

with open (direc , 'r') as lec:
    print(lec.readable())
    for linea in lec:
        n.append(linea)
    count = 0
    for i in range(len(n)):
        if count == 0:
            count=count+1
            Med.append(n[i][:1])
        elif count == 1:
            count=count+1
            TimeOn.append(datetime.strptime(n[i][:12],r'%H:%M:%S,%f').time())
            TimeOff.append(datetime.strptime(n[i][17:29],r'%H:%M:%S,%f').time())
        elif count == 2:
            count=count+1
        elif count == 3:
            count=count+1
            fecha.append(datetime.strptime(n[i][:23],r'%Y-%m-%d %H:%M:%S.%f').date())
        elif count == 4:
            count=count+1    
            lati.append(n[i].split()[18][1:-1])
            long.append(n[i].split()[20][1:-1])
        else: count = 0

df= pd.DataFrame()
df['Med']=Med
df['TimeOn']=TimeOn
df['TimeOff']=TimeOff
df['fecha']=fecha
df['lati']=lati
df['long']=long
'''
#%%
'''
import tkinter as tk
from tkinter import filedialog

import cv2

root = tk.Tk()
root.withdraw()
coord_path = filedialog.askdirectory(title='Seleccione directorio con videos')

vids=list()
for a in os.listdir(coord_path):
    if '.MP4' in a:
     vids.append(coord_path+'/'+a)
 '''    
