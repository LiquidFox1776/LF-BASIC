'''
Copyright 2018 LiquidFox1776 LiquidFox1776@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Python Version:    3.x
License:           MIT
'''

import ply.lex as command_lex

reserved_keywords = ['LIST', 'EXIT', 'RUN', 'ERASE','CLS', 'HELP', 'DEBUG', 'LOAD']

tokens = [
   'INT', # a whole number
   'FLOAT', # a number in the form of n.n where n is an int
   'PLUS', # + symbol
   'MINUS', # - symbol
   'TIMES', # * symbol
   'DIVIDE', # / symbol
   'CIRCUMFLEX', # ^ symbol
   'EQUALS', # = symbol
   'GT', # > symbol
   'LT', # < symbol
   'LPAREN', # ( symbol
   'RPAREN', # ) symbol
   'STRING_LITERAL', # represents a string enclosed in quotation marks
   'COMMA',
   'SEMI_COLON',
   'LINE',
   'WORD',
   'ANY_TEXT',
] + reserved_keywords

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
	 	
def t_WORD(t): #finds identifiers or language keywords
	r'^[A-Z][A-Z][A-Z0-9]*' #a set of 1 or more characters  that start with a-z A-Z or an underscore followed by zero ore more word characters(letters and numbers)
	if t.value in reserved_keywords: # if we have found a keyword return KEYWORD
		t.type =  t.value    # Check for reserved words
		return t
	

def t_FLOAT(t): # floating point number detection
	r'\d*\.\d+'
	t.value = float(t.value)    
	return t
	
def t_INT(t): # integer number detection
	r'\d+'
	t.value = int(t.value)
	return t

def t_ANY_TEXT(t) : 
	r'\b.+' 
	t.type = 'ANY_TEXT'
	return t

def t_error(t): # Error handling rule
	#runtime.machine.error("Illegal characters '{}' at line {}".format(t.value ,t.lexer.lineno), verbose=False, position=t.lexpos)
	t.lexer.skip(len(t.value))

command_lexer = command_lex.lex() # Build the lexer