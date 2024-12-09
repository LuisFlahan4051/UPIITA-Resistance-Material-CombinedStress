import numpy as np
from matplotlib import pyplot as plt 
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors


def tangentVectorsAtCircle(radius, axis, zDirection=-1):
    """
    Dibuja un campo de vectores tangentes a un círculo en un gráfico 3D.

    Args:
        radius (float): El radio del círculo.
        amplitude (float): La amplitud de los vectores.
        cycles (int): El número de ciclos de los vectores.
        phase (float): La fase de los vectores.
        axis (Axes3D): El objeto Axes3D donde se dibujarán los vectores.

    Returns:
        None
    """
    if zDirection > 0:
        direction = -1
    else:
        direction = 1

    theta = np.linspace(0, 2*np.pi, 100)  # Ángulo para media onda
    z = np.linspace(0, 1, 100)         # Altura (relleno vertical)

    # Crear la cuadrícula
    Theta, z = np.meshgrid(theta, z)  # Mallado para theta y la onda
    X = radius * np.cos(Theta)              # Coordenadas X
    Y = radius * np.sin(Theta)              # Coordenadas Y
    Z = np.cos(Theta) * z  # Limitar Z a estar entre 0 y la onda seno

    # Dibujar la superficie
    axis.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

    # Dibujar vectores desde z=0 hasta la superficie
    indices = np.arange(0, len(theta), 5)  # Seleccionar algunos índices
    X_vec = X[0, indices]
    Y_vec = Y[0, indices]
    Z_vec = np.zeros_like(X_vec)
    U = direction*np.sin( theta[indices])
    V = -direction*np.cos(theta[indices])
    W = np.zeros_like(Z_vec)

    axis.quiver(X_vec, Y_vec, Z_vec, U, V, W, length=1, cmap='viridis', alpha=0.5,normalize=True)

