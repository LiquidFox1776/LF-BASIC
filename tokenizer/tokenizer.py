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
import ply.lex as lex
from runtime import runtime

reserved_keywords = [
'BASE',      # used in conjunction with OPTION determines if array bounds start at 0 or 1
'DATA',      # adds data to data
'DEF',       # used to declare functions
'FN',        # used in conjunction with DEF
'DIM',       # used to dimension an array
'END',       # terminates the program
'FOR',       # the start of a for loop
'GO',        # the go in go to
'GOSUB',     # go to sub 
'GOTO',      # jumps to a new line to execute
'IF',        # starts a conditional statement
'INPUT',     # reads user input
'LET',       # used to declare a variable
'NEXT',      # ends a for loop equates to a goto
'ON',        # goes to a line based on expression and list on x
'OPTION',    # used to set options
'PRINT',     # Displays data at the terminal
'RANDOMIZE', # initializes random number generator using random.seed
 'READ',     # reads from data
 'REM',      # Used for comments
 'RESTORE',  # resets the data pointer
 'RETURN',   # returns from a gosub
 'STEP',     # Optional part in a for loop, indicates an incremental or decremental amount 
 'STOP',     # ends the program
 'THEN',     # The then part in if then statements
 'TO',       # The to part in a For to loop
 'CLS',      # Clears the screen
 'DUMPVAR',  # TODO MAY REMOVE AT A LATER DATE
 'DUMPFUN',  # TODO MAY REMOVE AT A LATER DATE
 'EVAL'      # evaluates an expression and sets runtime.machine.eval_value, used to evaluate user functions
 ]
built_in_numeric_functions = ['ABS','ATN','CLK','COS','EXP','INT','LOG','RND','SGN','SIN','SQR','TAN']
built_in_string_functions = ['TAB']


tokens = [
   'INTEGER', # a whole number
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
   'STRING_VARIABLE',
   'STRING_ARRAY',
   'SIMPLE_NUMERIC_VARIABLE',
   'NUMERIC_ARRAY',
   'B_NUM_FN', # Built In Numeric Function
   'B_STR_FN', # Built In String Functions
] + reserved_keywords + built_in_numeric_functions + built_in_string_functions

#--------------------------------------------------------------------------------------------------------------
# Tokenizer
#--------------------------------------------------------------------------------------------------------- 
# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_CIRCUMFLEX = '\^'
t_EQUALS = r'='
t_GT     = r'>'
t_LT     = r'<'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMI_COLON = r';'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Regular expression rules for complex tokens
def t_REM(t): # REM detection/ comment line 
	r'REM .*'
	pass

def t_FN(t):
	r'FN[A-Z]'
	return t
	 
def t_WORD(t): #finds identifiers or language keywords
	r'[A-Z][A-Z][A-Z0-9]*' #a set of 1 or more characters  that start with a-z A-Z or an underscore followed by zero ore more word characters(letters and numbers)
	if t.value in reserved_keywords: # if we have found a keyword return KEYWORD
		t.type =  t.value    # Check for reserved words
		return t

	elif t.value in built_in_numeric_functions: # if we have found a bfn
		t.type =  'B_NUM_FN'    # Check for reserved words
		return t
	elif t.value in built_in_string_functions :
		t.type = 'B_STR_FN'
		return t
	else :
		return t
	

def t_STRING_ARRAY(t): #finds identifiers or language keywords
	r'[A-Z]\$\(' # just like a string only a ( must be included at the end
	t.value = t.value[:-1]
	return t

def t_STRING_VARIABLE(t): #finds identifiers or language keywords
	r'[A-Z]\$' #a set of 1 or more characters  that start with a-z A-Z or an underscore followed by zero ore more word characters(letters and numbers)
	t.type = "STRING_VARIABLE"
	return t


def t_NUMERIC_ARRAY(t): 
	r'[A-Z]\('
	t.value = t.value[:-1]
	return t


def t_SIMPLE_NUMERIC_VARIABLE(t): 
	r'\b[A-Z][0-9]?' 
	return t

def t_FLOAT(t): # floating point number detection
	r'\d*\.\d+'
	t.value = float(t.value)    
	return t
	
def t_INTEGER(t): # integer number detection
	r'\d+'
	t.value = int(t.value)    
	return t

def t_STRING_LITERAL(t) : # detects a string "string"
	r'\"[A-Za-z0-9\s\.!#\$%&\'\(\)\*,/:;<>\?\^_\+=-]*\"' # a set of characters enclosed by quotes
	t.type = "STRING_LITERAL"
	return t

def t_newline(t): # new line detection and line number tracking
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t

def t_error(t): # Error handling rule
	runtime.machine.error("Illegal characters '{}' at line {}".format(t.value ,t.lexer.lineno), verbose=False, position=t.lexpos)
	t.lexer.skip(len(t.value))
 
lexer = lex.lex() # Build the lexer