import re
import numpy as np
import pandas as pd
import datetime
import math


#=====================================
# MACRO FUNCIÓN de limpieza de datos
#=====================================

def limpiar_datos(data):
    import limpieza_datos as l
    data = l.cambio_nombre(data)
    data = l.eliminar_duplicados(data)
    data = l.eliminar_columnas(data)
    data = l.eliminar_columnas_extra(data)
    data = l.eliminar_espacios(data)
    data = l.tratar_ubicacion(data)
    data = l.tratar_cristal(data)
    data = l.tratar_precio(data)
    data = l.tratar_fabricacion(data)
    data = l.tratar_calibre(data)
    data = l.tipo_automatico(data)
    data = l.tratar_reserva(data)
    data = l.tratar_joyas(data)
    data = l.tratar_agua(data)
    data = l.tratar_diametro(data)
    data = l.funciones(data)
    data = l.otros(data)
    data = l.eliminacion_cierre(data)
    
    
    return data




#=====================
# FUNCIONES GENERALES
#=====================

# Función para cambiar el nombre a algunas columnas
def cambio_nombre(data):
    data = data.rename(columns={'(Reloj) Modelo':'Modelo'})
    
    return data


# Función para eliminar duplicados
def eliminar_duplicados(data):
    data = data.drop_duplicates(subset=['Código del anuncio'])

    return data

# Función para eliminar columnas que no aportan
def eliminar_columnas(data):
    data = data.drop(["Oscilación"], axis = 1)
    data = data.drop(["Longitud de la pulsera"], axis = 1)
    data = data.drop(["Grosor de la pulsera"], axis = 1)
    data = data.drop(["Ancho de la pulsera"], axis = 1)
    data = data.drop(["Ancho de cierre"], axis = 1)
    data = data.drop(["Código del anuncio"], axis = 1)

    return data

# Función para eliminar columnas extra que dudábamos si eliminar
def eliminar_columnas_extra(data):
    data = data.drop(["Grosor"], axis = 1)
    data = data.drop(["Código del comerciante"], axis = 1)
    data = data.drop(["Número de referencia"], axis = 1)
    

    return data


# Función para eliminar los espacios de las características de cada modelo
def eliminar_espacios(data):
    data["Cierre"] = data['Cierre'].str.strip()
    data["Cristal"] = data["Cristal"].str.strip()
    data["Año de fabricación"]= data["Año de fabricación"].str.strip()
    data["Material de la pulsera"]= data["Material de la pulsera"].str.strip()
    data["Estado"]= data["Estado"].str.strip()
    data["Género"] = data["Género"].str.strip()
    data["Contenido de la entrega"] = data["Contenido de la entrega"].str.strip()
    
    return data


#=================================
# FUNCIONES PARA TRATAR COLUMNAS
#=================================


def tratar_ubicacion(data):
    data[['Pais', 'Ciudad']] = data.Ubicación.str.split(',', n=1, expand=True)
    data = data.drop(["Ciudad"], axis = 1)
    data = data.drop(["Ubicación"], axis = 1)
    
    return data


def tratar_cristal(data):
    data.Cristal = data.Cristal.replace({"Esfera": "Cristal", "Pulsera": "Cristal"})
    
    return data


def tratar_precio(data):
    
    data["Precio"] = data["Precio"].apply(lambda x: x.replace("Precio a petición", "-999"))
    data["Precio"] = data["Precio"].apply(lambda x: x.replace("[Sujeto a negociación]", ""))
    data["Precio"] = data["Precio"].apply(lambda x: x.replace(" ", ""))
    data["Precio"] = data["Precio"].apply(lambda x: x.replace("€", ""))
    data["Precio"] = data["Precio"].apply(lambda x: x.replace("\xa0", ""))
    data["Precio"] = data["Precio"].apply(lambda x: x.replace("=", ""))
    
    for i in data['Precio']:
        try:
            resultado = re.search(r'\((.*)\)', i)
            precio = resultado.group(1)
            data['Precio'] = data['Precio'].replace(i, precio)
        except:
            continue
    data['Precio'] = data['Precio'].astype(float)
        
    return data


def tratar_fabricacion(data):
    
    año=list(data['Año de fabricación'])
    año = list(map(lambda s: s.strip(), año))
    for ind,x in enumerate(año):
        if x=='No conocido':
            año[ind]=float(np.nan)
        else:
            año[ind] = float(x.split("(")[0])
    fecha_actual = datetime.date.today()
    year_actual = fecha_actual.year
    for i, elem in enumerate(año):
        if not pd.isnull(elem):
            año[i] = (year_actual - elem)+1
    data['Edad']=año
    del data['Año de fabricación']
    
    return data


