import sys

tablaConst = dict()

VALOR = "valor"
TIPO = "tipo"

#clase que guarda todas las funciones con su tipo, id, direccion
class directorioFunciones:
    funciones = []
    def __init__(self):
        self.funciones = []

    def __str__(self):
        return self.funciones

class EstrucFunc:
    def __init__(self, id, type, dir):
        self.id = id
        self.type = type
        self.dir = dir
        self.globDir = None
        self.varTable = []

    def __str__(self):
        valores = str(self.id)
        valores += " " + str(self.type)
        valores += " " + str(self.dir)
        return valores

class Var:
    def __init__(self,id,type,dir,dim):
        self.id = id
        self.type = type
        self.dir = dir
        self.dim = []

    def __str__(self):
        valores = str(self.id)
        valores += " " + str(self.type)
        valores += " " + str(self.dir)
        return valores

def add_const(direc, value, type):
    if direc not in tablaConst:
        tablaConst[direc]=dict()

        tablaConst[direc][VALOR] = value
        tablaConst[direc][TIPO] = type

    else:
        print("Ya existe la constante")
