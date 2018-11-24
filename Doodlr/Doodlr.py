########################## IMPORTS ################################

import ply.lex as lex
import ply.yacc as yacc
import sys

import turtle

from lexer import *
from cuadruplos import *
from Cubo import *
from directorioFunciones import *
from maquinavirtual import *


########################## DECLARACION DE VARIABLES ################################

aprobado = True

#Pilas
pilaOpp = []
pilaVar  = []
pilacuadruplos =[]
pilaSaltos = []
funciones =[]
cuadruplos =[]

#VariabLe
temporalContador = 1
tipoDeVar = 0
scope = 1

#globales
gInt = 0
gFloat = 0
gBool = 0
parametrosNum = 0

#locales
lInt = 0
lFloat = 0
lBool = 0

#constantes
cInt = 0
cFloat = 0
cBool = 0

#temporales
tmpInt = 0
tmpFloat = 0
tmpBool = 0

tmpIntArr = 0
tmpFloatArr = 0
tmpBoolArr = 0

funciones.append(EstrucFunc("CONST","VOID",-1))
funciones[0].varTable.append(Var("-1","INT",17500,None))
#cInt += 1
funciones.append(EstrucFunc("GLOBAL","VOID",-1))

########################## REGLAS PARSER ################################


# Definicion de inicio de programa
def p_programa(p):
    ' programa : startQuad varGlobales cambiaScope declaraFunciones PR_main fillMainQuad TO_BRACKOP setMainFuncionValores mainBloque TO_BRACKCLO endPrograma'

#Crea el cuadruplo que dirige al MAIN
def p_startQuad(p):
    'startQuad :'
    pilaSaltos.append(len(cuadruplos))
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Goto', None, None, None))

#Llena el valor de la redireccion del Goto main
def p_fillMainQuad(p):
    'fillMainQuad :'
    salto = pilaSaltos.pop()
    cuadruplos[salto].var3 = len(cuadruplos)

#Crea el cuadrupLo de cierre del programa
def p_endPrograma(p):
    ' endPrograma : '
    cuadruplos.append(cuadruplo(len(cuadruplos), "OVER", None, None, None))

#El scope cambia, para así saber si trabajamos con variables globales o locales
def p_cambiaScope(p):
    ' cambiaScope : '
    global scope
    scope = 0

#Definicion de bloque de declaracion de variables globales
def p_varGlobales(p):
    ''' varGlobales : PR_global defVariables varGlobales
                    | empty'''

#Definicion de bloque de declaracion de variables Funciones
def p_declaraFunciones(p):
    ''' declaraFunciones : PR_function defFuncion declaraFunciones
                         | empty'''

def p_defFuncion(p):
    ''' defFuncion : decTipo ID agregaFuncion TO_PAROP decParametros TO_PARCLO TO_BRACKOP mainBloque TO_BRACKCLO endProcCuad'''

def p_agregaFuncion(p):
    ''' agregaFuncion : '''
    funciones.append(EstrucFunc(p[-1], p[-2], len(cuadruplos)))
    #Obtiene Direccion para el tipo de func
    global gInt , gFloat , gBool , lInt , lFloat , lBool
    global scope
    gInt = 0
    gFloat = 0
    gBool = 0
    lInt = 0
    lFloat = 0
    lBool = 0
    dire = setDireccionMem(p[-2],0,0,0,0,0,0)
    funciones[1].varTable.append(Var(p[-1], p[-2], dire, None))
    funciones[len(funciones)-1].globDir = dire
    scope = len(funciones) -1

def p_endProcCuad(p):
    ''' endProcCuad : '''

    cuadruplos.append(cuadruplo(len(cuadruplos), "EndProc", None, None , None))


def p_decParametros(p):
    ''' decParametros : decTipo ID meteVariable
               | decTipo ID meteVariable TO_COMA decParametros '''

#Definicion de un bloque de codigo basico
def p_mainBloque(p):
    ''' mainBloque : funcCiclos mainBloque
            | funcCondicionales mainBloque
            | defVariables mainBloque
            | llamadaDeFunciones mainBloque
            | funcIgual mainBloque
            | funcWrite mainBloque
            | funcRead mainBloque
            | funcReturn mainBloque
            | empty '''


