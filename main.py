from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QComboBox
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from graph import testGraphFunctions, graphStress, graphNormalStressOfMoment
from engine import engine, format_eng

def main():
    resultados = engine()
    
    graphNormalStressOfMoment(resultados)
    #testGraphFunctions()
    #graphStress(resultados)
    #run_app()
    
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
    setResultValues(outDataTable, engine())

    add_row_with_checkbox(dataTable)
    
    graphLayout = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout1')
    graphLayout2 = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout2')
    graphLayout3 = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout3')
    graphLayout4 = MainWindow.findChild(QtWidgets.QVBoxLayout, 'graphLayout4')

    
    create_3d_plot(graphLayout)
    create_cylinder_plot(graphLayout2)
    create_3d_plot(graphLayout3)
    create_3d_plot(graphLayout4)

    MainWindow.show()
    
    sys.exit(app.exec())

def setResultValues(outDataTable, resultados):
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



def create_3d_plot(parent):
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Datos para el plot
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))
    
    # Crear el plot
    ax.plot_surface(x, y, z, cmap='viridis')
    
    # Agregar título y títulos a los ejes
    ax.set_title('Superficie 3D')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

    
    Axes3D.mouse_init
    
    
    # Crear el canvas y agregarlo al layout del parent
    canvas = FigureCanvas(fig)
    canvas.draw()
    toolbar = NavigationToolBar(canvas)
    parent.addWidget(canvas)
    parent.addWidget(toolbar)
    
def create_cylinder_plot(parent):
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Datos para el cilindro
    z = np.linspace(0, 1, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = np.cos(theta)
    y = np.sin(theta)
    
    # Crear el plot del cilindro
    ax.plot_surface(x, y, z, cmap='viridis')

    # Crear las caras superior e inferior
    ax.plot_surface(x, y, np.zeros_like(z), color='b', alpha=0.5)  # Cara inferior
    ax.plot_surface(x, y, np.ones_like(z), color='b', alpha=0.5)   # Cara superior
    
    
    # Agregar título y títulos a los ejes
    ax.set_title('Cilindro Sólido')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    
    # Habilitar el control de zoom y rotación
    ax.mouse_init()
    
    # Crear el canvas y agregarlo al layout del parent
    canvas = FigureCanvas(fig)
    canvas.draw()
    toolbar = NavigationToolBar(canvas)
    parent.addWidget(canvas)
    parent.addWidget(toolbar)

if __name__ == '__main__':
    main()