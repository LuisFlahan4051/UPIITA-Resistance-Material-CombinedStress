import numpy as np
from matplotlib import pyplot as plt 
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def getENG(magnitud):
    exponent = int(np.floor(np.log10(abs(magnitud)) / 3) * 3)
    mantissa = magnitud / (10 ** exponent)
    return mantissa, exponent


def drawQuiverPlotly(fig, x, y, z, u, v, w, cone_height=0.1, colorscale='Viridis', sizeref=0.2):
    """
    Dibuja vectores en un gráfico 3D de Plotly utilizando Cone para las puntas.
    
    Args:
        fig (go.Figure): Figura de Plotly donde se dibujarán los vectores.
        x, y, z (numpy.ndarray): Coordenadas de origen de los vectores.
        u, v, w (numpy.ndarray): Componentes de los vectores.
        cone_height (float): Altura relativa de los conos basada en las magnitudes.
        colorscale (str): Escala de colores para los conos.
        base_sizeref (float): Factor de escala base para el tamaño de los conos.
    """

    for i in range(len(x)):
        # Coordenadas del origen y del final del cuerpo del vector
        x_start, y_start, z_start = x[i], y[i], z[i]
        x_end = x_start + u[i] * (1 - cone_height)
        y_end = y_start + v[i] * (1 - cone_height)
        z_end = z_start + w[i] * (1 - cone_height)

        cone_u = [u[i] * cone_height]
        cone_v = [v[i] * cone_height]
        cone_w = [w[i] * cone_height]

        # Dibujar el cono (punta del vector)
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_end], z=[z_end],
            u=cone_u, v=cone_v, w=cone_w,
            colorscale=colorscale,
            sizemode='absolute',
            sizeref=sizeref,
            showscale=False,
            showlegend=False
        ))

        # Dibujar el cilindro (cuerpo del vector) usando líneas
        fig.add_trace(go.Scatter3d(
            x=[x_start, x_end],
            y=[y_start, y_end],
            z=[z_start, z_end],
            mode='lines',
            line=dict(color='blue', width=5),
            showlegend=False
        ))

def tangentVectorsAtCircle(fig,radius, zDirection=1):
    """
    Dibuja un campo de vectores tangentes a un círculo en un gráfico 3D.

    Args:
        radius (float): El radio del círculo.
        zDirection (int): La dirección en el eje Z (1 para arriba, -1 para abajo).

    Returns:
        fig (go.Figure): La figura de Plotly con los vectores tangentes.
    """
    if zDirection > 0:
        direction = -1
    else:
        direction = 1

    theta = np.linspace(0, 2 * np.pi, 30)
    X = radius * np.cos(theta)
    Y = radius * np.sin(theta)
    Z = np.zeros_like(X)
    U = direction * np.sin(theta)
    V = -direction * np.cos(theta)
    W = np.zeros_like(Z)

    
    drawQuiverPlotly(fig, x=X, y=Y, z=Z, u=U, v=V, w=W, sizeref=0.1)  # Ajustar el tamaño de los vectores
    return fig

def graphTorsionalShearStress(resultados):
    radius = 1
    amplitude = resultados['maximoEsfuerzoCortanteTorsion']
    fig = go.Figure()
    tangentVectorsAtCircle(fig,radius)
    circular_plane(radius, 0, fig)
    fig.update_layout(
        title='Esfuerzo Cortante Torsional',
        scene=dict(
            xaxis=dict(range=[-radius * 2, radius * 2]),  # Ajustar el rango de los ejes
            yaxis=dict(range=[-radius * 2, radius * 2]),  # Ajustar el rango de los ejes
            zaxis=dict(range=[-amplitude, amplitude]),    # Ajustar el rango de los ejes
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
        )
    )
    fig.show()

