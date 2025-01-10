import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Mesh3d

from engine import getENG


" ------------------ graph functions ------------------ "

def graphTorsionalShearStress(maximoEsfuerzoCortanteTorsion=1, radius=1):
    radius = 1
    amplitude = maximoEsfuerzoCortanteTorsion
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
    return fig

def graphFlexuralShearStress(maximoEsfuerzoCortante=1, radius=1, direction=1):
    radius = 1
    amplitude = maximoEsfuerzoCortante
    fig = go.Figure()
    drawParabolicVectorsAtCicle(fig,radius, direction=direction)
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
    return fig

def graphNormalStress(esfuerzoNormalPromedio=1, radius=1, density=20):
    radius, radiusExponent = getENG(radius)
    normalStress = esfuerzoNormalPromedio
    normalStress, exponentStress = getENG(normalStress)

    fig = go.Figure()
    drawNormalVectorAtSurface(fig,radius, normalStress, 0, normalStress, density)
    circular_plane(radius, 0, fig)
    circular_plane(radius, normalStress, fig, alpha=0.1)
    # fig.update_layout(
    #     title='Esfuerzo Normal Perpendicular',
    #     scene=dict(
    #         xaxis=dict(range=[-radius, radius]),
    #         yaxis=dict(range=[-radius, radius]),
    #         zaxis=dict(range=[0, normalStress]),
    #         xaxis_title='X',
    #         yaxis_title='Y',
    #         zaxis_title='Z'
    #     ),
    #     showlegend=False
    # )
    # # Agregar etiquetas para los exponentes
    # fig.add_annotation(
    #     x=0, y=0, xref='paper', yref='paper',
    #     text=f'Escala Mx: e{np.abs(exponentStress)} \n Escala Radio: e{radiusExponent}',
    #     showarrow=False, font=dict(size=12)
    # )
    return fig

def graphStress(maximoEsfuerzoNormalFlexionanteX, maximoEsfuerzoNormalFlexionanteY, esfuerzoNormalPromedio, radius=1):
    theta = np.linspace(0, 360, 100)
    eX = maximoEsfuerzoNormalFlexionanteX * np.sin(np.radians(theta))
    eY = maximoEsfuerzoNormalFlexionanteY * np.cos(np.radians(theta))
    eN = esfuerzoNormalPromedio * np.ones_like(theta)

    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    # Pintar el área debajo de la curva y agregar vectores perpendiculares
    fig1.add_trace(go.Scatter(x=theta, y=eX, mode='lines', name='Esfuerzo Normal por Mx', line=dict(color='blue'), fill='tozeroy'))
    fig2.add_trace(go.Scatter(x=theta, y=eY, mode='lines', name='Esfuerzo Normal por My', line=dict(color='green'), fill='tozeroy'))
    fig3.add_trace(go.Scatter(x=theta, y=eN, mode='lines', name='Esfuerzo Normal', line=dict(color='red'), fill='tozeroy'))
    
    return fig1, fig2, fig3

def graphNormalStressOfMoment(maximoEsfuerzoNormalFlexionanteX,maximoEsfuerzoNormalFlexionanteY , radius=1):
    radius, radius_exponent = getENG(radius)
    # fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'surface'}, {'type': 'surface'}]], subplot_titles=("Esfuerzo Normal por Mx", "Esfuerzo Normal por My"))

    amplitude_x = maximoEsfuerzoNormalFlexionanteX
    amplitude_x, exponent_x = getENG(amplitude_x)

    amplitude_y = maximoEsfuerzoNormalFlexionanteY
    amplitude_y, exponent_y = getENG(amplitude_y)

    fig1 = waveAtCylinder(radius, amplitude_x, 1, 0)
    circular_plane(radius, 0, fig1)
    fig2 = waveAtCylinder(radius, amplitude_y, 1, np.pi/2)
    circular_plane(radius, 0, fig2)

    # for trace in fig1.data:
    #     fig.add_trace(trace, row=1, col=1)
    # for trace in fig2.data:
    #     fig.add_trace(trace, row=1, col=2)

    # Agregar etiquetas para los exponentes
    # fig.add_annotation(
    #     x=0, y=0, xref='paper', yref='paper',
    #     text=f'Escala Mx: e{np.abs(exponent_x)} \n Escala Radio: e{radius_exponent}',
    #     showarrow=False, font=dict(size=12)
    # )

    # fig.update_layout(height=600, width=1200, title_text="Esfuerzo Normal por Momento")
    # fig.show()
    return fig1, fig2

def graphEstructure():
    fig = go.Figure()
    solid_cylinder(fig, 1, 1)
    fig.update_layout(
        title='Estructura de un cilindro sólido',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
    ))

" ------------------ drawing functions ------------------ "
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

