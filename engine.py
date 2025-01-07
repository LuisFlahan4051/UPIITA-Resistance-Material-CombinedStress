import re
import numpy as np

" ------------------------ GENERALS ------------------------"

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

def getENG(magnitud):
    exponent = int(np.floor(np.log10(abs(magnitud)) / 3) * 3)
    mantissa = magnitud / (10 ** exponent)
    return mantissa, exponent

class Profile:
    def __init__(self, profile_type, dimension1, dimension2=None):
        self.profile_type = profile_type
        if profile_type == 'circle':
            self.radius = dimension1
            self.height = dimension2 if dimension2 else 1
            self.area = np.pi * (self.radius**2)
            self.volume = np.pi * (self.radius**2) * self.height
            self.polarMomentZ = (np.pi * (self.radius**4)) / 2
            self.momentX = (np.pi * (self.radius**4)) / 4
            self.momentY = self.momentX
        elif profile_type == 'rectangle':
            self.width = dimension1
            self.height = dimension2 if dimension2 else 1
            self.area = self.width * self.height
            self.momentX = (self.width * (self.height**3)) / 12
            self.momentY = (self.height * (self.width**3)) / 12
            self.momentZ = self.momentX + self.momentY

# Definir los materiales y sus propiedades
materials = {
    "Acero Estructural (ASTM-A36)": {"E": 200, "G": 77.2},
    "Acero Alta resistencia-baja aleación ASTM-A709 Grado 345": {"E": 200, "G": 77.2},
    "Acero Alta resistencia-baja aleación ASTM-A913 Grado 450": {"E": 200, "G": 77.2},
    "Acero Alta resistencia-baja aleación ASTM-A992 Grado 345": {"E": 200, "G": 77.2},
    "Acero Templado ASTM-A709 Grado 690": {"E": 200, "G": 77.2},
    "Acero Inoxidable, AISI 302 Laminado en frio": {"E": 190, "G": 75},
    "Acero Inoxidable, AISI 302 Recocido": {"E": 190, "G": 75},
    "Acero de refuerzo Resistencia media": {"E": 200, "G": 77},
    "Acero de refuerzo Alta resistencia": {"E": 200, "G": 77},
    "Hierro fundido Hierro fundido gris 4.5% C. ASTM A-48": {"E": 69, "G": 28},
    "Hierro fundido Hierro fundido maleable 2% C, 1% Si. ASTM A-47": {"E": 165, "G": 65},
    "Aluminio Aleación 1100-H14 (99% Al)": {"E": 70, "G": 26},
    "Aluminio Aleación 2014-T6": {"E": 75, "G": 27},
    "Aluminio Alcación 2024-T4": {"E": 73, "G": None},
    "Aluminio Aleación 5456-H116": {"E": 72, "G": None},
    "Aluminio Aleación 6061-T6": {"E": 70, "G": 26},
    "Aluminio Aleación 7075-T6": {"E": 72, "G": 28},
    "Cobre Cobre libre de oxigeno (99.9% Cu) Recocido": {"E": 120, "G": 44},
    "Cobre Cobre libre de oxigeno (99.9% Cu) Endurecido": {"E": 120, "G": 44},
    "Cobre Latón amarillo (65% Cu. 35% Zn) Laminado en frio": {"E": 105, "G": 39},
    "Cobre Latón amarillo (65% Cu. 35% Zn) Recocido": {"E": 105, "G": 39},
    "Cobre Latón rojo (85% Cu. 15% Zn) Laminado en frio": {"E": 120, "G": 44},
    "Cobre Latón rojo (85% Cu. 15% Zn) Recocido": {"E": 120, "G": 44},
    "Cobre Estaño bronce (88 Cu, 8Sn, 4Zn)": {"E": 95, "G": None},
    "Cobre Manganeso bronce (63 Cu, 25 Zn, 6 Al, 3 Mn. 3 Fe)": {"E": 105, "G": None},
    "Cobre Aluminio bronce (81 Cu, 4 Ni, 4 Fe, 11 Al)": {"E": 110, "G": 42}
}

"------------------------ FUNCTIONS ------------------------"

