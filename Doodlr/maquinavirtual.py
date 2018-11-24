from cuadruplos import *
from directorioFunciones import *
from memoriavirtual import *
import turtle
from turtle import  *

tur = turtle.Turtle(shape="turtle")

class parametro():
    value = None
    type = None

    def __init__(self,value,type):
        self.value = value
        self.type = type

    def __str__(self):
        return "{}: {}".format(self.type, self.value)

class maquinavirtual():
    def __init__(self, funciones, cuadruplos):
        self.cuadruplos = cuadruplos
        self.funciones = funciones

        self.cuadruploActual = 0
        self.regresaCuadruplo = []
        self.regresaDireccion = []

        self.memVirtual = memoriaVirtual()

        for i in range(0,len(self.funciones.funciones)):
            self.memVirtual.colocarValores(self.funciones.funciones[i])
        self.memoria = self.memVirtual
        self.parametros = []

    def goto(self,cuadruplos):
        self.cuadruploActual = cuadruplos.var3-1

    def gotoF(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        if not var1:
            self.cuadruploActual = cuadruplos.var3-1

    def goSub(self,cuadruplos):
        begin = cuadruplos.var1
        self.regresaCuadruplo.append(self.cuadruploActual)
        self.run(begin,'EndProc')
        print(str(self.cuadruploActual) + "      EndProc	None	None	None")
        self.cuadruploActual = self.regresaCuadruplo.pop()

    def param(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        tipo = memoria.sacarType(cuadruplos.var1)
        param = parametro(valor,tipo)
        self.parametros.append(param)

    def paramFill(self,cuadruplos,memoria):
        dirVal = cuadruplos.var1
        for parametro in self.parametros:
            memoria.meterValor(var2,parametro.va)

    def ret(self,cuadruplos,memoria):
        value = memoria.obtenerValor(cuadruplos.var1)
        dir = self.regresaDireccion.pop()
        memoria.meterValor(value,dir)

    def verifica(self,cuadruplos,memoria):
        var1 = cuadruplos.var1
        var2 = cuadruplos.var2
        value = memoria.obtenerValor(cuadruplos.var3)
        value = memoria.fixType(cuadruplos.var3, value)
        if not value<var1 and value>var2:
            print('No cabe')

    def era(self, cuadruplos):
        self.regresaDireccion.append(cuadruplos.var1)

    def ARRDef(self,cuadruplos,memoria):
        var1 = cuadruplos.var1
        var1 = var1+1
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        value = var1+var2
        memoria.meterValor(value,cuadruplos.var3)
        memoria.meterValor(var2,value)

    def opDivision(self,cuadruplos,memoria):
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        if(var2 == 0):
            print('division entre 0')
        else:
            var1 = memoria.obtenerValor(cuadruplos.var1)
            var1 = memoria.fixType(cuadruplos.var1,var1)
            var3 = cuadruplos.var3
            valor = var1 / var2
            memoria.meterValor(valor,var3)

    def opDivMod(self,cuadruplos,memoria):
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        if(var2 == 0):
            print('division entre 0')
        else:
            var1 = memoria.obtenerValor(cuadruplos.var1)
            var1 = memoria.fixType(cuadruplos.var1,var1)
            var3 = cuadruplos.var3
            valor = var1 % var2
            memoria.meterValor(valor,var3)

    def opMatematica(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        #print("VAR 1 OP MAT " + str(var1))
        var2 = memoria.obtenerValor(cuadruplos.var2)
        #print("VAR 2 OP MAT " + str(var2))
        var3 = cuadruplos.var3
        #print("VAR 3 OP MAT " + str(var3))
        estatuto = cuadruplos.estatuto
        var1 = memoria.fixType(cuadruplos.var1, var1)
        #print("VAR 1 OP MAT FIXED " + str(var1))
        var2 = memoria.fixType(cuadruplos.var2, var2)
        #print("VAR 2 OP MAT FIXED " + str(var2))

        if estatuto == '+':
            valor = var1 + var2

        elif estatuto == '-':
            valor = var1 - var2

        elif estatuto == '*':
            valor = var1 * var2
        #print("RESULTADO DE LA OP MAT: " +str(valor))
        memoria.meterValor(valor,var3)

    def opComparacion(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var3 = cuadruplos.var3
        estatuto = cuadruplos.estatuto
        var1 = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.fixType(cuadruplos.var2, var2)

        if estatuto == '>':
            valor = var1 > var2

        elif estatuto == '>=':
            valor = var1 >= var2

        elif estatuto == '<':
            valor = var1 < var2

        elif estatuto == '<=':
            valor = var1 <= var2

        elif estatuto == '!=':
            valor = var1 != var2

        elif estatuto == '==':
            valor = var1 == var2

        elif estatuto == '%':
            valor = var1 / var2
        #print("RESULTADO DE LA COMPARACION: " +str(valor))
        memoria.meterValor(valor,var3)

    def signoIgual(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        #print('valor signo igual ' + str(valor))
        memoria.meterValor(valor, cuadruplos.var3)

    def despliega(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        print("           ''' RESPUESTA: " + str(valor) + " '''")

    def dibujaCirculo(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vRadio = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vWidth = memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, var3)
        if vColor == 1:
            tur.color("red")
        if vColor == 2:
            tur.color("purple")
        if vColor == 3:
            tur.color("blue")
        if vColor == 4:
            tur.color("yellow")
        if vColor == 5:
            tur.color("orange")

        tur.width(vWidth)
        tur.penup()
        tur.goto(10,10)
        tur.pendown()
        tur.begin_fill()
        tur.circle(vRadio)
        tur.end_fill()
        turtle.done()

    def dibujaRectangulo(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vLargo = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vAlto = memoria.fixType(cuadruplos.var2, var2)
        varp3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, varp3)

        if vColor == 1:
            tur.color("black","red")
        if vColor == 2:
            tur.color("black","purple")
        if vColor == 3:
            tur.color("black","blue")
        if vColor == 4:
            tur.color("black","yellow")
        if vColor == 5:
            tur.color("black","orange")

        tur.penup()
        tur.goto(10,10)
        tur.pendown()
        tur.begin_fill()
        tur.forward(vLargo)
        tur.left(90)
        tur.forward(vAlto)
        tur.left(90)
        tur.forward(vLargo)
        tur.left(90)
        tur.forward(vAlto)
        tur.end_fill()
        turtle.done()

    def dibujaEspiral(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vRango = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vAngulo = memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, var3)

        colors = ['red', 'purple', 'blue', 'green', 'yellow', 'orange']

        tur.speed('fastest')
        if vColor == 1:
            tur.color("red")
        if vColor == 2:
            tur.color("purple")
        if vColor == 3:
            tur.color("blue")
        tur.penup()
        tur.pendown()
        for i in range(vRango): # this "for" loop will repeat these functions n times
            if vColor == 10:
                tur.pencolor(colors[i%6])
            tur.forward(i)
            tur.left(vAngulo)
        turtle.done()

    def dibujaEstrella(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vVertices = memoria.fixType(cuadruplos.var1-1, var1)
        print("VERTICES " + str(vVertices))
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vStep= memoria.fixType(cuadruplos.var2-1, var2)
        print("STEPS " + str(vStep))
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColors = memoria.fixType(cuadruplos.var3, var3)
        print("COLORES ESTRELLA " + str(vColors))

        colors = ['red', 'purple', 'blue', 'green', 'yellow', 'orange']

        tur.speed('fastest')
        tur.penup()
        tur.goto(10,10)
        tur.pendown()
        vVertices = int(vVertices)
        for i in range(vVertices): # this "for" loop will repeat these functions n times
            tur.pencolor(colors[i%5])
            tur.forward(100)
            tur.right(vStep*360.0/vVertices)
        turtle.done()

    def meterParametros(self,memoria):
        #print(" paramatros" + str(self.parametros.reverse()))
        self.parametros.reverse()
        contInt = 1
        contFloat = 1
        contBool = 1
        while self.parametros:
            var = self.parametros.pop()
            #print("paramatros: {}".format(var))
            valor = var.value
            tipo = var.type

            if tipo == 'INT':
                dir = 8500 + contInt
                contInt+=1
            elif tipo == 'FLOAT':
                dir = 9500 + contFloat
                contFloat+=1
            elif tipo == 'BOOL':
                dir = 10500 + contBool
                contBool+=1
            #print("meterParametros - valor: {} y dir: {}".format(valor, dir))
            memoria.meterValor(valor,dir)
            # memoria.meterValorParametros(valor,dir)
        #print("Memoria: \n{}".format(memoria))


    def run(self,begin,end):
        memoria = memoriaVirtual()
        memoria.mConstante = self.memVirtual.mConstante
        memoria.mGlobal = self.memVirtual.mGlobal

        for i in range(2,len(self.funciones.funciones)):
            memoria.colocarValores(self.funciones.funciones[i])
        self.meterParametros(memoria)
        self.cuadruploActual = begin

        while self.cuadruplos[self.cuadruploActual].estatuto != end:
            cuadruplo = self.cuadruplos[self.cuadruploActual]
            print(cuadruplo)
            accion = cuadruplo.estatuto

            if accion == 'Goto':
                self.goto(cuadruplo)

            elif accion == 'GotoF':
                self.gotoF(cuadruplo, memoria)

            elif accion == 'Era':
                self.era(cuadruplo)

            elif accion == 'Gosub':
                self.goSub(cuadruplo)

            elif accion == 'Param':
                self.param(cuadruplo,memoria)

            elif accion == 'ParamFill':
                self.paramFill(cuadrupLo, memoria)

            elif accion == 'Return':
                self.ret(cuadruplo,memoria)

            elif accion == 'Ver':
                self.verifica(cuadruplo, memoria)

            elif accion == '+ARR':
                self.ARRDef(cuadruplo, memoria)

            elif accion == 'Read':
                self.despliega(cuadruplo, memoria)

            elif accion == 'Write':
                self.despliega(cuadruplo, memoria)

            elif accion == '+' or accion == '-' or accion == '*':
                self.opMatematica(cuadruplo,memoria)

            elif accion == '/':
                self.opDivision(cuadruplo,memoria)

            elif accion == '%':
                self.opDivMod(cuadruplo,memoria)

            elif accion == 'AND' or accion == 'OR' or accion == '<' or accion == '<=' or accion == '>' or accion == '>=' or accion == '!=' or accion == '==':
                self.opComparacion(cuadruplo,memoria)

            elif accion == '=':
                self.signoIgual(cuadruplo, memoria)

            elif accion == 'Circulo':
                self.dibujaCirculo(cuadruplo,memoria)

            elif accion == 'Rectangulo':
                self.dibujaRectangulo(cuadruplo,memoria)

            elif accion == 'Espiral':
                self.dibujaEspiral(cuadruplo,memoria)

            elif accion == 'Estrella':
                self.dibujaEstrella(cuadruplo,memoria)

            elif accion == 'OVER':
                return 0

            else:
                print('ERROR, cuadruplo no acceptado: ')
                print(cuadruplo)

            self.cuadruploActual = self.cuadruploActual + 1
        self.memVirtual.mConst = memoria.mConstante
        self.memVirtual.mGlobal = memoria.mGlobal