def p_setMainFuncionValores(p):
    ' setMainFuncionValores : '
    global gInt , gFloat , gBool , lInt , lFloat , lBool
    gInt = 0
    gFloat = 0
    gBool = 0
    lInt = 0
    lFloat = 0
    lBool = 0

# Define Write
def p_funcWrite(p):
    ' funcWrite : PR_write TO_PAROP ID agregaWriteCuad TO_PARCLO TO_PuntoComa'

# Define Read
def p_funcRead(p):
    ' funcRead : PR_read TO_PAROP ID agregaReadCuad TO_PARCLO TO_PuntoComa'

# Define Return
def p_funcReturn(p):
    ' funcReturn : PR_return TO_PAROP ID agregaReturnCuad TO_PARCLO TO_PuntoComa'

# Definicion de asignacion
def p_funcIgual(p):
    ''' funcIgual : ID pushPilaVar OP_EQUALS pushPilaOp defExpresiones TO_PuntoComa extraNeed agregaIgualCuad
                  | ID TO_CBRACKOP defExpresiones TO_CBRACKCLO OP_EQUALS defExpresiones cuadruploAsignaArr TO_PuntoComa agregaIgualCuad '''

def p_extraNeed(p):
    ' extraNeed : empty '

# Definicion de ciclos WHILE
def p_funcCiclos(p):
    ' funcCiclos :  PR_While whileCuadP1 TO_PAROP defExpresiones TO_PARCLO whileCuadP2 TO_BRACKOP mainBloque TO_BRACKCLO whileCuadP3'


# Definicion de condicional if
def p_funcCondicionales (p):
    ' funcCondicionales : PR_if TO_PAROP defExpresiones TO_PARCLO agregaIfCuadP1 TO_BRACKOP mainBloque TO_BRACKCLO else agregaIfCuadP3'

# Definicion de condicional else
def p_else (p):
    ''' else : agregaIfCuadP2 PR_else TO_BRACKOP mainBloque TO_BRACKCLO
             | empty '''

#Declaracion de Variables , Arreglos

def p_decTipo(p):
    ''' decTipo : PR_int tipoVar
                | PR_float tipoVar
                | PR_bool tipoVar
                | PR_void tipoVar'''
    p[0] = p[1]

def p_defVariables (p):
    ''' defVariables : PR_int tipoVar defVar1 TO_PuntoComa
                     | PR_float tipoVar defVar1 TO_PuntoComa
                     | PR_bool tipoVar defVar1 TO_PuntoComa
                     | PR_void tipoVar defVar1 TO_PuntoComa '''

def p_defVar1 (p):
    ''' defVar1 : variable defVar2
                | arreglo defVar2 '''

def p_defVar2 (p):
    ''' defVar2 : TO_COMA defVar1
                | empty '''

#Declaracion de variables
def p_variable(p):
    ' variable : ID meteVariable '

###############################

#Declaracion de arreglos
def p_arreglo(p):
   ' arreglo : ID TO_CBRACKOP TO_INT TO_CBRACKCLO escribeArr'

def p_escribeArr(p):
   'escribeArr : empty'
   global scope

   ID = p[-4]
   localVars = list(map(lambda x: x.id ,funciones[scope].varTable))
   globalVars = list(map(lambda x: x.id ,funciones[1].varTable))

   if ID in localVars or ID in globalVars:
    print(str(ID)+' ya fue definida')

   else:
    global tipoDeVar
    newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)
    funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,p[-2]))

    for i in range(0,int(p[-2])):
        ID = p[-4] + '[' + str(i) + ']'
        newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)
        funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,p[-2]))
##################################################


# meter tipo de var
def p_tipoVar(p):
    ' tipoVar : empty '
    global tipoDeVar
    tipoDeVar = p[-1]

