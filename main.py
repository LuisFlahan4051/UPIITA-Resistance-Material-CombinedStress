from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QComboBox, QDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import tempfile

import graph
import engine
from engine import n, u, m, k, M, G, T, cord_x, cord_y, cord_z
import test

def main():
    run_app()

estructure = go.Figure()

def run_app():
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
   
    MainWindow = QtWidgets.QMainWindow()
   
    loader = QtUiTools.QUiLoader()
    file = QtCore.QFile("./main.ui")
    file.open(QtCore.QFile.ReadOnly)
    MainWindow = loader.load(file)
    file.close()
    
    results = engine.engine()

    dataTable = MainWindow.findChild(QtWidgets.QTableWidget, 'dataTable')
    dataTable.setColumnCount(8)  # Establecer el número de columnas
    dataTable.setHorizontalHeaderLabels(['x', 'y','z','Apoyo','Tipo Apoyo','fx','fy','fz'])
    
    outDataTable = MainWindow.findChild(QtWidgets.QTableWidget, 'outDataTable')
    outDataTable.setColumnCount(100)
    outDataTable.setRowCount(3)
    outDataTable.setVerticalHeaderLabels(['Esfuerzo Normal por Mx','Esfuerzo Normal por My','Esfuerzo Normal'])
    setResultValuesToTable(outDataTable, results)

    addLoadPoint = MainWindow.findChild(QtWidgets.QPushButton, 'addLoadPoint')
    addLoadPoint.clicked.connect(lambda: showLoadPointEntry(MainWindow))

    addBar = MainWindow.findChild(QtWidgets.QPushButton, 'addBar')
    addBar.clicked.connect(lambda: showBarEntry(MainWindow))

    add_row_with_checkbox(dataTable)
    
    graphLayout = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout1')
    web_view = QWebEngineView()
    graphLayout.addWidget(web_view)

    
    
    normalStress = MainWindow.findChild(QtWidgets.QRadioButton, 'normalStress')
    normalStress2D = MainWindow.findChild(QtWidgets.QRadioButton, 'normalStress2D')
    shearStress = MainWindow.findChild(QtWidgets.QRadioButton, 'shearStress')
    mohrStress = MainWindow.findChild(QtWidgets.QRadioButton, 'mohr')
    
    plot1 = plotNormalStress(results)
    plot2 = plotShearStress(results)
    plot3 = plotNormalStress2D(results)
    plotMohrFile = plotMohr(results)

    normalStress.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot1))))
    shearStress.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot2))))
    normalStress2D.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot3))))
    
    mohrStress.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plotMohrFile))
    ))




    MainWindow.show()
    
    sys.exit(app.exec())

def showLoadPointEntry(parent):
    loader = QtUiTools.QUiLoader()
    file = QtCore.QFile("./addPointForce.ui")
    file.open(QtCore.QFile.ReadOnly)
    dialog = loader.load(file, parent)
    file.close()

    dialog_fx = dialog.findChild(QtWidgets.QLineEdit, 'dialog_fx')
    dialog_fy = dialog.findChild(QtWidgets.QLineEdit, 'dialog_fy')
    dialog_fz = dialog.findChild(QtWidgets.QLineEdit, 'dialog_fz')
    dialog_px = dialog.findChild(QtWidgets.QLineEdit, 'dialog_px')
    dialog_py = dialog.findChild(QtWidgets.QLineEdit, 'dialog_py')
    dialog_pz = dialog.findChild(QtWidgets.QLineEdit, 'dialog_pz')
    dialog_mx = dialog.findChild(QtWidgets.QLineEdit, 'dialog_mx')
    dialog_my = dialog.findChild(QtWidgets.QLineEdit, 'dialog_my')
    dialog_mz = dialog.findChild(QtWidgets.QLineEdit, 'dialog_mz')

    # Conectar el botón de aceptar
    if dialog.exec() == QDialog.Accepted:
        
        # Aquí puedes agregar el código para manejar los datos ingresados
        print(f"aceptar")

def updateModule(comboBoxMaterial, moduleE, moduleG):
    selected_material = comboBoxMaterial.currentText()
    if selected_material in engine.materials:
        E_value = engine.materials[selected_material]["E"]
        moduleE.setText(str(E_value))
        G_value = engine.materials[selected_material]["G"]
        moduleG.setText(str(G_value))

