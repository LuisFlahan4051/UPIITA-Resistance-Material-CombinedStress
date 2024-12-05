import re
import numpy as np

n= np.float_power(10, -9)
u= np.float_power(10, -6)
m= np.float_power(10, -3)
k= np.float_power(10, 3)
M= np.float_power(10, 6)
G= np.float_power(10, 9)
T= np.float_power(10, 12)

cord_x=0
cord_y=1
cord_z=2

def engine():

    profile = 'circle'
    if profile == 'circle':
        radius = 40*m
        height = 1
        area = np.pi * (radius**2)
        volume = np.pi * (radius**2) * height
        polarMomentZ = (np.pi * (radius**4)) / 2
        momentX = (np.pi * (radius**4)) / 4
        momentY = momentX

    if profile == 'rectangle':
        width = 1
        height = 1
        area = width * height
        momentX = (width * (height**3)) / 12
        momentY = (height * (width**3)) / 12
        momentZ = momentX + momentY

    vectorPosicion1 = np.array([-750*m, 600*m,500*m])
    vectorFuerza1 = np.array([-120*k, 250*k, 400*k])
    matrizMomento = np.cross(vectorPosicion1, vectorFuerza1)
    print(f"El momento es: {matrizMomento}")

    esfuerzoNormal = vectorFuerza1[cord_z]/area
    esfuerzoCortanteX = vectorFuerza1[cord_x]/area
    esfuerzoCortanteY = vectorFuerza1[cord_y]/area

    maximoEsfuerzoNormalFlexionanteX = (matrizMomento[cord_x] * radius) / momentX
    maximoEsfuerzoNormalFlexionanteY = (matrizMomento[cord_y] * radius) / momentY
    maximoEsfuerzoCortanteTorsion = (matrizMomento[cord_z] * radius) / polarMomentZ

    print(f"El esfuerzo normal es: {format_eng(esfuerzoNormal)} Pa")
    print(f"El esfuerzo cortante en X es: {format_eng(esfuerzoCortanteX)} Pa")
    print(f"El esfuerzo cortante en Y es: {format_eng(esfuerzoCortanteY)} Pa")
    print(f"El máximo esfuerzo normal flexionante en X es: {format_eng(maximoEsfuerzoNormalFlexionanteX)} Pa")
    print(f"El máximo esfuerzo normal flexionante en Y es: {format_eng(maximoEsfuerzoNormalFlexionanteY)} Pa")
    print(f"El máximo esfuerzo cortante por torsión es: {format_eng(maximoEsfuerzoCortanteTorsion)} Pa")
    return esfuerzoNormal, esfuerzoCortanteX, esfuerzoCortanteY, maximoEsfuerzoNormalFlexionanteX, maximoEsfuerzoNormalFlexionanteY, maximoEsfuerzoCortanteTorsion
    

def format_eng(value):
    """
    Formatea un valor numérico en notación de ingeniería.
    
    Args:
        value (float): El valor numérico a formatear.
    
    Returns:
        str: El valor formateado como una cadena.
    """
    prefixes = {
        -6: 'u', 
        -3: 'm',
        0: '',
        3: 'k',
        6: 'M',
        9: 'G',
        12: 'T'
    }
    
    if value == 0:
        return '0'
    
    exponent = int(np.floor(np.log10(abs(value)) / 3) * 3)
    mantissa = value / (10 ** exponent)
    
    if exponent in prefixes:
        return f"{mantissa:.6g}{prefixes[exponent]}"
    else:
        return f"{mantissa:.6g}e{exponent}"

def parse_eng(value_str):
    """
    Convierte una cadena en notación de ingeniería a un valor numérico.
    
    Args:
        value_str (str): La cadena en notación de ingeniería.
    
    Returns:
        float: El valor numérico correspondiente.
    """
    prefixes = {
        'u': -6,
        'm': -3,
        '': 0,
        'k': 3,
        'M': 6,
        'G': 9,
        'T': 12
    }
    
    # Expresión regular para separar la mantisa y el prefijo
    match = re.match(r"([-+]?\d*\.?\d+)([a-zA-Z]*)", value_str)
    
    if not match:
        raise ValueError(f"Cadena no válida: {value_str}")
    
    mantissa_str, prefix = match.groups()
    mantissa = float(mantissa_str)
    
    if prefix not in prefixes:
        raise ValueError(f"Prefijo no válido: {prefix}")
    
    exponent = prefixes[prefix]
    return mantissa * (10 ** exponent)