# Guarda Variable y le asigna direccion
def p_meteVariable(p):
    ' meteVariable : empty '
    global scope
    ID = p[-1]

    localVars = list(map(lambda x: x.id, funciones[scope].varTable))
    globalVars = list(map(lambda x: x.id ,funciones[1].varTable))

    if ID in localVars or ID in globalVars:
        print(str(ID)+' ya fue definida')
    else:
        global tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool
        newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)
        funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,None))

# Define todas las expresiones
def p_defExpresiones(p):
    ''' defExpresiones : decExpresion
                       | decExpresion PR_and pushPilaOp defExpresiones agregaAndCuad
                       | decExpresion PR_or pushPilaOp defExpresiones agregaAndCuad '''
    p[0] = p[1]

# Declara una expresion individual
def p_decExpresion(p):
    ''' decExpresion : miniExp
        | miniExp OP_EQUALTO pushPilaOp miniExp agregaComparCuad
        | miniExp OP_DIFF pushPilaOp  miniExp agregaComparCuad
        | miniExp OP_LESST pushPilaOp  miniExp agregaComparCuad
        | miniExp OP_LESSTEQ pushPilaOp miniExp agregaComparCuad
        | miniExp OP_GREATT pushPilaOp  miniExp agregaComparCuad
        | miniExp OP_GREATTEQ pushPilaOp miniExp agregaComparCuad '''
    p[0] = p[1]

# Declara expresiones con sumas y restas
def p_miniExp(p):
    ''' miniExp : microExp
                | microExp OP_SUBS pushPilaOp miniExp agregaSumResCuad
                | microExp OP_ADD pushPilaOp miniExp  agregaSumResCuad '''
    p[0] = p[1]

# Declara expresiones con multiplicaciones y divisiones
def p_microExp (p):
    ''' microExp : micromicroExp
                 | micromicroExp OP_MULT pushPilaOp microExp agregaMultDivCuad
                 | micromicroExp OP_DIV pushPilaOp microExp agregaMultDivCuad
                 | micromicroExp OP_MOD pushPilaOp microExp agregaMultDivCuad '''
    p[0] = p[1]

def p_micromicroExp(p):
    ''' micromicroExp : decSolucion
                      | decSolucion OP_POW pushPilaOp micromicroExp agregaPowCuad '''
    p[0] = p[1]

def p_decSolucion(p):
    ''' decSolucion : ID pushPilaVar
                    | ID TO_CBRACKOP defExpresiones TO_CBRACKCLO cuadArrPush
                    | TO_INT agregaIntCuad
                    | TO_FLOAT agregaFloatCuad
                    | PR_true agregaBoolCuad
                    | PR_false agregaBoolCuad
                    | llamadaDeFunciones
                    | TO_PAROP pushPilaOp defExpresiones TO_PARCLO pushPilaOp  '''
    p[0] = p[1]

# llamada de fuciones
def p_llamadaDeFunciones(p):
    ''' llamadaDeFunciones : ID eraCuadruplo TO_PAROP decParamFuncs TO_PARCLO TO_PuntoComa goSubCuadruplo
    					   | funcionesDibuja
                           | empty'''

def p_funcionesDibuja(p):
    ''' funcionesDibuja : PR_circulo  TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa circuloCuad
                        | PR_rectangulo TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa rectanguloCuad
                        | PR_espiral TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa espiralCuad
                        | PR_estrella TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa estrellaCuad'''

def p_decParamFuncs(p):
    ''' decParamFuncs : ID paramCuadruplo
                      | ID paramCuadruplo TO_COMA decParamFuncs
                      | empty '''

########################## PILAS ################################

# Agrega operadores a la pila de operadores
def p_pushPilaOp(p):
    ' pushPilaOp : empty '
    pilaOpp.append(p[-1]) #p[-1 ] quieredecir que se ira a la instrucion de atras menos 1 es decir se ira al operador


# Agrega Variables a la pila de Variables
def p_pushPilaVar(p):
    ' pushPilaVar : empty '
    pilaVar.append(p[-1])

########################## CUADRUPLOS TIPO VARIABLES ################################