def tratar_calibre(data):
    data['Calibre'] = data['Calibre'].astype(str)
    calibre = data['Calibre'].str.split(',', expand = True)
    calibre2 = calibre.rename(columns={0:'Calibre 1',
                                   1:'Calibre 2',2:'Calibre 3'})
    try:
        calibre2.drop([3], axis = 1)
    except:
        print()
    data= pd.concat([data, calibre2], axis = 1)
    data = data.drop(["Calibre",3], axis = 1)

    data["Calibre 1"] = data["Calibre 1"].apply(lambda x: x.replace("[[",""))
    data["Calibre 1"] = data["Calibre 1"].apply(lambda x: x.replace("]]",""))
    data["Calibre 1"] = data["Calibre 1"].apply(lambda x: x.replace("'",""))
    data["Calibre 2"].fillna("None" , inplace = True)
    data["Calibre 2"] = data["Calibre 2"].apply(lambda x: x.replace("'",""))
    data["Calibre 2"] = data["Calibre 2"].apply(lambda x: x.replace("]]",""))
    data["Calibre 3"].fillna("None" , inplace = True)
    data["Calibre 3"] = data["Calibre 3"].apply(lambda x: x.replace("]]",""))
    data["Calibre 3"] = data["Calibre 3"].apply(lambda x: x.replace("'",""))

    data["Calibre 1"].replace("","None", inplace = True)
    data.drop(["Calibre 2"], axis = 1, inplace = True)

    data = data.rename(columns={'Calibre 1':'Tipo de Calibre',
                                   'Calibre 3':'Código de Calibre'})
    
    data = data.drop(["Código de Calibre"], axis = 1)

    return data


def tipo_automatico(data):
    data.loc[(data["Tipo de Calibre"]!='Automático') & (data["Tipo de Calibre"]!='Cuarzo') 
         & (data["Tipo de Calibre"]!='Cuerda manual'),'Tipo de Calibre']="Automático"
    
    return data
    

def tratar_reserva(data):
    data["Reserva de marcha"]= data["Reserva de marcha"].astype(str)
    data["Reserva de marcha"] = data["Reserva de marcha"].apply(lambda x: x.replace("h", ""))
    data["Reserva de marcha"] = data["Reserva de marcha"].apply(lambda x: x.replace(" ", ""))
    data["Reserva de marcha"]= data["Reserva de marcha"].astype(float)
    
    return data


def tratar_joyas(data):
    data["Número de joyas"]= data["Número de joyas"].astype(float)
    return data


def tratar_agua(data):
    data["Resistente al agua"]= data["Resistente al agua"].astype(str)
    data["Resistente al agua"]= data["Resistente al agua"].apply(lambda x: x.replace("ATM", ""))
    data["Resistente al agua"]= data["Resistente al agua"].apply(lambda x: x.replace("No resistente al agua", "0"))
    data["Resistente al agua"]= data["Resistente al agua"].apply(lambda x: x.replace("Más de 120", "140"))
    data["Resistente al agua"]= data["Resistente al agua"].apply(lambda x: x.replace(",", "."))
    data["Resistente al agua"]= data["Resistente al agua"].astype(float)
    
    return data


def tratar_diametro(data):
    import math
    data["Diámetro"]= data["Diámetro"].astype(str)
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace(" ", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("mmProbar", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("mm", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace(",", "."))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("y", "."))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("incl.thelugs", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("30bezel(", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("all)", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("ca.", ""))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("×", "x"))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("31.636.2", "nan"))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("40.834.7", "nan"))
    data["Diámetro"]= data["Diámetro"].apply(lambda x: x.replace("42.544.6", "nan"))
    diametro = list(data["Diámetro"])
    diametro_nuevo = list()
    for ind,i in enumerate(diametro):
        if len(i) <= 5 and 'x' not in i and i != 'nan':
            i = (float(i))*math.pi
            diametro_nuevo.append(i)
        elif len(i) > 4 and 'x' in i:
            sep = i.split('x')
            i = float(sep[0])*2 + float(sep[1])*2
            diametro_nuevo.append(i)
        else:
            i == 'nan'
            try:
                diametro_nuevo.append(float(i))
            except:
                diametro_nuevo.append(np.nan)
    data['Diámetro'] = diametro_nuevo
    data['Diámetro'] = data['Diámetro'].astype(float)

    data = data.rename(columns={'Diámetro':'Perímetro'})
    
    return data

#Función para separar la columna Funciones en varias columnas (con 1 si lo tiene y 0 si no lo tiene)

def funciones(data):
    data = data.rename(columns={'                     Funciones':'Funciones'})
    funciones=[]
    for x in data['Funciones']:
        try:
            x=x.split(',')
            x = list(map(lambda l: l.strip(), x))
            funciones.append(x)
        except: 
            funciones.append([])
            continue
    data['Funciones']=funciones
    carac=[]
    for x in data['Funciones']:
        try:  
            for i in x:
                if i not in carac:
                    carac.append(i)
        except: continue
    for x in carac:
        fun=[]
        for i in data['Funciones']:
            if x in i:
                fun.append(1)
            else:
                fun.append(0)  
        data[x]=fun 
    del data['Funciones']
    
    return data


# Función para separar la columna Otros (con 0 y 1)

def otros(data):
    data = data.rename(columns={'                     Otros':'Otros'})
    otros=[]
    for x in data['Otros']:
        try:
            x=x.split(',')
            x = list(map(lambda l: l.strip(), x))
            otros.append(x)
        except: 
            otros.append([])
            continue
    data['Otros']=otros
    carac=[]
    for x in data['Otros']:
        try:  
            for i in x:
                if i not in carac:
                    carac.append(i)
        except: continue
    for x in carac:
        fun=[]
        for i in data['Otros']:
            if x in i:
                fun.append(1)
            else:
                fun.append(0)  
        data[x]=fun 
    del data['Otros']
    
    return data


def eliminacion_cierre(data):
    data = data.drop(["Cierre"], axis = 1)
    
    return data


                     