def showBarEntry(parent):
    loader = QtUiTools.QUiLoader()
    file = QtCore.QFile("./addBar.ui")
    file.open(QtCore.QFile.ReadOnly)
    dialog = loader.load(file, parent)
    file.close()

    comboBoxPerfil = dialog.findChild(QtWidgets.QComboBox, 'comboBoxPerfil')
    comboBoxPerfil.addItem("Circular")
    comboBoxPerfil.addItem("Rectangular")
    comboBoxPerfil.addItem("IPR")
    comboBoxMaterial = dialog.findChild(QtWidgets.QComboBox, 'comboBoxMaterial')
    for material in engine.materials.keys():
        comboBoxMaterial.addItem(material)
    
    moduleE = dialog.findChild(QtWidgets.QLineEdit, 'moduleE')
    moduleG = dialog.findChild(QtWidgets.QLineEdit, 'moduleG')
    
    # Actualizar el valor del módulo cuando se seleccione un material
    comboBoxMaterial.currentIndexChanged.connect(lambda: updateModule(comboBoxMaterial, moduleE, moduleG))

    originX = dialog.findChild(QtWidgets.QLineEdit, 'originX')
    originY = dialog.findChild(QtWidgets.QLineEdit, 'originY')
    originZ = dialog.findChild(QtWidgets.QLineEdit, 'originZ')
    endX = dialog.findChild(QtWidgets.QLineEdit, 'endX')
    endY = dialog.findChild(QtWidgets.QLineEdit, 'endY')
    endZ = dialog.findChild(QtWidgets.QLineEdit, 'endZ')
    comboBoxNormalAxis = dialog.findChild(QtWidgets.QComboBox, 'comboBoxNormalAxis')
    comboBoxNormalAxis.addItem("x")
    comboBoxNormalAxis.addItem("y")
    comboBoxNormalAxis.addItem("z")


    # Circular Perfil
    internalDiameter = dialog.findChild(QtWidgets.QLineEdit, 'internalDiameter')
    externalDiameter = dialog.findChild(QtWidgets.QLineEdit, 'externalDiameter')

    # Rectangular Perfil
    side1 = dialog.findChild(QtWidgets.QLineEdit, 'side1')
    side2 = dialog.findChild(QtWidgets.QLineEdit, 'side2')
    comboBoxRHAxis = dialog.findChild(QtWidgets.QComboBox, 'comboBoxRHAxis')
    comboBoxRHAxis.addItem("x")
    comboBoxRHAxis.addItem("y")
    comboBoxRHAxis.addItem("z")

    # IPR Perfil
    peralte = dialog.findChild(QtWidgets.QLineEdit, 'peralte')
    widthPeralte = dialog.findChild(QtWidgets.QLineEdit, 'widthPeralte')
    patin = dialog.findChild(QtWidgets.QLineEdit, 'patin')
    widthPatin = dialog.findChild(QtWidgets.QLineEdit, 'widthPatin')
    comboBoxIPRHAxis = dialog.findChild(QtWidgets.QComboBox, 'comboBoxIPRHAxis')
    comboBoxIPRHAxis.addItem("x")
    comboBoxIPRHAxis.addItem("y")
    comboBoxIPRHAxis.addItem("z")


    # Conectar el botón de aceptar
    if dialog.exec() == QDialog.Accepted:
        
        # Aquí puedes agregar el código para manejar los datos ingresados
        print(f"aceptar")

def setResultValuesToTable(outDataTable, resultados):
    theta = np.linspace(0,360,100)
    eX = resultados['maximoEsfuerzoNormalFlexionanteX']*np.sin(np.radians(theta))
    eY = resultados['maximoEsfuerzoNormalFlexionanteY']*np.cos(np.radians(theta))
    eN = resultados['esfuerzoNormalPromedio']*np.ones_like(theta)

    for i in range(0,100):
        outDataTable.setItem(0, i, QTableWidgetItem(f"{engine.format_eng(eX[i])}"))
        outDataTable.setItem(1, i, QTableWidgetItem(f"{engine.format_eng(eY[i])}"))
        outDataTable.setItem(2, i, QTableWidgetItem(f"{engine.format_eng(eN[i])}"))
    

def add_row_with_checkbox(table_widget):
    # Obtener el número actual de filas
    row_count = table_widget.rowCount()

    
    
    # Insertar una nueva fila
    table_widget.insertRow(row_count)
    
    # Crear un QCheckBox
    checkbox = QCheckBox()
    checkbox_widget = QWidget()
    checkbox_layout = QHBoxLayout()
    checkbox_layout.addWidget(checkbox)
    checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
    checkbox_layout.setContentsMargins(0, 0, 0, 0)
    checkbox_widget.setLayout(checkbox_layout)
    
    # Crear un QComboBox
    combobox = QComboBox()
    combobox.addItem("Fijo")
    combobox.addItem("Deslizante")
    combobox.addItem("Empotrado")
    combobox_widget = QWidget()
    combobox_layout = QHBoxLayout()
    combobox_layout.addWidget(combobox)
    combobox_layout.setAlignment(QtCore.Qt.AlignCenter)
    combobox_layout.setContentsMargins(0, 0, 0, 0)
    combobox_widget.setLayout(combobox_layout)
    
    # Insertar el QCheckBox en la primera columna de la nueva fila
    table_widget.setCellWidget(row_count, 3, checkbox_widget)
    table_widget.setCellWidget(row_count, 4, combobox_widget)

    # Insertar datos de ejemplo en las otras columnas
    table_widget.setItem(row_count, 1, QTableWidgetItem("Dato 1"))
    table_widget.setItem(row_count, 2, QTableWidgetItem("Dato 2"))