def p_agregaIntCuad(p):
    ' agregaIntCuad : empty '
    #dirConst = getDirecConstantes('INT')
    #valor = p[-1]
    #type = 'INT'
    #add_const(dirConst, valor, type)
    pilaVar.append(p[-1])
    funciones[0].varTable.append(Var(p[-1], 'INT', getDirecConstantes('INT'), None))

def p_agregaFloatCuad(p):
    ' agregaFloatCuad : empty '
    #dirConst = getDirecConstantes('FLOAT')
    #valor = p[-1]
    #type = 'FLOAT'
    #add_const(dirConst, valor, type)
    pilaVar.append(p[-1])
    funciones[0].varTable.append(Var(p[-1], 'FLOAT', getDirecConstantes('FLOAT'), None))

def p_agregaBoolCuad(p):
    ' agregaBoolCuad : empty '
    dirConst = getDirecConstantes('BOOL')
    valor = p[-1]
    type = 'BOOL'
    add_const(dirConst, valor, type)
    pilaVar.append(p[-1])
    funciones[0].varTable.append(Var(p[-1], 'BOOL', getDirecConstantes('BOOL'), None))

########################## CUADRUPLOS ARREGLOS ################################

def p_CuadruploArrpush(p):
    "cuadArrPush : empty"
    # metemos en la lista de cuadruplos la verificacion de 0 a valor-1 o int(getDimensionVar(p[-4]))-1 y lo guardamos en un espacio de memoria
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Ver' ,0, int(getDimensionVar(p[-4]))-1 , getDireccionMem(p[-2])))
    print("EL DIM " + str(getDimensionVar(p[-4])) )

    global temporalContador
    numTemporal = "t" + str(temporalContador)
    pilaVar.append(numTemporal)
    temporalContador = temporalContador + 1

    #Definimos que la direccion temporal siempre será int, por lo que en la lista de funciones se mete el contador de
    # variable temporal, el tipo INT y la direccion
    dire = getDirecTempArr('INT')
    funciones[scope].varTable.append(Var(numTemporal, 'INT', dire,None))

    #Muestra la fila de cuadruplos, agregando el operador +ARR obteniendo la direccion de memoria del inicio del arreglo,
    # la direccion de la constante/var local/var global y la direccion temporal del arreglo
    cuadruplos.append(cuadruplo(len(cuadruplos), '+ARR' ,getDireccionMem(p[-4]), getDireccionMem(p[-2]) , getDireccionMem(numTemporal)))
    pilaVar.append(numTemporal)
    temporalContador = temporalContador + 1

########################## CUADRUPLOS COMPARACION ################################

def p_agregaAndCuad(p):
    ' agregaAndCuad : '
    if len(pilaOpp)> 0:
        global temporalContador
        if pilaOpp[len(pilaOpp)-1] == 'OR' or pilaOpp[len(pilaOpp)-1] == 'AND':
            operador = pilaOpp.pop()
            temporal = pilaVar.pop()
            numTemporal = "t" + str(temporalContador)
            dirTemporal = getDireccionMem(temporal)
            dirTipoTemp = getDirecTipoVar(temporal)
            temporal = pilaVar.pop()
            izq = getDireccionMem(temporal)
            dirTipoIzq = getDirecTipoVar(temporal)
            resultado = getCubeType(dirTipoIzq, dirTipoTemp, operador)
            if resultado == Type.ERROR:
                print("Error de sintaxis en comparaciones")
                sys.exit()
            dirResultado = getDirecTemporales(resultado)
            funciones[scope].varTable.append(Var(numTemporal, resultado, dirResultado, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, izq, dirTemporal, dirResultado))
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1