def graphTorsionalShearStress(resultados):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    radius = 1
    amplitude = resultados['maximoEsfuerzoCortanteTorsion']
    tangentVectorsAtCircle(radius, ax)
    circular_plane(radius, 0, ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([-amplitude, amplitude]) 
    
    plt.show()

def drawNormalVectorAtSurface(radius, esfuerzoNormalPromedio, axis, originPlane=0,height=1):
    """
    Dibuja vectores normales a la superficie de un cilindro en toda la matriz del círculo.

    Args:
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.
        esfuerzoNormalPromedio (float): El esfuerzo normal promedio.
        axis (Axes3D): El objeto Axes3D donde se dibujarán los vectores.

    Returns:
        None
    """
    # Crear una cuadrícula de coordenadas
    theta = np.linspace(0, 2 * np.pi, 20)
    r = np.linspace(0, radius, 5)
    theta, r = np.meshgrid(theta, r)
    
    # Convertir coordenadas polares a cartesianas
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.ones_like(x) * originPlane  # Altura constante

    # Componentes del vector normal
    u = np.zeros_like(x)
    v = np.zeros_like(y)
    w = np.ones_like(z) * height

    # Dibujar los vectores normales
    axis.quiver(x, y, z, u, v, w, cmap='viridis', arrow_length_ratio=1/(height*10), alpha=0.5)



def graphPerpendicularStress(resultados):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    esfuerzoNormalPromedio = resultados['esfuerzoNormalPromedio']
    
    
    radius = 1
    height = esfuerzoNormalPromedio
    circular_plane(radius, 0, ax)
    circular_plane(radius, height, ax,alpha=0.3)
    drawNormalVectorAtSurface(radius,esfuerzoNormalPromedio, ax,0, height)

    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([0, height])  

    plt.show()

def graphStress(resultados):
    fig = plt.figure()
    ax = fig.add_subplot(311)
    # ax11 = fig.add_subplot(322, projection='3d')
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    theta = np.linspace(0,360,100)
    eX = resultados['maximoEsfuerzoNormalFlexionanteX']*np.sin(np.radians(theta))
    eY = resultados['maximoEsfuerzoNormalFlexionanteY']*np.cos(np.radians(theta))
    eN = resultados['esfuerzoNormalPromedio']*np.ones_like(theta)

    ax.plot(theta, eX, label='Esfuerzo Normal por Mx', color='blue')
    ax.fill_between(theta, eX, color='blue', alpha=0.3)
    ax.set_title('Esfuerzo Normal por Mx')
    ax.legend()
    ax.set_xlabel('Theta (°)')
    ax.set_ylabel('Esfuerzo (Pa)')

    ax.quiver(theta[::5], np.zeros_like(theta[::5]), np.zeros_like(theta[::5]), eX[::5], angles='xy', scale_units='xy', scale=1, color='blue')
    

    # theta_rad = np.radians(theta)
    # theta_grid, eX_grid = np.meshgrid(theta_rad, eX)
    # X = eX_grid * np.cos(theta_grid)
    # Y = eX_grid * np.sin(theta_grid)
    # Z = np.ones_like(X)  # Mantener z constante

    # ax11.plot_surface(X, Y, Z, color='blue', alpha=0.6)
    # ax11.set_title('Esfuerzo Normal por Mx Enrollado')
    # ax11.set_xlabel('Eje X')
    # ax11.set_ylabel('Eje Y')
    # ax11.set_zlabel('Eje Z')

    
    # Z_vector = np.zeros_like(theta)
    # X_vector = maximoEsfuerzoNormalFlexionanteX * np.cos(np.radians(theta))
    # Y_vector = maximoEsfuerzoNormalFlexionanteX * np.sin(np.radians(theta))
    # U = np.zeros_like(Z_vector)
    # V = np.zeros_like(Z_vector)
    # W = eX

    # ax11.quiver(X_vector[::5], Y_vector[::5], Z_vector[::5], U[::5], V[::5], W[::5], color='red')


    
    ax2.plot(theta, eY, label='Esfuerzo Normal por My', color='green')
    ax2.fill_between(theta, eY, color='green', alpha=0.3)
    ax2.set_title('Esfuerzo Normal por My')
    ax2.legend()
    ax2.set_xlabel('Theta (°)')
    ax2.set_ylabel('Esfuerzo (Pa)')

    ax2.quiver(theta[::5], np.zeros_like(theta[::5]), np.zeros_like(theta[::5]), eY[::5], angles='xy', scale_units='xy', scale=1, color='green')


    ax3.plot(theta, eN, label='Esfuerzo Normal', color='red')
    ax3.fill_between(theta, eN, color='red', alpha=0.3)
    ax3.set_title('Esfuerzo Normal')
    ax3.legend()
    ax.set_xlabel('Theta (°)')
    ax.set_ylabel('Esfuerzo (Pa)')

    ax3.quiver(theta[::5], np.zeros_like(theta[::5]), np.zeros_like(theta[::5]), eN[::5], angles='xy', scale_units='xy', scale=1, color='red')


    #mplcursors.cursor(ax, hover=True)
    #mplcursors.cursor(ax2, hover=True)
    #mplcursors.cursor(ax3, hover=True)

    plt.tight_layout()
    plt.show()


def graphNormalStressOfMoment(resultados):
    fig = plt.figure()

    radius = 1
    
    axis = fig.add_subplot(121, projection='3d')
    amplitude = resultados['maximoEsfuerzoNormalFlexionanteX']
    waveAtCylinder(radius, amplitude, 1, 0, axis)
    circular_plane(radius, 0, axis)
    axis.set_xlabel('X')
    axis.set_ylabel('Y')
    axis.set_zlabel('Z')
    axis.set_xlim([-radius, radius])
    axis.set_ylim([-radius, radius])
    axis.set_zlim([-amplitude, amplitude])  # Límite en Z basado en la amplitud
    
    axis2 = fig.add_subplot(122, projection='3d')
    amplitude = resultados['maximoEsfuerzoNormalFlexionanteY']
    waveAtCylinder(radius, amplitude, 1, np.pi/2, axis2)
    circular_plane(radius, 0, axis2)
    axis2.set_xlabel('X')
    axis2.set_ylabel('Y')
    axis2.set_zlabel('Z')
    axis2.set_xlim([-radius, radius])
    axis2.set_ylim([-radius, radius])
    axis2.set_zlim([-amplitude, amplitude])
    plt.show()
    


def waveAtCylinder(radius, amplitude, cycles, phase, axis):
    """
    Dibuja una onda senoidal sobre la superficie de un cilindro.

    Args:
        radius (float): El radio del cilindro.
        amplitude (float): La amplitud de la onda senoidal.
        cycles (int): El número de ciclos de la onda senoidal.
        phase (float): La fase de la onda senoidal.
        axis (Axes3D): El objeto Axes3D donde se dibujará la onda senoidal.

    Returns:
        None
    """
    theta = np.linspace(0, 2*np.pi, 100)  # Ángulo para media onda
    z = np.linspace(0, 1, 100)         # Altura (relleno vertical)

    # Crear la cuadrícula
    Theta, z = np.meshgrid(theta, z)  # Mallado para theta y la onda
    X = radius * np.cos(Theta)              # Coordenadas X
    Y = radius * np.sin(Theta)              # Coordenadas Y
    Z = amplitude * np.sin(cycles * Theta + phase) * z  # Limitar Z a estar entre 0 y la onda seno

    # Dibujar la superficie
    axis.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

    # Dibujar vectores desde z=0 hasta la superficie
    indices = np.arange(0, len(theta), 4)  # Seleccionar algunos índices
    X_vec = X[0, indices]
    Y_vec = Y[0, indices]
    Z_vec = np.zeros_like(X_vec)
    U = np.zeros_like(X_vec)
    V = np.zeros_like(Y_vec)
    W = amplitude * np.sin(cycles * theta[indices] + phase)

    # arrow_length_ratio = 0; los cabezales de las flechas no se dibujan bien con amplitudes grandes
    arrow_length_ratio = 1/(amplitude*10)  # Relación de longitud de la flecha
    #arrow_length_ratio = 0

    axis.quiver(X_vec, Y_vec, Z_vec, U, V, W, cmap='viridis',alpha=0.7, length=1, arrow_length_ratio=arrow_length_ratio,linewidth=2)

def solid_cylinder(radius, height, axis):
    """
    Dibuja un cilindro sólido en un gráfico 3D.

    Args:
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.
        axis (Axes3D): El objeto Axes3D donde se dibujará el cilindro.

    Returns:
        None
    """
    cylinder(0, radius, height, axis)
    circular_plane(radius, 0, axis)
    circular_plane(radius, height, axis)

def cylinder(origin,radius, height, axis):
    """
    Dibuja un cilindro en un gráfico 3D.

    Args:
        origin (float): La coordenada Z de origen del cilindro.
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.
        axis (Axes3D): El objeto Axes3D donde se dibujará el cilindro.

    Returns:
        None
    """
    z = np.linspace(origin, height, 20)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    
    axis.plot_surface(x, y, z, cmap='viridis')

def circular_plane(radius, height, axis, alpha=0.5):
    """
    Dibuja un plano circular en un gráfico 3D.

    Args:
        radius (float): El radio del plano circular.
        height (float): La altura en el eje Z donde se dibujará el plano circular.
        axis (Axes3D): El objeto Axes3D donde se dibujará el plano circular.

    Returns:
        None
    """
    # Crear una cuadrícula de coordenadas
    theta = np.linspace(0, 2 * np.pi, 100)
    radius = np.linspace(0, radius, 50)
    theta, radius = np.meshgrid(theta, radius)
    
    # Convertir coordenadas polares a cartesianas
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = height
    z = np.ones_like(x) * z # Rellena la matriz z con el valor de z con el mismo tamaño de x
    
    # Dibujar el plano circular
    axis.plot_surface(x, y, z, cmap='viridis', alpha=alpha)

# -------------------- TEST ------------------------ #

def testGraphFunctions():
    """
    Ejecuta esta función para probar las funciones de gráficos.
    """
    fig = plt.figure()
    axis = fig.add_subplot(131, projection='3d')

    solid_cylinder(1, 1, axis)

    # Agregar títulos a los ejes
    axis.set_title('Cilindro')
    axis.set_xlabel('Eje X')
    axis.set_ylabel('Eje Y')
    axis.set_zlabel('Eje Z')
    
    axis2 = fig.add_subplot(132, projection='3d')
    draw_vector_field(axis2, vector_field_func, (-1, 1), (-1, 1), (-1, 1), density=5)
    
    axis3 = fig.add_subplot(133, projection='3d')
    axis3.set_title('Vector')
    axis3.set_xlim([0, 2])
    axis3.set_ylim([0, 2])
    axis3.set_zlim([0, 2])
    draw_vector(axis3, (0, 0, 0), (1, 1, 1))
    plt.show()


def draw_vector(ax, origin, vector):
    """
    Dibuja un vector en el espacio 3D.

    Args:
        ax (Axes3D): El objeto Axes3D donde se dibujará el vector.
        origin (tuple): Las coordenadas de origen del vector (x0, y0, z0).
        vector (tuple): La magnitud del vector (dx, dy, dz).
    """
    x0, y0, z0 = origin
    dx, dy, dz = vector
    
    ax.quiver(x0, y0, z0, dx, dy, dz, color='g', arrow_length_ratio=0.1)
    
    # Agregar títulos a los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

def draw_vector_field(ax, func, x_range, y_range, z_range, density=10):
    """
    Dibuja un campo vectorial en el espacio 3D.

    Args:
        ax (Axes3D): El objeto Axes3D donde se dibujará el campo vectorial.
        func (callable): La función que define el campo vectorial. Debe aceptar tres argumentos (x, y, z) y devolver una tupla (dx, dy, dz).
        x_range (tuple): El rango de valores para el eje X (xmin, xmax).
        y_range (tuple): El rango de valores para el eje Y (ymin, ymax).
        z_range (tuple): El rango de valores para el eje Z (zmin, zmax).
        density (int): La densidad de los vectores en el campo.
    """
    x = np.linspace(x_range[0], x_range[1], density)
    y = np.linspace(y_range[0], y_range[1], density)
    z = np.linspace(z_range[0], z_range[1], density)
    x, y, z = np.meshgrid(x, y, z)
    
    u, v, w = func(x, y, z)
    
    ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
    
    # Agregar títulos a los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

def vector_field_func(x, y, z):
    """
    Ejemplo de función que define un campo vectorial.
    """
    u = -y
    v = x
    w = np.zeros_like(z)
    return u, v, w
