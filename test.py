import plotly.graph_objects as go
import numpy as np

def graficar_circulo_mohr(sigma_x, sigma_y, tau_xy):
    sigma_prom = (sigma_x + sigma_y) / 2
    radio = np.sqrt(((sigma_x - sigma_y) / 2) ** 2 + tau_xy ** 2)

    theta = np.linspace(0, 2 * np.pi, 100)
    sigma = sigma_prom + radio * np.cos(theta)
    tau = radio * np.sin(theta)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigma, y=tau, mode='lines', name='Círculo de Mohr'))
    fig.add_trace(go.Scatter(x=[sigma_prom], y=[0], mode='markers', marker=dict(color='red'), name='Centro'))
    fig.add_trace(go.Scatter(x=[sigma_x, sigma_y], y=[tau_xy, -tau_xy], mode='markers', marker=dict(color='green'), name='Puntos de tensión'))
    fig.update_layout(
        title='Círculo de Mohr',
        xaxis_title='Tensión Normal (σ)',
        yaxis_title='Tensión Cortante (τ)',
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis_zeroline=True,
        yaxis_zeroline=True,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def graficar_circulo_mohr_3d(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx):
    # Tensor de tensiones
    T = np.array([
        [sigma_x, tau_xy, tau_zx],
        [tau_xy, sigma_y, tau_yz],
        [tau_zx, tau_yz, sigma_z]
    ])
    # Tensiones principales (autovalores de T)
    tensiones_principales = np.linalg.eigvalsh(T)
    sigma_1, sigma_2, sigma_3 = sorted(tensiones_principales, reverse=True)

    # Círculos
    centros = [(sigma_1 + sigma_2) / 2, (sigma_2 + sigma_3) / 2, (sigma_3 + sigma_1) / 2]
    radios = [np.abs(sigma_1 - sigma_2) / 2, np.abs(sigma_2 - sigma_3) / 2, np.abs(sigma_3 - sigma_1) / 2]

    fig = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 100)
    for centro, radio in zip(centros, radios):
        sigma = centro + radio * np.cos(theta)
        tau = radio * np.sin(theta)
        fig.add_trace(go.Scatter3d(x=sigma, y=tau, z=np.zeros_like(sigma), mode='lines'))

    fig.update_layout(
        title='Círculo de Mohr en 3D',
        scene=dict(
            xaxis_title='Tensión Normal (σ)',
            yaxis_title='Tensión Cortante (τ)',
            zaxis_title='Tensión Cortante (τ)',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    return fig

def graficar_circulo_mohr_3d_esferas(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx):
    """
    Grafica el círculo de Mohr en 3D usando Plotly.

    Args:
        sigma_x: Tensión normal en el eje x.
        sigma_y: Tensión normal en el eje y.
        sigma_z: Tensión normal en el eje z.
        tau_xy: Tensión cortante en el plano xy.
        tau_yz: Tensión cortante en el plano yz.
        tau_zx: Tensión cortante en el plano zx.
    """

    # Tensiones principales
    sigma_1 = (sigma_x + sigma_y) / 2 + np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)
    sigma_2 = (sigma_x + sigma_y) / 2 - np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)
    sigma_3 = sigma_z

    # Centros y radios de los círculos
    centros = [(sigma_1 + sigma_2) / 2, (sigma_2 + sigma_3) / 2, (sigma_3 + sigma_1) / 2]
    radios = [np.abs(sigma_1 - sigma_2) / 2, np.abs(sigma_2 - sigma_3) / 2, np.abs(sigma_3 - sigma_1) / 2]

    # Crear la figura
    fig = go.Figure()

    # Generar puntos para las esferas
    phi = np.linspace(0, np.pi, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    phi, theta = np.meshgrid(phi, theta)

    for centro, radio in zip(centros, radios):
        x = centro + radio * np.sin(phi) * np.cos(theta)
        y = radio * np.sin(phi) * np.sin(theta)
        z = radio * np.cos(phi)
        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.5, name=f'Esfera con centro en {centro}'))

    # Configurar el diseño
    fig.update_layout(
        title='Círculo de Mohr en 3D',
        scene=dict(
            xaxis_title='Tensión Normal (σ)',
            yaxis_title='Tensión Cortante (τ)',
            zaxis_title='Tensión Cortante (τ)',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    return fig

# Ejemplo de uso
# graficar_circulo_mohr(20, -10, 15)
# graficar_circulo_mohr_3d(100, 50, 30, 25, 15, 10)
# graficar_circulo_mohr_3d_esferas(100, 50, 30, 25, 15, 10)

def run_app():
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    global estructure
    estructure = go.Figure()

    global dataBarsTable
    dataBarsTable = MainWindow.findChild(QtWidgets.QTableWidget, 'dataBarsTable')
    headersBars = ['Origen X', 
               'Origen Y', 
               'Origen Z', 
               'Extremo X', 
               'Extremo Y', 
               'Extremo Z', 
               'Eje Normal',
               'Material', 
               'Módulo E', 
               'Módulo G',
               'Perfil', 
               'Diámetro Interno', 
               'Diámetro Externo', 
               'Lado 1', 
               'Lado 2', 
               'Eje RH', 
               'Peralte', 
               'Ancho Peralte', 
               'Patin', 
               'Ancho Patin', 
               'Eje IPR'] 
    dataBarsTable.setColumnCount(len(headersBars))
    replaceHeaders(dataBarsTable, headersBars)

    updateBtn = MainWindow.findChild(QtWidgets.QPushButton, 'updateBtn')
    updateBtn.clicked.connect(lambda: (
        updateStructures()
    ))

    MainWindow.show()
    
    sys.exit(app.exec())

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

def updateStructures():

    row_count = dataBarsTable.rowCount()
    initialPoint = [0,0,0]
    endPoint = [1,1,1]
    radius = 1
    drawCylinderPointToPoint(initial_point=initialPoint, final_point=endPoint, radius=radius, fig=estructure)
    for row in range(row_count):
        if dataBarsTable.item(row, 10).text() == "Circular":
            # initialPoint = [float(dataBarsTable.item(row, 0).text()), float(dataBarsTable.item(row, 1).text()), float(dataBarsTable.item(row, 2).text())]
            # endPoint = [float(dataBarsTable.item(row, 3).text()), float(dataBarsTable.item(row, 4).text()), float(dataBarsTable.item(row, 5).text())]
            # diameter = float(dataBarsTable.item(row, 12).text())
            # radius = diameter / 2
            print("ejecutando")
            plotNormalStress(results=engine.engine())


def plotNormalStress(results):
    global estructure

    profile = engine.Profile('circle',40*10**-3)

    # Crear subplots
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Esfuerzo Normal", "Esfuerzo Por Flexión", "Esfuerzo Por Flexión", "Gráfica 4"))

    # Añadir superficies a los subplots
    fig1 = graphNormalStress(results["esfuerzoNormalPromedio"], radius=profile.radius, density=10)
    fig3, fig2= graphNormalStressOfMoment(results["maximoEsfuerzoNormalFlexionanteX"], results["maximoEsfuerzoNormalFlexionanteY"],radius=profile.radius)



    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)
    for trace in estructure.data:
        fig.add_trace(trace, row=1, col=4)

    
    # Ajustar el tamaño de cada gráfica
    fig.update_layout(
        title='Esfuerzos Normales',
        height=350,  # Altura total de la figura
        width=1500,  # Ancho total de la figura
        scene=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            zaxis_title='Eje Z'
        ),
        scene2=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            zaxis_title='Eje Z'
        ),
        scene3=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            zaxis_title='Eje Z'
        ),
        scene4=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            zaxis_title='Eje Z'
        )
    )

    # Guardar la figura en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        fig.write_html(tmpfile.name)
        tmpfile.flush()
        tmpfile.seek(0)
        html_file = tmpfile.name

    return html_file