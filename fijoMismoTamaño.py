import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QPushButton, QLabel, QGroupBox,
                            QVBoxLayout, QHBoxLayout,QTableWidget, QTableWidgetItem,
                            QAbstractItemView, QGridLayout, QComboBox, QFrame, QLineEdit
                            )

from Lista import Lista

class MemoriaFija(QMainWindow):
    def __init__(self,sql=None):
        QMainWindow.__init__(self)
        QMainWindow.setWindowFlags(self,Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowIcon(QIcon(""))
        self.setWindowTitle("Simulador de memoria")
        self.resize(400,350)
        self.lista = Lista()
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.setStyleSheet("QGroupBox {background:rgba(245, 246, 250,.95)}")

        pixmap = QPixmap("")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 400, 370))
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

    #    self.showTable()
        self.groupMainWindow()

        self.seleccionarDivisionDeMemoria.currentIndexChanged.connect(self.crearParticiones)
        self.ptCargar.clicked.connect(self.agregarProceso)
        self.ptLiberar.clicked.connect(self.liberarProceso)
        self.seleccionarDivisionDeMemoriaLC.currentTextChanged.connect(self.prueba2)

    def prueba2(self):
        if self.seleccionarDivisionDeMemoriaLC.currentText() == "Crear proceso":
            self.ptLiberar.setEnabled(False)
            self.ptCargar.setEnabled(True)
            self.lineEdit1.setEnabled(True)
            self.lineEdit2.setEnabled(True)

        elif self.seleccionarDivisionDeMemoriaLC.currentText() == "Liberar proceso":
            self.ptLiberar.setEnabled(True)
            self.ptCargar.setEnabled(False)
            self.lineEdit1.setEnabled(True)
            self.lineEdit2.setEnabled(False)

    def agregarProceso(self):
        if self.seleccionarDivisionDeMemoria.currentText != "Seleccione particiones":
            nombre = self.lineEdit1.text()
            try:
                tamanio = int(self.lineEdit2.text())
            except Exception as e:
                print("campo vacio")
                tamanio = ""
                
            # tamanio = int(self.lineEdit2.text())
            if nombre != "" and tamanio != "":
                self.lista.cargarProcesoMismoTamanioFijo(nombre,tamanio)
                nodo = self.lista.buscar(nombre)
                try:
                    print(nodo)
                    print("Fila: %s"%nodo.fila)
                    print("Nombre: %s"%nodo.nombre)
                    # self.tablaBitacora.setItem(nodo.fila, 0, QTableWidgetItem("%s MU:%s\nML:%s"%(nodo.nombre,nodo.tamanioUtilizado,nodo.tamanioRestante)))
                    self.tablaBitacora.item(nodo.fila,0).setText("%s MU:%s\nML:%d"%(nodo.nombre,nodo.tamanioUtilizado,nodo.tamanioRestante))
                    self.lista.listar()
                except Exception as e:
                    print(e)


    def liberarProceso(self):
        nombre = self.lineEdit1.text()
        if nombre != "":
            nodo = self.lista.buscar(nombre)
            try:
                self.lista.liberarProcesosMismoTamanioFijo(nombre)
                self.tablaBitacora.item(nodo.fila,0).setText("%s MU:%s\nML:%d"%(nodo.nombre,nodo.tamanioUtilizado,nodo.tamanioRestante))
                self.lista.listar()
            except Exception as e:
                print(e)


    def crearParticiones(self):
        #llamar al metodo agregarProcesoFijoMismoTamnio
        self.lista = Lista()
        # print(self.seleccionarDivisionDeMemoria.currentText())
        self.tablaBitacora.clearContents()
        particiones=int(self.seleccionarDivisionDeMemoria.currentText())
        self.lista.hacerParticionesMismoTamanioFijo(particiones)
        self.tablaBitacora.setRowCount(particiones)
        for h in range(0,self.tablaBitacora.rowCount()):
            if self.tablaBitacora.rowCount() == 8:
                self.tablaBitacora.setRowHeight(h,36)
            elif self.tablaBitacora.rowCount() == 7:
                self.tablaBitacora.setRowHeight(h,42)
            elif self.tablaBitacora.rowCount() == 4:
                self.tablaBitacora.setRowHeight(h,73)
            elif self.tablaBitacora.rowCount() == 2:
                self.tablaBitacora.setRowHeight(h,145)
            elif self.tablaBitacora.rowCount() == 1:
                self.tablaBitacora.setRowHeight(h,300)

            self.tablaBitacora.setItem(h, 0, QTableWidgetItem("%d MB"%(569/particiones)))
            self.tablaBitacora.item(h,0).setTextAlignment(Qt.AlignCenter)
            # self.tablaBitacora.item(0,0).setText("Hola")

        self.lista.listar()
    

    def groupMainWindow(self):
        self.groupControl = QGroupBox()

        self.etiqueta1 = QLabel("FIJO IGUAL TAMAÑO")
        self.etiqueta22 = QLabel("Crear/Liberar")
        self.seleccionarDivisionDeMemoriaLC = QComboBox()
        # self.seleccionarDivisionDeMemoriaLC.addItem("")
        self.seleccionarDivisionDeMemoriaLC.addItem("Crear proceso")
        self.seleccionarDivisionDeMemoriaLC.addItem("Liberar proceso")

        h11 = QHBoxLayout()
        h11.addWidget(self.etiqueta22)
        h11.addWidget(self.seleccionarDivisionDeMemoriaLC)

        self.etiqueta2 = QLabel("Particiones")
        self.seleccionarDivisionDeMemoria = QComboBox()
        self.seleccionarDivisionDeMemoria.addItem("Seleccione particiones")
        self.seleccionarDivisionDeMemoria.addItem("1")
        self.seleccionarDivisionDeMemoria.addItem("2")
        self.seleccionarDivisionDeMemoria.addItem("4")
        self.seleccionarDivisionDeMemoria.addItem("7")
        self.seleccionarDivisionDeMemoria.addItem("8")
        h1 = QHBoxLayout()
        h1.addWidget(self.etiqueta2)
        h1.addWidget(self.seleccionarDivisionDeMemoria)

        self.etiqueta3 = QLabel("Nombre")
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setPlaceholderText("Nombre del proceso")
        h2 = QHBoxLayout()
        h2.addWidget(self.etiqueta3)
        h2.addWidget(self.lineEdit1)
        
        self.btRegresar = QPushButton("Regresar",self.groupControl)
        self.btRegresar.setGeometry(QRect(5,310,90,25))

        self.etiqueta4 = QLabel("Tamaño")
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setPlaceholderText("Cantidad de espacio en MB")
        h3 = QHBoxLayout()
        h3.addWidget(self.etiqueta4)
        h3.addWidget(self.lineEdit2)

        self.ptCargar = QPushButton("Crear")
        self.ptLiberar = QPushButton("Liberar")
        self.ptLiberar.setEnabled(False)
        h4 = QHBoxLayout()
        h4.addWidget(self.ptCargar)
        h4.addWidget(self.ptLiberar)

        v1 = QVBoxLayout()
        v1.addWidget(self.etiqueta1)
        v1.addLayout(h11)
        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addLayout(h3)
        v1.addLayout(h4)
        v1.addSpacing(170)
        self.groupControl.setLayout(v1)


        self.groupSimulator = QGroupBox()
        self.line=QFrame()            #marco hereda el espacio del QMainWindow
        # self.line.setGeometry(QRect(215,20,2,510))      #posicion y tamañp
        self.line.setFrameShape(QFrame.VLine)           #forma linea en este caso
        self.line.setFrameShadow(QFrame.Raised)         #sombra
        # self.line.setLineWiddth(2)                       #grosor



        self.tablaBitacora = QTableWidget()
        self.tablaBitacora.setColumnCount(1)    #Establecer numero de columna
        # self.tablaBitacora.setRowCount(2)       #Establecer numero de fila
        self.tablaBitacora.setMaximumWidth(100) #Establecer ancho maximo

        # self.tablaBitacora.setItem(0, 0, QTableWidgetItem("8 MB"))
        # self.tablaBitacora.item(0,0).setBackground(Qt.red)
        # self.tablaBitacora.item(0,0).setTextAlignment(Qt.AlignCenter)

        nombrecolumnas=("569M",)
        self.tablaBitacora.setHorizontalHeaderLabels(nombrecolumnas)#nombre de columna

        self.tablaBitacora.setAutoScroll(True)
        self.tablaBitacora.setAlternatingRowColors(True)
        self.tablaBitacora.verticalHeader().setDefaultSectionSize(20)       #alturas celda
        self.tablaBitacora.setColumnWidth(0,100)                            #anchura celda
        self.tablaBitacora.setRowHeight(0,10)
        self.tablaBitacora.setRowHeight(1,50)
        self.tablaBitacora.setRowHeight(2,90)

      
        """
            for indice, ancho in enumerate((anchura1,anchura2,anchura3),start=0):
                self.tablaBitacora.setColumnWidth(indice,ancho)
        """

        self.tablaBitacora.setEditTriggers(QAbstractItemView.NoEditTriggers)#Desabilitar editar celdas
        # self.tablaBitacora.setSelectionMode(QAbstractItemView.SingleSelection)#Seleccionar una celda a la vez
        # self.tablaBitacora.setSelectionMode(QAbstractItemView.NoSelection)#Desabilita la selecion
        self.tablaBitacora.setDragDropOverwriteMode(False)
        self.tablaBitacora.setSortingEnabled(False)#desabilita el ordenamiento
        self.tablaBitacora.verticalHeader().setVisible(False)#ocultar header verticales

        v2  = QVBoxLayout()
        v2.addWidget(self.tablaBitacora)
        self.groupSimulator.setLayout(v2)

        self.grid = QGridLayout()
        self.grid.addWidget(self.groupControl,0,0,1,1)
        self.grid.addWidget(self.line,0,1,2,1)
        self.grid.addWidget(self.groupSimulator,0,2,1,4)

        self.centralwidget.setLayout(self.grid)




    def verificarCantidadDeFilas(self,tabla,datos):
        if len(datos) > tabla.rowCount():
            tabla.setRowCount(len(datos))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MemoriaFija()
    main.show()
    app.exec_()