def p_agregaComparCuad(p):
    ' agregaComparCuad : '
    if len(pilaOpp)> 0:
        global temporalContador
        if pilaOpp[len(pilaOpp)-1] == '<' or pilaOpp[len(pilaOpp)-1] == '>'  or pilaOpp[len(pilaOpp)-1] == '<=' or pilaOpp[len(pilaOpp)-1] == '=>' or pilaOpp[len(pilaOpp)-1] == '==' or pilaOpp[len(pilaOpp)-1] == '!=':
            operador = pilaOpp.pop()
            temporal = pilaVar.pop()
            numTemporal = "t" + str(temporalContador)
            dirTemporal = getDireccionMem(temporal)
            dirTipoTemp = getDirecTipoVar(temporal)
            temporal = pilaVar.pop()
            izq = getDireccionMem(temporal)
            dirTipoIzq = getDirecTipoVar(temporal)
            resultado = getCubeType(dirTipoIzq, dirTipoTemp, operador)
            if resultado == Type.ERROR:
                print("Error de sintaxis en comparaciones")
                sys.exit()
            dirResultado = getDirecTemporales(resultado)
            funciones[scope].varTable.append(Var(numTemporal, resultado, dirResultado, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, izq, dirTemporal, dirResultado))
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1

########################## CUADRUPLOS ARITMETICOS ################################

def p_agregaSumResCuad(p):
    ' agregaSumResCuad : '
    if len(pilaOpp)> 0:
        global temporalContador
        if pilaOpp[len(pilaOpp)-1] == '+' or pilaOpp[len(pilaOpp)-1] == '-':
            operador = pilaOpp.pop()
            temporal = pilaVar.pop()
            numTemporal = "t" + str(temporalContador)
            dirTemporal = getDireccionMem(temporal)
            dirTipoTemp = getDirecTipoVar(temporal)
            temporal = pilaVar.pop()
            izq = getDireccionMem(temporal)
            dirTipoIzq = getDirecTipoVar(temporal)
            resultado = getCubeType(dirTipoIzq, dirTipoTemp, operador)
            if resultado == Type.ERROR:
                print("Error de sintaxis en comparaciones")
                sys.exit()
            dirResultado = getDirecTemporales(resultado)
            funciones[scope].varTable.append(Var(numTemporal, resultado, dirResultado, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, izq, dirTemporal, dirResultado))
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1

def p_agregaMultDivCuad(p):
    ' agregaMultDivCuad : '
    if len(pilaOpp)> 0:
        global temporalContador
        if pilaOpp[len(pilaOpp)-1] == '*' or pilaOpp[len(pilaOpp)-1] == '/' or pilaOpp[len(pilaOpp)-1] == '%':
            operador = pilaOpp.pop()
            temporal = pilaVar.pop()
            numTemporal = "t" + str(temporalContador)
            dirTemporal = getDireccionMem(temporal)
            dirTipoTemp = getDirecTipoVar(temporal)
            temporal = pilaVar.pop()
            izq = getDireccionMem(temporal)
            dirTipoIzq = getDirecTipoVar(temporal)
            resultado = getCubeType(dirTipoIzq, dirTipoTemp, operador)
            if resultado == Type.ERROR:
                print("Error de sintaxis en comparaciones")
                sys.exit()
            dirResultado = getDirecTemporales(resultado)
            funciones[scope].varTable.append(Var(numTemporal, resultado, dirResultado, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, izq, dirTemporal, dirResultado))
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1

def p_agregaPowCuad(p):
    ' agregaPowCuad : '
    if len(pilaOpp)> 0:
        global temporalContador
        if pilaOpp[len(pilaOpp)-1] == '^' :
            operador = pilaOpp.pop()
            temporal = pilaVar.pop()
            numTemporal = "t" + str(temporalContador)
            dirTemporal = getDireccionMem(temporal)
            dirTipoTemp = getDirecTipoVar(temporal)
            temporal = pilaVar.pop()
            izq = getDireccionMem(temporal)
            dirTipoIzq = getDirecTipoVar(temporal)
            resultado = getCubeType(dirTipoIzq, dirTipoTemp, operador)
            if resultado == Type.ERROR:
                print("Error de sintaxis en comparaciones")
                sys.exit()
            dirResultado = getDirecTemporales(resultado)
            funciones[scope].varTable.append(Var(numTemporal, resultado, dirResultado, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, izq, dirTemporal, dirResultado))
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1

########################## CUADRUPLOS ASIGNACION ################################

