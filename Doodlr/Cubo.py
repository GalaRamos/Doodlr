from enum import Enum
class Type(Enum):
     INT = 1
     FLOAT = 2
     BOOL = 3
     ERROR = -1

class Operation(Enum):
     PLUS = 1
     MINUS = 2
     MULTIPLY = 3
     DIVIDE = 4
     MODULE = 5
     GREATER = 6
     GREATEREQUAL = 7
     LESS = 8
     LESSEQUAL = 9
     ASIGN = 10
     EQUAL = 11
     NOTEQUAL = 12
     AND = 13
     OR = 14
     POW = 15

charToEnum = {
    "+" : Operation.PLUS,
    "-" : Operation.MINUS,
    "*" : Operation.MULTIPLY,
    "/" : Operation.DIVIDE,
    "%" : Operation.MODULE,
    ">" : Operation.GREATER,
    ">=" : Operation.GREATEREQUAL,
    "<" : Operation.LESS,
    "<=" : Operation.LESSEQUAL,
    "=" : Operation.ASIGN,
    "==" : Operation.EQUAL,
    "!=" : Operation.NOTEQUAL,
    "AND" : Operation.AND,
    "OR" : Operation.OR,
    "^" : Operation.POW,
    "INT" : Type.INT,
    "FLOAT" : Type.FLOAT,
    "BOOL" : Type.BOOL,
    "err" : Type.ERROR
}

def getCubeType(typ1,typ2,act):
    return cubo[charToEnum[typ1]][charToEnum[typ2]][charToEnum[act]]