def plotNormalStress2D(results):
    fig = make_subplots(rows=1, cols=4,
        subplot_titles=("Esfuerzo Normal", "Esfuerzo Por Flexión", "Esfuerzo Por Flexión", "Gráfica 4"))

    fig3, fig2, fig1 =graph.graphStress(results["maximoEsfuerzoNormalFlexionanteX"], results["maximoEsfuerzoNormalFlexionanteY"], results["esfuerzoNormalPromedio"])



    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)
    
    
    # Ajustar el tamaño de cada gráfica
    fig.update_layout(
        title='Esfuerzos Normales',
        height=350,  # Altura total de la figura
        width=1500,  # Ancho total de la figura
        scene=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
        ),
        scene2=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y'
        ),
        scene3=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y'
        ),
        scene4=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y'
        )
    )
    
    # Ajustar el formato de los ejes Y
    fig.update_yaxes(tickformat=".1e")

    # Guardar la figura en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        fig.write_html(tmpfile.name)
        tmpfile.flush()
        tmpfile.seek(0)
        html_file = tmpfile.name

    return html_file

def plotNormalStress(results):
    profile = engine.Profile('circle',40*10**-3)

    # Crear subplots
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Esfuerzo Normal", "Esfuerzo Por Flexión", "Esfuerzo Por Flexión", "Gráfica 4"))

    # Añadir superficies a los subplots
    fig1 = graph.graphNormalStress(results["esfuerzoNormalPromedio"], radius=profile.radius, density=10)
    fig3, fig2= graph.graphNormalStressOfMoment(results["maximoEsfuerzoNormalFlexionanteX"], results["maximoEsfuerzoNormalFlexionanteY"],radius=profile.radius)

    fig4 = go.Figure()
    # graph.drawPrismPointToPoint([0,0,0],[1,1,1],1,2,fig4)
    graph.drawIPRprofile([0, 0, 0], [1, 1, 1], 0.2, 0.5, 0.8,fig4)
    graph.drawArrowMoment([1, 1, 1], fig4, axis='y', invertDirection=True)
    




    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)
    for trace in fig4.data:
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
    
def plotShearStress(results):
    profile = engine.Profile('circle',40*10**-3)
    

    # Crear subplots
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Esfuerzo Cortante Flexión", "Esfuerzo Cortante Flexión", "Esfuerzo Esfuerzo Torsión", "Gráfica 4"))

    # Añadir superficies a los subplots
    fig1 = graph.graphFlexuralShearStress(results["maximoEsfuerzoCortanteX"], radius=profile.radius)
    fig2 = graph.graphFlexuralShearStress(results["maximoEsfuerzoCortanteY"], radius=profile.radius, direction=-1)
    fig3 = graph.graphTorsionalShearStress(results["maximoEsfuerzoCortanteTorsion"], radius=profile.radius)

    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)

    
    # Ajustar el tamaño de cada gráfica
    fig.update_layout(
        title='Esfuerzos Cortantes',
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

    # Crear el QWebEngineView y cargar el archivo HTML
    
    # parent.load(QtCore.QUrl.fromLocalFile(html_file))
    return html_file

def plotMohr(results):
    # Extraer los valores necesarios de los resultados
    # sigma_x = results['sigma_x']
    # sigma_y = results['sigma_y']
    # sigma_z = results['sigma_z']
    # tau_xy = results['tau_xy']
    # tau_yz = results['tau_yz']
    # tau_zx = results['tau_zx']
    sigma_x = 100
    sigma_y = 50
    sigma_z = 30
    tau_xy = 25
    tau_yz = 15
    tau_zx = 10

    # Crear subplots
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'xy'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Círculo de Mohr 2D", "Círculo de Mohr 3D", "Círculo de Mohr 3D Esferas"))

    # Graficar Círculo de Mohr 2D
    fig1 = test.graficar_circulo_mohr(sigma_x, sigma_y, tau_xy)
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    # Graficar Círculo de Mohr 3D
    fig2 = test.graficar_circulo_mohr_3d(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

    # Graficar Círculo de Mohr 3D Esferas
    fig3 = test.graficar_circulo_mohr_3d_esferas(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)

    # Ajustar el tamaño de cada gráfica
    fig.update_layout(
        title='Círculo de Mohr',
        height=600,  # Altura total de la figura
        width=1800,  # Ancho total de la figura
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
        )
    )

    # Guardar la figura en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        fig.write_html(tmpfile.name)
        tmpfile.flush()
        tmpfile.seek(0)
        html_file = tmpfile.name

    return html_file   

if __name__ == '__main__':
    main()