# Cuadruplo para asignaciones normales
def p_agregaIgualCuad(p):
    ' agregaIgualCuad : '
    ID = p[-7]
    if len(pilaOpp)> 0:
        if pilaOpp[len(pilaOpp)-1] == '=' :
            temporal = pilaVar.pop()
            dirVariable = getDireccionMem(temporal)
            dirTipo1 = getDirecTipoVar(temporal)
            asigna = getDireccionMem(ID)
            dirTipo2 = getDirecTipoVar(ID)
            operador = pilaOpp.pop()
            sintaxis = getCubeType(dirTipo1, dirTipo2, operador)
            if sintaxis == Type.ERROR:
                print ("Error de sintaxis")
                sys.exit()
            cuadruplos.append(cuadruplo(len(cuadruplos), operador, dirVariable, None , asigna))

# Cuadruplo para asignaciones de arreglos
def p_CuadruploAsignaARR(p):
    'cuadruploAsignaArr : empty'
    ID = p[-6]
    if len(pilaOpp)> 0:
        if pilaOpp[len(pilaOpp)-1] == '=' :
            temporal = pilaVar.pop()
            dirVariable = getDireccionMem(temporal)
            dirTipo1 = getDirecTipoVar(temporal)
            asigna = getDireccionMem(ID)
            dirTipo2 = getDirecTipoVar(ID)
            operador = pilaOpp.pop()
            sintaxis = getCubeType(dirTipo1, dirTipo2, operador)
            if sintaxis == Type.ERROR:
                print ("Error de sintaxis")
                sys.exit()
            cuadruplos.append(cuadruplo(len(cuadruplos), 'Ver', 0, int(getDimensionVar(p[-6]))-1, getDireccionMem(p[-5])))
            global temporalContador
            numTemporal = "t" + str(temporalContador)
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1
            dirArr = getDirecTempArr("INT")
            funciones[scope].varTable.append(Var(numTemporal, 'INT', dirArr, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), '+ARR' ,getDireccionMem(p[-7]), getDireccionMem(p[-5]), getDireccionMem(numTemporal)))
            cuadruplos.append(cuadruplo(len(cuadruplos), '=', dirVariable, None,  getDireccionMem(numTemporal)))

########################## CUADRUPLOS INSTRUCCIONES ################################

def p_agregaWriteCuad(p):
    ' agregaWriteCuad : '
    ID = p[-1]
    dirID = getDireccionMem(ID)
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Write',dirID, None , None))

def p_agregaReadCuad(p):
    ' agregaReadCuad : '
    ID = p[-1]
    dirID = getDireccionMem(ID)
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Read',dirID, None , None))

def p_agregaReturnCuad(p):
    ' agregaReturnCuad : '
    ID = p[-1]
    dirID = getDireccionMem(ID)
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Return',dirID, None , None))

########################## CUADRUPLOS CONDICIONALES Y CICLOS ################################

def p_agregaIfCuadP1(p):
    ' agregaIfCuadP1 : '
    pilaSaltos.append(len(cuadruplos))
    cuadruplos.append(cuadruplo(len(cuadruplos), "GotoF", getDireccionMem(pilaVar.pop()), None, None))

def p_agregaIfCuadP2(p):
    ' agregaIfCuadP2 : '
    idSaltos = pilaSaltos.pop()
    pilaSaltos.append(len(cuadruplos))
    cuadruplos.append(cuadruplo(len(cuadruplos), "Goto", None, None, None))
    cuadruplos[idSaltos].var3 = len(cuadruplos)

def p_agregaIfCuadP3(p):
    ' agregaIfCuadP3 : '
    idSaltos = pilaSaltos.pop()
    cuadruplos[idSaltos].var3 = len(cuadruplos)

# guardar indice de cuadruplo donde se empieza la condicion del while
def p_whileCuadP1(p):
    ' whileCuadP1 : '
    pilaSaltos.append(len(cuadruplos))

# guardar indice de cuadruplo del GotoF
def p_whileCuadP2(p):
    ' whileCuadP2 : '
    pilaSaltos.append(len(cuadruplos))
    cuadruplos.append(cuadruplo(len(cuadruplos), "GotoF", getDireccionMem(pilaVar.pop()), None, None))