cubo = {
# int operacion tipo
    Type.INT: {
    #int operacion int
      Type.INT: {
        Operation.PLUS:"INT",
        Operation.MINUS:"INT",
        Operation.MULTIPLY:"INT",
        Operation.DIVIDE:"INT",
        Operation.MODULE: "INT",
        Operation.GREATER:"BOOL",
        Operation.GREATEREQUAL:"BOOL",
        Operation.LESSEQUAL:"BOOL",
        Operation.LESS:"BOOL",
        Operation.ASIGN:"INT",
        Operation.EQUAL:"BOOL",
        Operation.NOTEQUAL:"BOOL",
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:"INT"
        },
    #int operacion FLOAT
      Type.FLOAT: {
        Operation.PLUS:"FLOAT",
        Operation.MINUS:"FLOAT",
        Operation.MULTIPLY:"FLOAT",
        Operation.DIVIDE:"FLOAT",
        Operation.MODULE: "FLOAT",
        Operation.GREATER:"BOOL",
        Operation.GREATEREQUAL:"BOOL",
        Operation.LESSEQUAL:"BOOL",
        Operation.LESS:"BOOL",
        Operation.ASIGN:"INT",
        Operation.EQUAL:"BOOL",
        Operation.NOTEQUAL:"BOOL",
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:"FLOAT"
        },
    #int operacion BOOL
      Type.BOOL: {
        Operation.PLUS:Type.ERROR,
        Operation.MINUS:Type.ERROR,
        Operation.MULTIPLY:Type.ERROR,
        Operation.DIVIDE:Type.ERROR,
        Operation.MODULE:Type.ERROR,
        Operation.GREATER:Type.ERROR,
        Operation.GREATEREQUAL:Type.ERROR,
        Operation.LESSEQUAL:Type.ERROR,
        Operation.LESS:Type.ERROR,
        Operation.ASIGN:Type.ERROR,
        Operation.EQUAL:Type.ERROR,
        Operation.NOTEQUAL:Type.ERROR,
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:Type.ERROR
        },
      },
#FLOAT operacion tipo
    Type.FLOAT:{
    #FLOAT operacion int
      Type.INT: {
        Operation.PLUS:"FLOAT",
        Operation.MINUS:"FLOAT",
        Operation.MULTIPLY:"FLOAT",
        Operation.DIVIDE:"FLOAT",
        Operation.MODULE: "INT",
        Operation.GREATER:"BOOL",
        Operation.GREATEREQUAL:"BOOL",
        Operation.LESSEQUAL:"BOOL",
        Operation.LESS:"BOOL",
        Operation.ASIGN:"FLOAT",
        Operation.EQUAL: "BOOL",
        Operation.NOTEQUAL:"BOOL",
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:"FLOAT"
        },
    #FLOAT operacion FLOAT
      Type.FLOAT: {
        Operation.PLUS:"FLOAT",
        Operation.MINUS:"FLOAT",
        Operation.MULTIPLY:"FLOAT",
        Operation.DIVIDE:"FLOAT",
        Operation.MODULE: "INT",
        Operation.GREATER:"BOOL",
        Operation.GREATEREQUAL:"BOOL",
        Operation.LESSEQUAL:"BOOL",
        Operation.LESS:"BOOL",
        Operation.ASIGN:"FLOAT",
        Operation.EQUAL: "BOOL",
        Operation.NOTEQUAL:"BOOL",
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:'FLOAT'
        },
    #FLOAT operacion BOOL
      Type.BOOL: {
        Operation.PLUS:Type.ERROR,
        Operation.MINUS:Type.ERROR,
        Operation.MULTIPLY:Type.ERROR,
        Operation.DIVIDE:Type.ERROR,
        Operation.MODULE:Type.ERROR,
        Operation.GREATER:Type.ERROR,
        Operation.GREATEREQUAL:Type.ERROR,
        Operation.LESSEQUAL:Type.ERROR,
        Operation.LESS:Type.ERROR,
        Operation.ASIGN:Type.ERROR,
        Operation.EQUAL:Type.ERROR,
        Operation.NOTEQUAL:Type.ERROR,
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:Type.ERROR
        },
      },
#BOOL operacion tipo
    Type.BOOL:{
    #BOOL operacion int
      Type.INT: {
        Operation.PLUS:Type.ERROR,
        Operation.MINUS:Type.ERROR,
        Operation.MULTIPLY:Type.ERROR,
        Operation.DIVIDE:Type.ERROR,
        Operation.MODULE:Type.ERROR,
        Operation.GREATER:Type.ERROR,
        Operation.GREATEREQUAL:Type.ERROR,
        Operation.LESSEQUAL:Type.ERROR,
        Operation.LESS:Type.ERROR,
        Operation.ASIGN:Type.ERROR,
        Operation.EQUAL:Type.ERROR,
        Operation.NOTEQUAL:Type.ERROR,
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:Type.ERROR
        },
    #BOOL operacion FLOAT
      Type.FLOAT: {
        Operation.PLUS:Type.ERROR,
        Operation.MINUS:Type.ERROR,
        Operation.MULTIPLY:Type.ERROR,
        Operation.DIVIDE:Type.ERROR,
        Operation.MODULE:Type.ERROR,
        Operation.GREATER:Type.ERROR,
        Operation.GREATEREQUAL:Type.ERROR,
        Operation.LESSEQUAL:Type.ERROR,
        Operation.LESS:Type.ERROR,
        Operation.ASIGN:Type.ERROR,
        Operation.EQUAL:Type.ERROR,
        Operation.NOTEQUAL:Type.ERROR,
        Operation.AND:Type.ERROR,
        Operation.OR:Type.ERROR,
        Operation.POW:Type.ERROR
        },
    #BOOL operacion BOOL
      Type.BOOL: {
        Operation.PLUS:Type.ERROR,
        Operation.MINUS:Type.ERROR,
        Operation.MULTIPLY:Type.ERROR,
        Operation.DIVIDE:Type.ERROR,
        Operation.MODULE:Type.ERROR,
        Operation.GREATER:Type.ERROR,
        Operation.GREATEREQUAL:Type.ERROR,
        Operation.LESSEQUAL:Type.ERROR,
        Operation.LESS:Type.ERROR,
        Operation.ASIGN:"BOOL",
        Operation.EQUAL:"BOOL",
        Operation.NOTEQUAL:"BOOL",
        Operation.AND:"BOOL",
        Operation.OR:"BOOL",
        Operation.POW:Type.ERROR
        },
      },
}