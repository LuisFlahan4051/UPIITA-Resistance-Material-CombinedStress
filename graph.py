import numpy as np
from matplotlib import pyplot as plt 
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors

def graphStress(esfuerzoNormal, esfuerzoCortanteX, esfuerzoCortanteY, maximoEsfuerzoNormalFlexionanteX, maximoEsfuerzoNormalFlexionanteY, maximoEsfuerzoCortanteTorsion):
    fig = plt.figure()
    ax = fig.add_subplot(311)
    # ax11 = fig.add_subplot(322, projection='3d')
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    theta = np.linspace(0,360,100)
    eX = maximoEsfuerzoNormalFlexionanteX*np.sin(np.radians(theta))
    eY = maximoEsfuerzoNormalFlexionanteY*np.cos(np.radians(theta))
    eN = esfuerzoNormal*np.ones_like(theta)

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
    input("Press Enter to continue...")

def testGraphFunctions():
    fig = plt.figure()
    axis = fig.add_subplot(121, projection='3d')

    solid_cylinder(1, 1, axis)

    # Agregar títulos a los ejes
    axis.set_title('Cilindro')
    axis.set_xlabel('Eje X')
    axis.set_ylabel('Eje Y')
    axis.set_zlabel('Eje Z')
    
    axis2 = fig.add_subplot(122, projection='3d')
    #draw_vector(axis2, (0, 0, 0), (1, 1, 1))
    draw_vector_field(axis2, vector_field_func, (-1, 1), (-1, 1), (-1, 1), density=5)
    
    plt.show()


def sinusoide():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()

def cylinder(origin,radius, height, axis):
    z = np.linspace(origin, height, 20)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    
    axis.plot_surface(x, y, z, cmap='viridis')

def circular_plane(radius, height, axis):
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
    axis.plot_surface(x, y, z, cmap='viridis')

def solid_cylinder(radius, height, axis):
    cylinder(0, radius, height, axis)
    circular_plane(radius, 0, axis)
    circular_plane(radius, height, axis)

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