def p_whileCuadP3(p):
    ' whileCuadP3 : '
    gotoFalseId = pilaSaltos.pop()
    beginId = pilaSaltos.pop()
    cuadruplos.append(cuadruplo(len(cuadruplos), "Goto", None, None, beginId))
    cuadruplos[gotoFalseId].var3 = len(cuadruplos)

########################## CUADRUPLOS FUNCIONES ################################

# obtiene parametros
def p_paramCuadruplo(p):
    ''' paramCuadruplo : '''
    ID = p[-1]
    global parametrosNum
    parametroVal = getDireccionMem(ID)
    paramActual = "param" + str(parametrosNum)
    parametrosNum += 1
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Param', parametroVal, None , paramActual))

def p_eraCuadruplo(p):
    ''' eraCuadruplo : '''
    global parametrosNum
    parametrosNum = 1
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Era',getFunctionById(p[-1]).dir , None , None))


def p_goSubCuadruplo(p):
    ''' goSubCuadruplo : '''
    ID = p[-6]
    global parametrosNum
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Gosub', getFunctionById(p[-6]).dir, None , None))
    parametrosNum = 1

########################## CUADRUPLOS FIGURAS ################################
def p_circuloCuad(p):
    ' circuloCuad : '
    radio = getDireccionMem(p[-7])
    width = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Circulo', radio, width, color))

def p_rectanguloCuad(p):
    ' rectanguloCuad : '
    largo = getDireccionMem(p[-7])
    alto = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Rectangulo', largo , alto , color))

def p_espiralCuad(p):
    ' espiralCuad : '
    rango = getDireccionMem(p[-7])
    angulo = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Espiral', rango , angulo , color))

def p_estrellaCuad(p):
    ' estrellaCuad : '
    vertices = getDireccionMem(p[-7])
    step = getDireccionMem(p[-5])
    #largo = getDireccionMem(p[-3])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Estrella', vertices, step, color))
    #cuadruplos.append(cuadruplo(len(cuadruplos), 'estrella2', color, None, None, None))

########################## FUNCIONES ################################

# FUNCIONES BUSQUEDA
def getFuncion(ID):
    funcionesAll = list(map(lambda x: x.id , funciones))
    idFuncion = funcionesAll.index(ID)
    if idFuncion >= 0:
        return funciones[idFuncion]

# FUNCS DIRECCIONES DE MEMORIA
def setDireccionMem(tipoVar, globalI, globalFloat , globalBool , localInt , localFloat , localBool):
    global scope, gInt , gFloat , gBool , lInt , lFloat , lBool
    global scope
    direcInicial =  0
    if (scope == 1):
        if (tipoVar == 'INT'):
            direcInicial = 5500 + globalI
            gInt = gInt +1
        elif (tipoVar == 'FLOAT'):
            direcInicial = 6500 + globalFloat
            gFloat = gFloat +1
        elif (tipoVar == 'BOOL'):
            direcInicial = 7500 + globalBool
            gBool= gBool +1
    else:
        if (tipoVar == 'INT'):
            direcInicial = 8500 + localInt
            lInt = lInt +1
        elif (tipoVar == 'FLOAT'):
            direcInicial = 9500+ localFloat
            localFloat = lFloat +1
        elif (tipoVar == 'BOOL'):
            direcInicial = 10500 + localBool
            lBool = lBool +1
    return direcInicial

def getDirecTemporales(tipoVar):
    direcTemporales = 0
    global tmpInt, tmpFloat, tmpBool
    if(tipoVar == 'INT'):
        direcTemporales = 11500 + tmpInt
        tmpInt += 1
    elif(tipoVar == 'FLOAT'):
        direcTemporales = 12500 + tmpFloat
        tmpFloat += 1
    elif(tipoVar == 'BOOL'):
        direcTemporales = 13500 + tmpBool
        tmpBool += 1
    return direcTemporales

