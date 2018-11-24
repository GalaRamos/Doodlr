import ply.lex as lex
import re
import codecs
import os
import sys

# Lista de las palabras reservadas del lenguaje
reservedWords = {
	  'FUNCION' : 'PR_function',
	  'GLOBAL' : 'PR_global',
	  'RETURN' : 'PR_return',
	  'MAIN' : 'PR_main',


	  'IF' : 'PR_if' ,
	  'ELSE' : 'PR_else',
	  'WHILE' : 'PR_While',
	  'TRUE' : 'PR_true',
	  'FALSE' : 'PR_false',

	  'INT' : 'PR_int',
	  'FLOAT' : 'PR_float',
	  'BOOL' : 'PR_bool',
	  'VOID' : 'PR_void',
	  'AND' : 'PR_and',
	  'OR' : 'PR_or',
	  'WRITE' : 'PR_write',
	  'READ' : 'PR_read',

	  'CIRCULO' : 'PR_circulo',
	  'RECTANGULO' : 'PR_rectangulo',
	  'ESPIRAL' : 'PR_espiral',
	  'ESTRELLA' : 'PR_estrella',
}

#Tokens validos
tokens = ['OP_ADD','OP_SUBS','OP_MULT','OP_DIV', 'OP_MOD', 'OP_POW',
			'OP_EQUALTO','OP_EQUALS','OP_DIFF',
			'OP_LESST','OP_LESSTEQ','OP_GREATT','OP_GREATTEQ',
			'TO_PAROP','TO_PARCLO','TO_BRACKOP','TO_BRACKCLO','TO_CBRACKOP','TO_CBRACKCLO',
			'TO_INT','TO_FLOAT','ID','TO_COMA','TO_PuntoComa']

#Operaciones validas de los tokens
t_ignore = ' \t\n'
t_OP_ADD = r'\+'
t_OP_SUBS = r'\-'
t_OP_MULT = r'\*'
t_OP_DIV = r'\/'
t_OP_MOD = r'\%'
t_OP_POW = r'\^'
t_OP_EQUALTO = r'\=\='
t_OP_EQUALS = r'\='
t_OP_DIFF = r'\!\='
t_OP_LESST = r'\<'
t_OP_LESSTEQ = r'\<\='
t_OP_GREATT = r'\>'
t_OP_GREATTEQ = r'\>\='
t_TO_PAROP = r'\('
t_TO_PARCLO = r'\)'
t_TO_BRACKOP = r'\{'
t_TO_BRACKCLO = r'\}'
t_TO_CBRACKOP = r'\['
t_TO_CBRACKCLO = r'\]'
t_TO_INT = r'[0-9]+'
t_TO_FLOAT = r'[0-9]+\.[0-9]+'
t_TO_COMA = r'\,'
t_TO_PuntoComa = r'\;'

tokens = tokens + list(reservedWords.values())

#Nombres de IDs
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reservedWords.get(t.value,'ID')
    return t

# Funcion para checar la sintaxis del lenguaje
def t_error(t):
    global aprobado
    aprobado = False
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)
# Construye el lexer
lex.lex()
