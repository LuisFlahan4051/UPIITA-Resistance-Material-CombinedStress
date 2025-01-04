from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QComboBox, QDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
import numpy as np
from plotly.subplots import make_subplots
import tempfile

from graph import graphStress, graphNormalStressOfMoment,graphNormalStress,graphTorsionalShearStress, graphFlexuralShearStress
import graph
from engine import format_eng
import engine

def main():
    run_app()
    
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
    
    dataTable = MainWindow.findChild(QtWidgets.QTableWidget, 'dataTable')
    dataTable.setColumnCount(8)  # Establecer el número de columnas
    dataTable.setHorizontalHeaderLabels(['x', 'y','z','Apoyo','Tipo Apoyo','fx','fy','fz'])
    
    outDataTable = MainWindow.findChild(QtWidgets.QTableWidget, 'outDataTable')
    outDataTable.setColumnCount(100)
    outDataTable.setRowCount(3)
    outDataTable.setVerticalHeaderLabels(['Esfuerzo Normal por Mx','Esfuerzo Normal por My','Esfuerzo Normal'])
    setResultValuesToTable(outDataTable, engine.engine())

    addLoadPoint = MainWindow.findChild(QtWidgets.QPushButton, 'addLoadPoint')
    addLoadPoint.clicked.connect(lambda: show_data_entry_dialog(MainWindow))

    add_row_with_checkbox(dataTable)
    
    graphLayout = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout1')
    web_view = QWebEngineView()
    graphLayout.addWidget(web_view)

    
    
    normalStress = MainWindow.findChild(QtWidgets.QRadioButton, 'normalStress')
    normalStress2D = MainWindow.findChild(QtWidgets.QRadioButton, 'normalStress2D')
    shearStress = MainWindow.findChild(QtWidgets.QRadioButton, 'shearStress')
    
    plot1 = plotNormalStress()
    plot2 = plotShearStress()
    plot3 = plotNormalStress2D(engine.engine())

    normalStress.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot1))))
    shearStress.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot2))))
    normalStress2D.toggled.connect(lambda: (
        web_view.load(QtCore.QUrl.fromLocalFile(plot3))))


    MainWindow.show()
    
    sys.exit(app.exec())

def show_data_entry_dialog(parent):
    loader = QtUiTools.QUiLoader()
    file = QtCore.QFile("./addPointForce.ui")
    file.open(QtCore.QFile.ReadOnly)
    dialog = loader.load(file, parent)
    file.close()

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
        outDataTable.setItem(0, i, QTableWidgetItem(f"{format_eng(eX[i])}"))
        outDataTable.setItem(1, i, QTableWidgetItem(f"{format_eng(eY[i])}"))
        outDataTable.setItem(2, i, QTableWidgetItem(f"{format_eng(eN[i])}"))
    

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

    fig3, fig2, fig1 =graph.graphStress(results)

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

def plotNormalStress():
    profile = engine.Profile('circle',40*10**-3)
    results = engine.engine()

    # Crear subplots
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Esfuerzo Normal", "Esfuerzo Por Flexión", "Esfuerzo Por Flexión", "Gráfica 4"))

    # Añadir superficies a los subplots
    fig1 = graphNormalStress(results, radius=profile.radius, density=10)
    fig3, fig2= graph.graphNormalStressOfMoment(results,radius=profile.radius)

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
    
def plotShearStress():
    profile = engine.Profile('circle',40*10**-3)
    results = engine.engine()

    # Crear subplots
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                        subplot_titles=("Esfuerzo Cortante Flexión", "Esfuerzo Cortante Flexión", "Esfuerzo Esfuerzo Torsión", "Gráfica 4"))

    # Añadir superficies a los subplots
    fig1 = graph.graphFlexuralShearStress(results, radius=profile.radius)
    fig2 = graph.graphFlexuralShearStress(results, radius=profile.radius, direction=-1)
    fig3 = graph.graphTorsionalShearStress(results, radius=profile.radius)

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
    

if __name__ == '__main__':
    main()