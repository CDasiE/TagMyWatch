import re
import numpy as np
import pandas as pd
import datetime

#=============================================
# MACRO FUNCIÓN de imputación de valores nulos
#=============================================

def imputacion(data):
    import imputaciones as i
    data = i.imputacion_cuarzo(data)
    data = i.imputacion_estado(data)
    data = i.imputacion_esfera(data)
    data = i.imputacion_material_caja(data)
    data = i.imputacion_color_pulsera(data)
    data = i.imputacion_bisel(data)
    data = i.imputacion_material_cierre(data)
    data = i.imputacion_material_pulsera(data)
    data = i.imputacion_esfera_numeros(data)
    data = i.imputacion_cristal(data)
    data = i.imputacion_calibre(data)
    data = i.imputacion_perimetro(data)
    data = i.imputacion_genero(data)
    data = i.imputar_modelo(data)
    data = i.eliminar_precio(data)
    
    return data


#=====================
# FUNCIONES GENERALES
#=====================
def imputacion_cuarzo(data):
    data.loc[data["Tipo de Calibre"]=='Cuarzo','Número de joyas']=0
    data.loc[data["Tipo de Calibre"]=='Cuarzo','Reserva de marcha']=0
    
    return data

def imputacion_estado(data):
    data['Estado'] = data['Estado'].fillna(data['Estado'].mode()[0])
    
    return data

def imputacion_esfera(data):
    data['Esfera'] = data['Esfera'].fillna(data['Esfera'].mode()[0])
    
    return data


def imputacion_material_caja(data):
    data['Material de la caja'] = data['Material de la caja'].fillna(data['Material de la caja'].mode()[0])
    
    return data


def imputacion_color_pulsera(data):
    data['Color de la pulsera'] = data['Color de la pulsera'].fillna(data['Esfera'])
    
    return data


def imputacion_bisel(data):
    data['Material del bisel'] = data['Material del bisel'].fillna(data['Material de la caja'])
    
    return data

def imputacion_material_cierre(data):
    data['Material del cierre'] = data['Material del cierre'].fillna(data['Material de la caja'])
    
    return data

def imputacion_material_pulsera(data):
    data['Material de la pulsera'] = data['Material de la pulsera'].fillna(data['Material de la caja'])
    
    return data

def imputacion_esfera_numeros(data):
    data['Esfera con números'] = data['Esfera con números'].fillna("Otros")
    
    return data

def imputacion_cristal(data):
    data['Cristal'] = data['Cristal'].fillna("Otro material")
    
    return data

def imputacion_calibre(data):
    data.loc[data["Tipo de Calibre"]=='None', "Tipo de Calibre"]= data['Tipo de Calibre'].mode()[0]
    
    return data

def imputacion_perimetro(data):
    data.loc[data['Perímetro'] > 350, 'Perímetro'] = data['Perímetro'].mean()
    data['Perímetro'] = data['Perímetro'].fillna(data['Perímetro'].mean())
    
    return data

def imputacion_genero(data):
    data['Género'] = data['Género'].fillna(data['Género'].mode()[0])
    
    return data

def imputar_modelo(data):
    data['Precio'].replace(-999.0,0,inplace=True)
    medianas=data[data['Precio']!=0].groupby(['Marca','Modelo']).median()
    modelos=medianas.index
    precio=list(medianas['Precio'])
    medianas_marcas= dict(zip(modelos, precio))
    data['Modelo'].replace(np.nan,'cambiar',inplace=True)
    var=1000000
    modelo=0
    for ind,x in enumerate(data['Modelo']):
        if x=='cambiar':
            for mar,mod in medianas_marcas:
                if data.iloc[ind,0]==mar:
                    resta=abs(data.iloc[ind,6]-medianas_marcas.get((mar,mod)))
                    if var>resta:
                        var=resta
                        modelo=mod
            data.iloc[ind,1]=modelo
    return data

def eliminar_precio(data):
    data = data.query('Precio != 0')
    
    return data