def graphFlexuralShearStress(resultados):
    radius = 1
    amplitude = resultados['maximoEsfuerzoCortanteX']
    fig = go.Figure()
    drawParabolicVectorsAtCicle(fig,radius)
    circular_plane(radius, 0, fig)
    fig.update_layout(
        title='Esfuerzo Cortante Flexional',
        scene=dict(
            xaxis=dict(range=[-radius * 2, radius * 2]),  # Ajustar el rango de los ejes
            yaxis=dict(range=[-radius * 2, radius * 2]),
            zaxis=dict(range=[-2, 2]),
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        showlegend=False
    )
    fig.show()


def drawParabolicVectorsAtCicle(fig,radius, direction=1, invert=True):
    """
    Dibuja vectores paralelos al eje Y o X dependiendo el argumento direction, al rededor de una circunferencia donde su tamaño decrece parabólicamente.

    Args:
        radius (float): El radio del círculo.
        direction (int): 1 para vectores en dirección X, -1 para vectores en dirección Y.
        invert (bool): Si True, invierte la dirección de los vectores.

    Returns:
        fig (go.Figure): La figura de Plotly con los vectores parabólicos.
    """
    direction = 1 if direction > 0 else -1
    theta = np.linspace(0, 2 * np.pi, 30)
    X = radius * np.cos(theta)
    Y = radius * np.sin(theta)
    Z = np.zeros_like(X)

    if invert:
        invert = 1
    else:
        invert = -1

    if direction == 1:
        r = radius * np.sin(theta)
        magnitudes = (1 - (r / radius) ** 2)
        V = invert * np.abs(magnitudes * np.sign(np.cos(theta)))
        U = np.zeros_like(Y)
    else:
        r = radius * np.cos(theta)
        magnitudes = (1 - (r / radius) ** 2)
        U = invert * np.abs(magnitudes * np.sign(np.sin(theta)))
        V = np.zeros_like(X)

    W = np.zeros_like(Z)

    drawQuiverPlotly(fig,x=X, y=Y, z=Z, u=U, v=V, w=W, sizeref=0.1)

def drawNormalVectorAtSurface(fig,radius, esfuerzoNormalPromedio, originPlane=0, height=1):
    """
    Dibuja vectores normales a la superficie de un cilindro en toda la matriz del círculo.

    Args:
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.
        esfuerzoNormalPromedio (float): El esfuerzo normal promedio.
        originPlane (float): La altura en el eje Z donde se dibujarán los vectores.

    Returns:
        fig (go.Figure): La figura de Plotly con los vectores normales.
    """
    theta = np.linspace(0, 2 * np.pi, 20)
    r = np.linspace(0, radius, 5)
    theta, r = np.meshgrid(theta, r)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.ones_like(x) * originPlane
    u = np.zeros_like(x)
    v = np.zeros_like(y)
    w = np.ones_like(z) * height

    drawQuiverPlotly(fig, x.flatten(), y.flatten(), z.flatten(), u.flatten(), v.flatten(), w.flatten(), sizeref=height/10)

def graphPerpendicularStress(resultados, radius=1):
    radius, radiusExponent = getENG(radius)
    normalStress = resultados['esfuerzoNormalPromedio']
    normalStress, exponentStress = getENG(normalStress)

    fig = go.Figure()
    drawNormalVectorAtSurface(fig,radius, normalStress, 0, normalStress)
    circular_plane(radius, 0, fig)
    circular_plane(radius, normalStress, fig, alpha=0.1)
    fig.update_layout(
        title='Esfuerzo Normal Perpendicular',
        scene=dict(
            xaxis=dict(range=[-radius, radius]),
            yaxis=dict(range=[-radius, radius]),
            zaxis=dict(range=[0, normalStress]),
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        showlegend=False
    )
    # Agregar etiquetas para los exponentes
    fig.add_annotation(
        x=0, y=0, xref='paper', yref='paper',
        text=f'Escala Mx: e{np.abs(exponentStress)} \n Escala Radio: e{radiusExponent}',
        showarrow=False, font=dict(size=12)
    )
    fig.show()


def drawVector2D(fig, x_start, y_start, x_end, y_end, color='blue'):
    """
    Dibuja un vector en un gráfico 2D de Plotly utilizando una línea y un triángulo para la punta.
    
    Args:
        fig (go.Figure): Figura de Plotly donde se dibujará el vector.
        x_start, y_start (float): Coordenadas de origen del vector.
        x_end, y_end (float): Coordenadas del final del vector.
        color (str): Color del vector.
    """
    # Dibujar la línea del vector
    fig.add_trace(go.Scatter(
        x=[x_start, x_end],
        y=[y_start, y_end],
        mode='lines',
        line=dict(color=color, width=2)
    ))

    # Calcular las coordenadas del triángulo para la punta del vector
    cone_height = 0.1
    cone_base = 0.05
    direction = np.array([x_end - x_start, y_end - y_start])
    direction = direction / np.linalg.norm(direction)  # Normalizar la dirección
    normal = np.array([-direction[1], direction[0]])  # Vector normal en 2D
    p1 = np.array([x_end, y_end])
    p2 = p1 - cone_height * direction + cone_base * normal
    p3 = p1 - cone_height * direction - cone_base * normal

    # Dibujar el triángulo para la punta del vector
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0], p3[0], p1[0]],
        y=[p1[1], p2[1], p3[1], p1[1]],
        fill='toself',
        fillcolor=color,
        line=dict(color=color),
        mode='lines'
    ))

def graphStress(resultados):
    theta = np.linspace(0, 360, 100)
    eX = resultados['maximoEsfuerzoNormalFlexionanteX'] * np.sin(np.radians(theta))
    eY = resultados['maximoEsfuerzoNormalFlexionanteY'] * np.cos(np.radians(theta))
    eN = resultados['esfuerzoNormalPromedio'] * np.ones_like(theta)

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Esfuerzo Normal por Mx', 'Esfuerzo Normal por My', 'Esfuerzo Normal'))

    # Pintar el área debajo de la curva y agregar vectores perpendiculares
    fig.add_trace(go.Scatter(x=theta, y=eX, mode='lines', name='Esfuerzo Normal por Mx', line=dict(color='blue'), fill='tozeroy'), row=1, col=1)
    fig.add_trace(go.Scatter(x=theta, y=eY, mode='lines', name='Esfuerzo Normal por My', line=dict(color='green'), fill='tozeroy'), row=2, col=1)
    fig.add_trace(go.Scatter(x=theta, y=eN, mode='lines', name='Esfuerzo Normal', line=dict(color='red'), fill='tozeroy'), row=3, col=1)