def esfuerzoCortantePorFlexionEnAngulo(maximoEsfuerzoCortante, gradoObservacion, radio, type='circle'):
    """
    Entrega el esfuerzo cortante que varia parabólicamente en función de un grado de perspectiva respecto al eje neutro y el eje direccón.

    Args:
        grado (float): entre 0 y 90 grados.
        radio (float): radio de la sección transversal.

    Returns:
        float: el esfuerzo cortante en función del grado de observación.
    """
    if type == 'circle':
        gradoObservacion = np.abs(gradoObservacion)
        if gradoObservacion > 360:
            gradoObservacion = gradoObservacion % 360
        
        r= radio * np.sin(np.radians(gradoObservacion))
        return maximoEsfuerzoCortante * (1 - (r/radio)**2)
    else:
        return 0

def esfuerzoNormalPromedio(vectorFuerza, area, ejeNormal):
    """
    Entrega el esfuerzo normal promedio en función de un vector de fuerza y un área.

    Args:
        vectorFuerza (np.array): vector de fuerza.
        area (float): área de la sección transversal (Normal).
        ejeNormal (int): eje normal al que se desea calcular el esfuerzo normal 0,1,2 para x,y,z respectivamente.

    Returns:
        float: el esfuerzo normal promedio en función de un eje normal.
    """ 
    return vectorFuerza[ejeNormal]/area


def esfuerzoCortante(vectorFuerza, area, ejeCortante, type='circle', base=0, height=0):
    """
    Entrega el esfuerzo cortante en función de un vector de fuerza y un área.

    Args:
        vectorFuerza (np.array): vector de fuerza.
        area (float): área de la sección transversal (Normal).
        ejeCortante (int): eje cortante al que se desea calcular el esfuerzo cortante 0,1,2 para x,y,z respectivamente.

    Returns:
        float: el esfuerzo cortante en función de un eje cortante.
    """ 
    if type == 'circle':
        promedio= vectorFuerza[ejeCortante]/area
        maxCortante= (4/3) * promedio
        return promedio, maxCortante
    if type == 'rectangle':
        promedio= vectorFuerza[ejeCortante]/area
        maxCortante= (3/2)*promedio
        return promedio, maxCortante

def esfuerzoNormalPorFlexion(matrizMomento, profile, ejeNormal=cord_z):
    """
    Entrega el esfuerzo normal en función de un momento flector y un perfil.

    Args:
        matrizMomento (np.array): matriz de momento.
        profile (Profile): instancia de la clase Profile.
        ejeNormal (int): eje normal al que se desea calcular el esfuerzo normal 0,1,2 para x,y,z respectivamente.
    """
    if profile.profile_type == 'circle':
        if ejeNormal == cord_z:
            return (matrizMomento[cord_x] * profile.radius) / profile.momentX, (matrizMomento[cord_y] * profile.radius) / profile.momentY
        if ejeNormal == cord_x:
            return (matrizMomento[cord_y] * profile.radius) / profile.momentY, (matrizMomento[cord_z] * profile.radius) / profile.polarMomentZ
        if ejeNormal == cord_y:
            return (matrizMomento[cord_x] * profile.radius) / profile.momentX, (matrizMomento[cord_z] * profile.radius) / profile.polarMomentZ
    if profile.profile_type == 'rectangle':
        if ejeNormal == cord_z:
            return (matrizMomento[cord_x] * profile.height) / profile.momentX, (matrizMomento[cord_y] * profile.width) / profile.momentY
        if ejeNormal == cord_x:
            return (matrizMomento[cord_y] * profile.width) / profile.momentY, (matrizMomento[cord_z] * profile.height) / profile.momentZ
        if ejeNormal == cord_y:
            return (matrizMomento[cord_x] * profile.height) / profile.momentX, (matrizMomento[cord_z] * profile.width) / profile.momentZ

def esfuerzoCortantePorTorsion(matrizMomento, profile, ejeNormal=cord_z):
    """
    Entrega el esfuerzo cortante en función de un momento torsor y un perfil.

    Args:
        matrizMomento (np.array): matriz de momento.
        profile (Profile): instancia de la clase Profile.
        ejeCortante (int): eje cortante al que se desea calcular el esfuerzo cortante 0,1,2 para x,y,z respectivamente.
    """
    if profile.profile_type == 'circle':
        if ejeNormal == cord_z:
            promedio = (matrizMomento[cord_z] * profile.radius) / profile.polarMomentZ
        if ejeNormal == cord_x:
            promedio = (matrizMomento[cord_x] * profile.radius) / profile.polarMomentZ
        if ejeNormal == cord_y:
            promedio = (matrizMomento[cord_y] * profile.radius) / profile.polarMomentZ

        maxCortante = (2/3) * promedio
        return promedio, maxCortante
    