def drawNormalVectorAtSurface(fig,radius, esfuerzoNormalPromedio, originPlane=0, height=1, density=20):
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
    theta = np.linspace(0, 2 * np.pi, density)
    r = np.linspace(0, radius, 5)
    theta, r = np.meshgrid(theta, r)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.ones_like(x) * originPlane
    u = np.zeros_like(x)
    v = np.zeros_like(y)
    w = np.ones_like(z) * height

    drawQuiverPlotly(fig, x.flatten(), y.flatten(), z.flatten(), u.flatten(), v.flatten(), w.flatten(), sizeref=height/10)

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

def drawCylinderPointToPoint(initial_point, final_point, radius, fig):
    # Convert points to numpy arrays
    initial_point = np.array(initial_point)
    final_point = np.array(final_point)
    
    # Calculate the vector for the cylinder's axis
    axis_vector = final_point - initial_point
    height = np.linalg.norm(axis_vector)
    axis_unit_vector = axis_vector / height
    
    # Define the virtual z and theta in cylindrical coordinates
    z_virtual = np.linspace(0, height, 20)
    theta_virtual = np.linspace(0, 2 * np.pi, 100)
    theta_virtual, z_virtual = np.meshgrid(theta_virtual, z_virtual)
    
    # Calculate the virtual x, y in cylindrical coordinates
    x_virtual = radius * np.cos(theta_virtual)
    y_virtual = radius * np.sin(theta_virtual)
    
    # Convert the cylindrical coordinates to Cartesian coordinates in the local frame
    cylinder_points = np.array([x_virtual.ravel(), y_virtual.ravel(), z_virtual.ravel()]).T
    
    # Find a rotation matrix to align the cylinder with the axis vector
    z_axis = np.array([0, 0, 1])  # Default axis
    rotation_axis = np.cross(z_axis, axis_unit_vector)
    rotation_axis_norm = np.linalg.norm(rotation_axis)
    
    if rotation_axis_norm != 0:  # Check if rotation is needed
        rotation_axis = rotation_axis / rotation_axis_norm
        angle = np.arccos(np.dot(z_axis, axis_unit_vector))
        K = np.array([[0, -rotation_axis[2], rotation_axis[1]],
                      [rotation_axis[2], 0, -rotation_axis[0]],
                      [-rotation_axis[1], rotation_axis[0], 0]])
        rotation_matrix = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
    else:
        rotation_matrix = np.eye(3)
    
    # Rotate and translate the points
    rotated_points = cylinder_points @ rotation_matrix.T
    final_points = rotated_points + initial_point
    
    # Reshape for plotting
    x = final_points[:, 0].reshape(x_virtual.shape)
    y = final_points[:, 1].reshape(y_virtual.shape)
    z = final_points[:, 2].reshape(z_virtual.shape)
    
    # Add the cylinder to the figure
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale="Viridis"))

