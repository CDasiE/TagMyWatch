import pandas as pd
import numpy as np
import re

#===========================================
# MACRO FUNCIÓN de limpieza del webscrapping
#===========================================

def limpieza_webscrap(lista):
    
    import tratamiento_webscrapping as w
    lista = w.eliminar_caracteres(lista)
    lista = w.creacion_dataframe(lista)
    
    return lista


#=====================
# FUNCIONES GENERALES
#=====================
# Primera función de limpieza para cada caracteristica del reloj (lee una lista de listas de relojes con sus caracteristicas)

def eliminar_caracteres(lista):
    lista_relojes = list()
    for reloj in lista:
        try:
            df = pd.DataFrame(reloj)
            df[0] = df[0].replace({'\n':''},regex=True)
            df[0] = df[0].replace({'\r':''},regex=True)
            nuevo_reloj = list(df[0])
        except: 
            continue
        if '                  Descripción' in nuevo_reloj:
            a = nuevo_reloj.index('                  Descripción')
            nuevo_reloj = nuevo_reloj[:a]
        lista_relojes.append(nuevo_reloj)
        
    return lista_relojes


# Creación de un dataframe a partir de una lista de listas con características de relojes (lee una lista de listas de relojes con sus caracteristicas)

def creacion_dataframe(lista):
    caracteristicas = ['Código del anuncio','Marca', '(Reloj) Modelo','Número de referencia','Código del comerciante',
                       'Material de la pulsera','Año de fabricación','Estado','Contenido de la entrega','Género','Ubicación',
                       'Precio','Disponibilidad','Reserva de marcha','Número de joyas','Oscilación','Diámetro','Grosor',
                       'Resistente al agua','Material del bisel','Cristal','Esfera','Esfera con números','Color de la pulsera',
                       'Longitud de la pulsera','Grosor de la pulsera','Ancho de la pulsera','Cierre','Material del cierre',
                       'Ancho de cierre','                     Funciones','                     Otros','Calibre','Material de la caja']

    lista_relojes = []
    for reloj in lista:
        values= []
        dicc= dict.fromkeys(caracteristicas,np.nan)
        calibre=[[]]
        for i,x in enumerate(reloj):
            if (x!='Calibre') and x in caracteristicas:
                dicc[x]=reloj[i+1]
            elif x=='Calibre':
                calibre[0].append(reloj[i+1])
        dicc['Calibre']=calibre 
        lista_relojes.append(dicc)
    df_relojes = pd.DataFrame(lista_relojes)
    return df_relojes