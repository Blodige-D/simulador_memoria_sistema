class Nodo:
    def __init__(self,nombre=None,tamanioTotal=None,i=None):
        self.nombre = nombre
        self.tamanioTotal = tamanioTotal
        self.siguiente=None
        self.tamanioUtilizado=0
        self.tamanioRestante=0
        self.fila=i

    def getObjeto(self):
        return self.objeto

    def getSiguiente(self):
        return self.siguiente

    def getTamanio(self):
        return self.tamanio

    def setObjeto(self,objeto):
        self.objeto=objeto

    def setSiguiente(self,siguiente):
        self.siguiente=siguiente

    def setTamanio(self,tamanio):
        self.tamanio = tamanio