def getDirecConstantes(tipoVar):
    direcConstantes = 0
    global cInt,cFloat,cBool
    if(tipoVar == 'INT'):
        direcConstantes = 14500 + cInt
        cInt += 1
    elif(tipoVar == 'FLOAT'):
        direcConstantes = 15500 + cFloat
        cFloat += 1
    elif(tipoVar == 'BOOL'):
        direcConstantes = 16500 + cBool
        cBool += 1
    return direcConstantes

def getDirecTempArr(varType):
    direcTempArr = 0
    global tmpIntArr,tmpFloatArr,tmpBoolArr
    if(varType == 'INT'):
        direcTempArr = 17500 + tmpIntArr
        tmpIntArr += 1
    elif(varType == 'FLOAT'):
        direcTempArr = 18500 + tmpFloatArr
        tmpFloatArr += 1
    elif(varType == 'BOOL'):
        direcTempArr = 19500 + tmpBoolArr
        tmpBoolArr += 1
    return direcTempArr

def getDireccionMem(ID):
    varLocales = list(map(lambda x: x.id ,funciones[scope].varTable))
    varGlobales = list(map(lambda x: x.id ,funciones[1].varTable))
    varConstant = list(map(lambda x: x.id ,funciones[0].varTable))
    if ID in varLocales:
        indiceID = varLocales.index(ID)
        return funciones[scope].varTable[indiceID].dir
    elif ID in varGlobales:
        indiceID  = varGlobales.index(ID)
        return funciones[1].varTable[indiceID].dir
    elif ID in varConstant:
        indiceID = varConstant.index(ID)
        return funciones[0].varTable[indiceID].dir
    return False

def getDirecTipoVar(ID):
    varLocales = list(map(lambda x: x.id ,funciones[scope].varTable))
    varGlobales = list(map(lambda x: x.id ,funciones[1].varTable))
    varConstant = list(map(lambda x: x.id ,funciones[0].varTable))
    if ID in varLocales:
        indiceID = varLocales.index(ID)
        return funciones[scope].varTable[indiceID].type
    elif ID in varGlobales:
        indiceID = varGlobales.index(ID)
        return funciones[1].varTable[indiceID].type
    elif ID in varConstant:
        indiceID = varConstant.index(ID)
        return funciones[0].varTable[indiceID].type
    return False

def getDimensionVar(ID):
    varLocales = list(map(lambda x: x.id ,funciones[scope].varTable))
    varGlobales = list(map(lambda x: x.id ,funciones[1].varTable))
    varConstant = list(map(lambda x: x.id ,funciones[0].varTable))
    if ID in varLocales:
        indiceID = varLocales.index(ID)
        return funciones[scope].varTable[indiceID].dim1
    elif ID in varGlobales:
        indiceID  = varGlobales.index(ID)
        return funciones[1].varTable[indiceID].dim1
    elif ID in varConstant:
        indiceID = varConstant.index(ID)
        return funciones[0].varTable[indiceID].dim1
    return False

def getFunctionById(ID):
    fNombres = list(map(lambda x: x.id , funciones))
    idx = fNombres.index(ID)
    if idx >= 0:
        return funciones[idx]

def GetFDir(ID):
  fNombres = list(map(lambda x: x.id , funciones))
  idx = fNombres.index(ID)
  if idx >= 0:
        return funciones[idx].dir

########################## EMPTY & ERROR ################################

def p_empty(p):
    ' empty : '

def p_error(p):
    global aprobado
    aprobado = False
    print("Error de sintaxis en '%s'" % p.value)
    sys.exit()

########################## PARSER READ ################################

parser = yacc.yacc()

archivo = sys.argv[1]
f = open(archivo, 'r')
s = f.read()
parser.parse(s)


func = directorioFunciones()
func.funciones = funciones

maquina = maquinavirtual(func, cuadruplos)
maquina.run(0, 'END')

if aprobado == True:
    #print("Archivo aprobado")
    #print ("\nCuadruplos:")
    #for i in range(0, len(cuadruplos)):
    #    print(str(cuadruplos[i]))
    sys.exit()
else:
    print("Archivo no aprobado")
    sys.exit()
