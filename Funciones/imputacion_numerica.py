import re
import numpy as np
import pandas as pd


def imputacion_numerica(data):
    
    data['Número de joyas'] = data['Número de joyas'].fillna(data['Número de joyas'].median())
    data['Reserva de marcha'] = data['Reserva de marcha'].fillna(data['Reserva de marcha'].median())
    data['Resistente al agua'] = data['Resistente al agua'].fillna(data['Resistente al agua'].median())
    data['Edad'] = data['Edad'].fillna(data['Edad'].median())
    
    return data