" ------------------------ MAIN ------------------------"
def engine():
    profile = Profile('circle', 40*m)
    vectorPosicion1 = np.array([-750*m, 600*m, 500*m])
    vectorFuerza1 = np.array([-120*k, 250*k, 400*k])
    matrizMomento = np.cross(vectorPosicion1, vectorFuerza1)
    print(f"El momento es: {matrizMomento}")

    eNormalPromedio = esfuerzoNormalPromedio(vectorFuerza1, profile.area, cord_z)
    maximoEsfuerzoCortanteX, esfuerzoCortantePromedioX = esfuerzoCortante(vectorFuerza1, profile.area, cord_x)
    maximoEsfuerzoCortanteY, esfuerzoCortantePromedioY = esfuerzoCortante(vectorFuerza1, profile.area, cord_y)

    maximoEsfuerzoNormalFlexionanteX, maximoEsfuerzoNormalFlexionanteY = esfuerzoNormalPorFlexion(matrizMomento, profile)
    maximoEsfuerzoCortanteTorsion, esfuerzoCortanteTorsionPromedio = esfuerzoCortantePorTorsion(matrizMomento, profile)
    
    print("--------------------------")
    print(f"El esfuerzo normal es: {format_eng(eNormalPromedio)} Pa")
    print(f"El esfuerzo cortante en X es: {format_eng(esfuerzoCortantePromedioX)} Pa")
    print(f"El máximo esfuerzo cortante en X es: {format_eng(maximoEsfuerzoCortanteX)} Pa")
    print(f"El esfuerzo cortante en Y es: {format_eng(esfuerzoCortantePromedioY)} Pa")
    print(f"El máximo esfuerzo cortante en Y es: {format_eng(maximoEsfuerzoCortanteY)} Pa")

    print(f"El máximo esfuerzo normal flexionante en X es: {format_eng(maximoEsfuerzoNormalFlexionanteX)} Pa")
    print(f"El máximo esfuerzo normal flexionante en Y es: {format_eng(maximoEsfuerzoNormalFlexionanteY)} Pa")
    print(f"El máximo esfuerzo cortante por torsión es: {format_eng(maximoEsfuerzoCortanteTorsion)} Pa")
    print(f"El esfuerzo cortante por torsión promedio es: {format_eng(esfuerzoCortanteTorsionPromedio)} Pa")
    
    esfuerzos = []
    ey=esfuerzoCortantePorFlexionEnAngulo(maximoEsfuerzoCortanteY, 30, profile.radius)
    print(ey)
    ex=esfuerzoCortantePorFlexionEnAngulo(maximoEsfuerzoCortanteX, 30+90, profile.radius)
    print(ex)

    et= np.sqrt(ex**2 + ey**2)
    print(et)
    eang= np.degrees(np.arctan(ey/ex))
    print(eang)




    # for i in range(0,360):
    #     esfuerzos.append(esfuerzoCortantePorFlexionEnAngulo(maximoEsfuerzoCortanteX, i, radius))
    # print(esfuerzos)
        
    return {
        'esfuerzoNormalPromedio': eNormalPromedio,
        'esfuerzoCortantePromedioX': esfuerzoCortantePromedioX,
        'maximoEsfuerzoCortanteX': maximoEsfuerzoCortanteX,
        'esfuerzoCortantePromedioY': esfuerzoCortantePromedioY,
        'maximoEsfuerzoCortanteY': maximoEsfuerzoCortanteY,
        'maximoEsfuerzoNormalFlexionanteX': maximoEsfuerzoNormalFlexionanteX,
        'maximoEsfuerzoNormalFlexionanteY': maximoEsfuerzoNormalFlexionanteY,
        'maximoEsfuerzoCortanteTorsion': maximoEsfuerzoCortanteTorsion,
        'esfuerzoCortanteTorsionPromedio': esfuerzoCortanteTorsionPromedio
    }