# Configurar el formato del eje Y para mostrar en notación científica
    fig.update_yaxes(tickformat=".1e", row=1, col=1)
    fig.update_yaxes(tickformat=".1e", row=2, col=1)
    fig.update_yaxes(tickformat=".1e", row=3, col=1)

    fig.update_layout(height=900, width=700, title_text="Esfuerzos Normales")
    fig.show()

def graphNormalStressOfMoment(resultados, radius=1):
    radius, radius_exponent = getENG(radius)
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'surface'}, {'type': 'surface'}]], subplot_titles=("Esfuerzo Normal por Mx", "Esfuerzo Normal por My"))

    amplitude_x = resultados['maximoEsfuerzoNormalFlexionanteX']
    amplitude_x, exponent_x = getENG(amplitude_x)

    amplitude_y = resultados['maximoEsfuerzoNormalFlexionanteY']
    amplitude_y, exponent_y = getENG(amplitude_y)

    fig1 = waveAtCylinder(radius, amplitude_x, 1, 0)
    circular_plane(radius, 0, fig1)
    fig2 = waveAtCylinder(radius, amplitude_y, 1, np.pi/2)
    circular_plane(radius, 0, fig2)

    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

    # Agregar etiquetas para los exponentes
    fig.add_annotation(
        x=0, y=0, xref='paper', yref='paper',
        text=f'Escala Mx: e{np.abs(exponent_x)} \n Escala Radio: e{radius_exponent}',
        showarrow=False, font=dict(size=12)
    )

    fig.update_layout(height=600, width=1200, title_text="Esfuerzo Normal por Momento")
    fig.show()

def waveAtCylinder(radius, amplitude, cycles, phase, alpha=0.5):
    """
    Dibuja una onda senoidal sobre la superficie de un cilindro.

    Args:
        radius (float): El radio del cilindro.
        amplitude (float): La amplitud de la onda senoidal.
        cycles (int): El número de ciclos de la onda senoidal.
        phase (float): La fase de la onda senoidal.

    Returns:
        fig (go.Figure): La figura de Plotly con la onda senoidal.
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, 1, 100)
    Theta, z = np.meshgrid(theta, z)
    X = radius * np.cos(Theta)
    Y = radius * np.sin(Theta)
    Z = amplitude * np.sin(cycles * Theta + phase) * z

    # Dibujar vectores desde z=0 hasta la superficie
    indices = np.arange(0, len(theta), 4)  # Seleccionar algunos índices
    X_vec = X[0, indices]
    Y_vec = Y[0, indices]
    Z_vec = np.zeros_like(X_vec)
    U = np.zeros_like(X_vec)
    V = np.zeros_like(Y_vec)
    W = amplitude * np.sin(cycles * theta[indices] + phase)


    fig = go.Figure()
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=alpha,showlegend=False,showscale=False))
    drawQuiverPlotly(fig, x=X_vec, y=Y_vec, z=Z_vec, u=U, v=V, w=W, sizeref=amplitude/10 )
    return fig

def solid_cylinder(fig,radius, height):
    """
    Dibuja un cilindro sólido en un gráfico 3D.

    Args:
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.

    Returns:
        fig (go.Figure): La figura de Plotly con el cilindro sólido.
    """
    
    cylinder(0, radius, height, fig)
    circular_plane(radius, 0, fig)
    circular_plane(radius, height, fig)

def cylinder(origin, radius, height, fig):
    """
    Dibuja un cilindro en un gráfico 3D.

    Args:
        origin (float): La coordenada Z de origen del cilindro.
        radius (float): El radio del cilindro.
        height (float): La altura del cilindro.
        fig (go.Figure): La figura de Plotly donde se dibujará el cilindro.

    Returns:
        fig (go.Figure): La figura de Plotly con el cilindro.
    """
    z = np.linspace(origin, height, 20)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Viridis',showlegend=False,showscale=False))

def circular_plane(radius, height, fig, alpha=0.5):
    """
    Dibuja un plano circular en un gráfico 3D.

    Args:
        radius (float): El radio del plano circular.
        height (float): La altura en el eje Z donde se dibujará el plano circular.
        fig (go.Figure): La figura de Plotly donde se dibujará el plano circular.
        alpha (float): Transparencia del plano circular.

    Returns:
        fig (go.Figure): La figura de Plotly con el plano circular.
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    radius = np.linspace(0, radius, 50)
    theta, radius = np.meshgrid(theta, radius)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.ones_like(x) * height

    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Viridis', opacity=alpha, showlegend=False, showscale=False))