def drawPrismPointToPoint(initial_point, final_point, width, height, fig):
    # Convert points to numpy arrays
    initial_point = np.array(initial_point)
    final_point = np.array(final_point)
    
    # Calculate the vector for the prism's axis
    axis_vector = final_point - initial_point
    length = np.linalg.norm(axis_vector)
    axis_unit_vector = axis_vector / length
    
    # Define a local orthonormal basis
    z_axis = np.array([0, 0, 1])
    if not np.allclose(axis_unit_vector, z_axis):
        v = np.cross(z_axis, axis_unit_vector)
        v = v / np.linalg.norm(v)
        K = np.array([[0, -v[2], v[1]],
                      [v[2], 0, -v[0]],
                      [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + np.sin(np.arccos(np.dot(z_axis, axis_unit_vector))) * K + \
                          (1 - np.cos(np.arccos(np.dot(z_axis, axis_unit_vector)))) * (K @ K)
    else:
        rotation_matrix = np.eye(3)
    
    # Define the vertices of the prism in the local frame
    w, h = width / 2, height / 2
    local_vertices = np.array([
        [-w, -h, 0], [w, -h, 0], [w, h, 0], [-w, h, 0],  # Bottom face
        [-w, -h, length], [w, -h, length], [w, h, length], [-w, h, length]  # Top face
    ])
    
    # Transform the vertices to global coordinates
    rotated_vertices = local_vertices @ rotation_matrix.T
    global_vertices = rotated_vertices + initial_point
    
    # Define faces for the prism
    faces = [
        [0, 1, 5, 4],  # Front face
        [1, 2, 6, 5],  # Right face
        [2, 3, 7, 6],  # Back face
        [3, 0, 4, 7],  # Left face
        [0, 1, 2, 3],  # Bottom face
        [4, 5, 6, 7]   # Top face
    ]
    
    # Add the prism to the figure
    for face in faces:
        fig.add_trace(go.Mesh3d(
            x=global_vertices[face, 0],
            y=global_vertices[face, 1],
            z=global_vertices[face, 2],
            color='blue',
            opacity=0.5
        ))

def drawIPRprofile(initial_point, final_point, alma_width, patin_width, patin, peralte, fig):
    # Convert points to numpy arrays
    initial_point = np.array(initial_point)
    final_point = np.array(final_point)
    
    # Calculate the vector for the profile's axis
    axis_vector = final_point - initial_point
    length = np.linalg.norm(axis_vector)
    axis_unit_vector = axis_vector / length
    
    # Define a local orthonormal basis
    z_axis = np.array([0, 0, 1])
    if not np.allclose(axis_unit_vector, z_axis):
        v = np.cross(z_axis, axis_unit_vector)
        v = v / np.linalg.norm(v)
        K = np.array([[0, -v[2], v[1]],
                      [v[2], 0, -v[0]],
                      [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + np.sin(np.arccos(np.dot(z_axis, axis_unit_vector))) * K + \
                          (1 - np.cos(np.arccos(np.dot(z_axis, axis_unit_vector)))) * (K @ K)
    else:
        rotation_matrix = np.eye(3)
    
    # Dimensions for the profile
    h = peralte / 2
    a = alma_width / 2
    p = patin_width / 2
    pt = patin / 2
    
    # Define vertices for the profile in the local frame
    local_vertices = np.array([
        # Bottom patín
        [-p, -h, 0], [p, -h, 0], [p, -h + pt, 0], [-p, -h + pt, 0],
        # Alma
        [-a, -h + pt, 0], [a, -h + pt, 0], [a, h - pt, 0], [-a, h - pt, 0],
        # Top patín
        [-p, h - pt, 0], [p, h - pt, 0], [p, h, 0], [-p, h, 0],
        # Repeat top layer (for extrusion)
        [-p, -h, length], [p, -h, length], [p, -h + pt, length], [-p, -h + pt, length],
        [-a, -h + pt, length], [a, -h + pt, length], [a, h - pt, length], [-a, h - pt, length],
        [-p, h - pt, length], [p, h - pt, length], [p, h, length], [-p, h, length]
    ])
    
    # Transform the vertices to global coordinates
    rotated_vertices = local_vertices @ rotation_matrix.T
    global_vertices = rotated_vertices + initial_point
    
    # Define faces for the profile
    faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],  # Bottom, alma, top patín
        [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23],  # Bottom, alma, top patín (extruded)
        [0, 1, 13, 12], [1, 2, 14, 13], [2, 3, 15, 14], [3, 0, 12, 15],  # Bottom patín sides
        [4, 5, 17, 16], [5, 6, 18, 17], [6, 7, 19, 18], [7, 4, 16, 19],  # Alma sides
        [8, 9, 21, 20], [9, 10, 22, 21], [10, 11, 23, 22], [11, 8, 20, 23]  # Top patín sides
    ]
    
    # Add the profile to the figure
    for face in faces:
        fig.add_trace(go.Mesh3d(
            x=global_vertices[face, 0],
            y=global_vertices[face, 1],
            z=global_vertices[face, 2],
            color='red',
            opacity=0.5
        ))

def drawArrowMoment(point, fig, radius=1, axis="x", invertDirection=False):
    # Convert point to numpy array
    point = np.array(point)
    
    # Define the arrow's direction
    if axis == "x":
        angle = np.linspace(0, 1.5 * np.pi, 100)  # Circle not closed completely
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = np.zeros_like(x)
        u, v, w = [1, 0, 0]
    elif axis == "y":
        angle = np.linspace(0, 1.5 * np.pi, 100)
        x = radius * np.cos(angle)
        z = radius * np.sin(angle)
        y = np.zeros_like(x)
        u, v, w = [0, 1, 0]
    else:
        angle = np.linspace(0, 1.5 * np.pi, 100)
        y = radius * np.cos(angle)
        z = radius * np.sin(angle)
        x = np.zeros_like(y)
        u, v, w = [0, 0, 1]
    
    # Invert the direction if needed
    if invertDirection:
        angle = -angle
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = np.zeros_like(x)
        if axis == "x":
            u, v, w = [-1, 0, 0]
        elif axis == "y":
            u, v, w = [0, -1, 0]
        else:
            u, v, w = [0, 0, -1]
    
    # Add the arrow to the figure
    fig.add_trace(go.Scatter3d(x=x + point[0], y=y + point[1], z=z + point[2], mode='lines', line=dict(color='blue', width=5)))
    
    # Add the cone at the end of the arrow
    if invertDirection:
        fig.add_trace(go.Cone(
        x=[x[-1] + point[0]], y=[y[-1] + point[1]], z=[z[-1] + point[2]],
        u=[-u], v=[-v], w=[-w],
        colorscale='Viridis',
        sizemode='absolute',
        sizeref=0.1,
        showscale=False,
        showlegend=False
    ))
    else:
        fig.add_trace(go.Cone(
        x=[x[-1] + point[0]], y=[y[-1] + point[1]], z=[z[-1] + point[2]],
        u=[u], v=[v], w=[w],
        colorscale='Viridis',
        sizemode='absolute',
        sizeref=0.1,
        showscale=False,
        showlegend=False
    ))

    
