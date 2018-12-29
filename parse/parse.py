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
from tokenizer.tokenizer import *
import ply.yacc as yacc
import os
from runtime import runtime
import platform

if platform.system() == 'Windows' :
	cls_command = 'cls'
else :
	cls_command = 'clear'

def p_line(p):
	'''
	line : INTEGER statement
		| INTEGER
	'''
def p_line_number_error(p):
	'''
	line : error statement
	'''
	print('Line Number Error')
	runtime.machine.error()

#def p_line_statement_error(p) :
#	'''
#	line : INTEGER error
#	'''
#	runtime.machine.error('Syntax Error bad statement ' + str(p[2].__dict__['value']), 
#	position=p[2].__dict__['lexpos'],
#	fatal = True, 
#	verbose=False  )

def p_statement(p):
	'''
	statement : let
				| end
				| if
				| goto
				| for
				| next
				| print
				| cls
				| input
				| def
				| dumpvar
				| dumpfun
				| on
				| gosub
				| return
				| data
				| restore
				| read
				| dim
				| randomize
				| stop
				| option
				| eval_exp
	'''

precedence = (
	 ('left', 'SEMI_COLON', 'COMMA'),
	 ('left', 'INTEGER', 'FLOAT'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
	 ('left', 'CIRCUMFLEX'),
	 ('left', 'LPAREN', 'RPAREN'),
	 ('left', 'B_NUM_FN', 'B_STR_FN', 'FN'),
	 ('right', 'UMINUS'), 
	 
)

def p_option(p) :
	'''
	option : OPTION BASE INTEGER
	'''
def p_option_bad_keyword(p) :
	'''
	option : OPTION error INTEGER
	'''
	runtime.machine.error('Syntax Error bad keyword {} expected BASE'.format(p[2].__dict__['value']), 
	position=p[2].__dict__['lexpos'],
	fatal = True, 
	verbose=False)
	
def p_option_bad_base(p) :
	'''
	option : OPTION BASE error
	'''
	runtime.machine.error('Syntax Error bad BASE option expected INTEGER ' + str(p[3].__dict__['value']), 
	position=p[3].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )
	
def p_eval_exp(p):
	'''
	eval_exp : EVAL numeric_expression
	'''
	#print('EVAL FROM EXP_PARSER', p[2])
	runtime.machine.eval_value = p[2]
	
def p_randomize(p) :
	'''
	randomize : RANDOMIZE
	'''
	runtime.machine.randomize()
	
def p_let(p) :
	# Rules for parsing LET keyword
	# examples LET A = A
	# LET A = 123 + 50
	# LET A$ = "STRING"
	'''
	let : LET STRING_VARIABLE EQUALS string_expression
		| LET NUMERIC_ARRAY INTEGER RPAREN EQUALS numeric_expression
		| LET NUMERIC_ARRAY INTEGER COMMA INTEGER RPAREN EQUALS numeric_expression
		| LET STRING_ARRAY INTEGER RPAREN EQUALS string_expression
		| LET STRING_ARRAY INTEGER COMMA INTEGER RPAREN EQUALS string_expression
		| LET SIMPLE_NUMERIC_VARIABLE EQUALS numeric_expression
	'''
	# p[1] LET 
	# p[2] IDENT
	# p[4] string_literal or expression
	if len(p) == 5 :
		if p[2][-1] == '$' :
			runtime.machine.set_variable(p[2],'STRING','"' + p[4] + '"')
		else :
			if float(p[4]).is_integer() == True :
				runtime.machine.set_variable(p[2],'INTEGER',int(p[4]))
			else :
				runtime.machine.set_variable(p[2],'FLOAT',p[4])
	else : # we are working with arrays
		if p.__dict__['slice'][2].type == 'STRING_ARRAY' :
			if len(p) == 7 :
				p[6] = '"' + p[6] + '"'
			else :
				p[8] = '"' + p[8] + '"'

		if len(p) == 7 :
			runtime.machine.set_array_value(p[2], [p[3]],p[6] ) #, variable name, index, value one dimensional array
		elif len(p) == 9 :
			runtime.machine.set_array_value(p[2], '['+str(p[3])+']['+str(p[5])+']', p[8]) # two dimensional array

def p_dim(p) :
	# examples
	# DIM A(10)
	# DIM A(10,10)
	# DIM A$(10)
	# DIM A$(10,20)
	'''
	dim : DIM STRING_ARRAY INTEGER RPAREN
		| DIM NUMERIC_ARRAY INTEGER RPAREN
		| DIM STRING_ARRAY INTEGER COMMA INTEGER RPAREN
		| DIM NUMERIC_ARRAY INTEGER COMMA INTEGER RPAREN
	'''

	var_type = p.__dict__['slice'][2].type
	if len(p) == 7 :
		runtime.machine.eval_dim(p[2],var_type,[p[3], p[5]]) # variable name upper bound1, upper bound2
	elif len(p) == 5 :
		runtime.machine.eval_dim(p[2],var_type, [p[3]]) # variable name, upper bound

def p_dim_bad_variable_name(p) :
	'''
	dim : DIM error INTEGER RPAREN
		| DIM error INTEGER COMMA INTEGER RPAREN
	'''
	runtime.machine.error('Syntax Error bad variable name ' + str(p[2].__dict__['value']), 
	position=p[2].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )
	
def p_dumpvar(p) : #  Shows the variable table
	'''
	dumpvar : DUMPVAR
	'''
	print(runtime.machine.variable_table)
	p[0] = p[1]
	
def p_dumpfun(p) : # shows the function table
	'''
	dumpfun : DUMPFUN
	'''
	p[0] = p[1]
	
def p_if(p) :
	# Rules for parsing IF keyword
	# examples IF expression relational expression then int where int is a line number
	# IF A > 1 THEN 600
	'''
	if : IF numeric_expression EQUALS numeric_expression THEN INTEGER
		| IF numeric_expression LT GT numeric_expression THEN INTEGER
		| IF numeric_expression GT numeric_expression THEN INTEGER
		| IF numeric_expression LT numeric_expression THEN INTEGER
		| IF numeric_expression GT EQUALS numeric_expression THEN INTEGER
		| IF numeric_expression LT EQUALS numeric_expression THEN INTEGER
		| IF string_expression EQUALS string_expression THEN INTEGER
	'''
	if(len(p) == 7) : # if true we are working with a relational other than <>
		tmp_p = list((p[1],p[2],p[3],p[4],p[6]))
		runtime.machine.eval_if(tmp_p)
	else : # two operators are being used
		tmp_p = list((p[1],p[2],p[3],p[4],p[5],p[7]))
		runtime.machine.eval_if(tmp_p)

def p_goto(p) :
	# Rules for parsing GOTO keyword
	# examples GOTO INTEGER
	# GOTO 999
	'''
	goto : GOTO INTEGER
	'''
	# p[1] GOTO
	# p[1] line number to go to
	runtime.machine.goto(p[2])
	
def p_goto_bad_number(p) :
	'''
	goto : GOTO error
	'''
	runtime.machine.error('Syntax Error bad INTEGER expected a number not ' + str(p[2].__dict__['value']), 
	position=p[2].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )

def p_gosub(p) :
	'''
	gosub : GOSUB INTEGER
	'''
	runtime.machine.gosub(p[2])

def p_gosub_error(p) :
	'''
	gosub : GOSUB error
	'''
	print('Syntax Error bad line number ', p[2])
	runtime.machine.error()

def p_return(p) :
	'''
	return : RETURN
	'''
	runtime.machine.gosub_return()

def p_on(p) :
	# on numeric_expression go to line_number_list
	# example on x go to 10,20,30
	# x is rounded
	'''
	on : ON numeric_expression GO TO line_number_list
	'''
	#TODO ? ADD GOTO line_number list as well, might implement does not follow ECMA-55
	#p[2] is numeric expression
	#p[5] is a list of line numbers
	runtime.machine.eval_on(p[2], p[5])

def p_on_bad_numeric_expression(p) :
	# on numeric_expression go to line_number_list
	# example on x go to 10,20,30
	# x is rounded
	'''
	on : ON error GO TO line_number_list
	'''
	runtime.machine.error('Syntax Error bad numeric expression ' + str(p[2].__dict__['value']), 
	position=p[2].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )

def p_on_bad_numeric_keyword_go(p) :
	# on numeric_expression go to line_number_list
	# example on x go to 10,20,30
	# x is rounded
	'''
	on : ON numeric_expression error TO line_number_list
	'''
	runtime.machine.error('Syntax Error bad keyword {} expected GO '.format(p[3].__dict__['value']), 
	position=p[3].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )

def p_on_bad_numeric_keyword_to(p) :
	# on numeric_expression go to line_number_list
	# example on x go to 10,20,30
	# x is rounded
	'''
	on : ON numeric_expression GO error line_number_list
	'''
	runtime.machine.error('Syntax Error bad keyword {} expected TO '.format(p[4].__dict__['value']), 
	position=p[4].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )

def p_on_bad_number_list(p) :
	# on numeric_expression go to line_number_list
	# example on x go to 10,20,30
	# x is rounded
	'''
	on : ON numeric_expression GO TO error
	'''
	runtime.machine.error('Syntax Error bad number list ' + str(p[5].__dict__['value']), 
	position=p[5].__dict__['lexpos'],
	fatal = True, 
	verbose=False  )
	


def p_line_number_list(p) :
	'''
	line_number_list : line_number_list line_number_list_sep line_number_list
	'''
	if len(p) == 4 :
		p[0] = p[1], p[2], p[3]
	elif len(p) == 3 :
		p[0] = p[1], p[2]
	else:
		p[0] = p[1]
def p_line_number_item(p) :
	'''
	line_number_list : INTEGER
	'''
	p[0] = p[1]

def p_line_number_list_sep(p) :
	'''
	line_number_list_sep : COMMA
	'''
	p[0] = None
def p_data(p) :
	# example DATA 125, "test"
	'''
	data : DATA data_list
	'''
	#p[2] is a list of expressions
	runtime.machine.eval_data_list(p[2])

def p_data_list(p) :
	'''
	data_list : data_list data_list_sep data_list
	'''
	if len(p) == 4 :
		p[0] = p[1], p[2], p[3]
	elif len(p) == 3 :
		p[0] = p[1], p[2]
	else:
		p[0] = p[1]

def p_data_list_expression(p) :
	'''
	data_list : expression
	'''
	p[0] = p[1]

def p_data_list_sep(p) :
	'''
	data_list_sep : COMMA
	'''
	pass

def p_read(p) :
	# example READ A, B, C$, D ...
	'''
	read : READ read_list
	'''
	#p[2] is a list of expressions
	runtime.machine.eval_read_list(p[2])

def p_read_list(p) :
	'''
	read_list : read_list read_list_sep read_list
	'''
	if len(p) == 4 :
		p[0] = p[1], p[2], p[3]
	elif len(p) == 3 :
		p[0] = p[1], p[2]
	else:
		p[0] = p[1]

def p_read_list_variables(p) : #TODO update when arrays are implemented
	'''
	read_list : SIMPLE_NUMERIC_VARIABLE 
				| STRING_VARIABLE
	'''
	p[0] = p[1]

def p_read_list_sep(p) :
	'''
	read_list_sep : COMMA
	'''
	pass
	
def p_restore(p) : # resets the data pointer
	'''
	restore : RESTORE
	'''
	runtime.machine.data_restore()
def p_for(p) :
	# Rules for parsing FOR keyword
	# examples FOR identifier EQUALS expression TO expression STEP expression
	# TODO needs implemented
	'''
	for : FOR SIMPLE_NUMERIC_VARIABLE EQUALS numeric_expression TO numeric_expression STEP numeric_expression
		| FOR SIMPLE_NUMERIC_VARIABLE EQUALS numeric_expression TO numeric_expression
	'''
	# p[1] FOR
	# p[2] IDENT function or variable
	# p[3] =
	# p[4] a numeric or string expression
	# p[5] TO
	# p[6] a numeric or string expression
	# p[7] optional STEP key word
	# p[8] optioanl increment decrement expression

	
	if(len(p) == 7) : # If true for loop without STEP
		p[0] = (p[1], p[2], p[4],p[6])
		runtime.machine.push_for(p[2], p[4],p[6]) # variable_name, init_value, end_value, step value
	else : # if true step was used
		runtime.machine.push_for(p[2], p[4],p[6], p[8]) # variable_name, init_value, end_value, step value
	
	
def p_next(p) :
	# Rules for parsing NEXT keyword
	# examples NEXT IDENT
	# NEXT X
	'''
	next : NEXT SIMPLE_NUMERIC_VARIABLE
	'''
	# p[1] NEXT
	# p[2] SIMPLE_NUMERIC_VARIABLE
	runtime.machine.next(p[2])
	p[0] = (p[2])

def p_print(p) :
	# Rules for parsing NEXT keyword
	# examples PRINT IDENT
	# PRINT STRING_LITERAL
	# PRINT PRINT_LIST
	'''
	print :  PRINT print_list
			| PRINT
	'''
	
	if len(p) > 2 : # if true we have something to print
		runtime.machine.eval_print(p[2])
	else :
		runtime.machine.eval_print('')
		

def p_print_list(p):
	# print_list = print_list print_list_sep
	# Examples of print list
	# PRINT "TEST ", 1
	# PRINT "TEST" ;;;;;;;
	# PRINT 1;;;;;;" TEST"
	'''
	print_list :  print_list_sep print_list
				| print_list print_list_sep print_list
				| print_list print_list_sep
				| print_list_sep
	'''
	# Depending on the length of p you can have different elements TODO? we could just use a loop
	if(len(p) == 4):
		p[0] = p[1],p[2],p[3]
	elif(len(p)==3) :
		p[0] = p[1], p[2]
	else : 
		p[0] = p[1]

def p_print_item(p): # print item can contain expressions and string literals
	'''
	print_list : expression
	'''
	p[0] = p[1]

def p_print_list_sep(p) : # part of the print statement rules that define what a print separator is , or ;
	'''
	print_list_sep : print_semi_colon
					| print_comma
	'''
	p[0] = p[1]
def p_print_semi_colon(p) :
	'''print_semi_colon : SEMI_COLON'''
	p[0] = [2]

def p_print_comma(p) :
	'''print_comma : COMMA'''
	p[0] = [1]

def p_def(p) :
	'''
	def : DEF FN EQUALS fn_body_numeric_expression
		| DEF FN LPAREN SIMPLE_NUMERIC_VARIABLE RPAREN EQUALS fn_body_numeric_expression
	'''
	#
	# Note that due how this interpreter is implemented duplicate rules are used with no embedded action to
	# verify the numeric expression in the def statement
	#
	func_body = runtime.machine.instructions[runtime.machine.program_counter][1].split('=')[1] # very hackish
	if( len(p) == 5) :
		runtime.machine.add_function_to_table(p[2], [], func_body)
	else :
		runtime.machine.add_function_to_table(p[2], [p[4]], func_body)

	
def p_fn_body_numeric_expression(p): # Rules for parsing a numeric expression
	'''
	fn_body_numeric_expression : LPAREN fn_body_numeric_expression RPAREN
				| fn_body_numeric_expression CIRCUMFLEX fn_body_numeric_expression
				| fn_body_numeric_expression TIMES fn_body_numeric_expression
				| fn_body_numeric_expression DIVIDE fn_body_numeric_expression
				| fn_body_numeric_expression PLUS fn_body_numeric_expression
				| fn_body_numeric_expression MINUS fn_body_numeric_expression
				| empty
				| fn_body_primary
	'''
	

def p_fn_body_expr_uminus(p): # used to make negative numerical expressions example -1 -A different than - 1 - A
	'''
	 fn_body_numeric_expression : MINUS fn_body_numeric_expression %prec UMINUS
	 '''

def p_fn_body_primary(p) : # contains the basic data that can make up a numeric expression, refer to tokenizer for details
	'''
	fn_body_primary :   INTEGER
						| FLOAT
						| fn_body_u_num_fn
						| fn_body_b_num_fn
						| fn_body_simple_numeric_variable
						| fn_body_numeric_array
	'''

def p_fn_body_u_num_fn(p) : # process user defined function
	'''
	fn_body_u_num_fn : FN LPAREN fn_body_numeric_expression RPAREN
			| FN
	'''

def p_fn_body_b_num_fn(p) : # process built-in functions abs, cos, tan etc...
	'''
	fn_body_b_num_fn : B_NUM_FN empty
		| B_NUM_FN fn_body_numeric_expression
	'''

def p_fn_body_simple_numeric_variable(p) : # rule to detect  a simple numeric variable and return the value
	'''
	fn_body_simple_numeric_variable : SIMPLE_NUMERIC_VARIABLE
	'''

def p_fn_body_numeric_array(p) : # rule to detect  a simple numeric variable and return the value
	'''
	fn_body_numeric_array : NUMERIC_ARRAY INTEGER RPAREN
					|  NUMERIC_ARRAY INTEGER COMMA INTEGER RPAREN
	'''

def p_fn_body_numeric_variable(p) : # made up of simple numeric variables ie A, B, C and array's A(1), B(1,2)
	'''
	fn_body_numeric_variable : fn_body_simple_numeric_variable
					|	fn_body_numeric_array
	'''
	
def p_cls(p) :
	# Rules for parsing CLS keyword
	# examples CLS
	# CLS
	'''
	cls : CLS
	'''
	os.system(cls_command)

def p_end(p) :
	# Rules for parsing END keyword
	# examples END
	# END
	'''
	end : END
	'''
	input()
	exit()

def p_stop(p) :
	# Rules for parsing END keyword
	# examples STOP
	# STOP
	'''
	stop : STOP
	'''
	input()
	exit()
def p_input(p) :
	'''
	input : INPUT string_expression SEMI_COLON SIMPLE_NUMERIC_VARIABLE
			| INPUT string_expression SEMI_COLON STRING_VARIABLE
			| INPUT SIMPLE_NUMERIC_VARIABLE
			| INPUT STRING_VARIABLE
	'''
	if len(p) == 3 :
		runtime.machine.eval_input('? ',p[2]) #INPUT without prompt , ECMA-55 recommends '? ' as a prompt
	elif len(p) == 5 :
		runtime.machine.eval_input(p[2],p[4]) # INPUT with prompt

def p_expression(p) : # an expression can be a string expression or a numeric_expression
	'''
	expression : string_expression
				| numeric_expression
	'''
	p[0] = p[1]
	
def p_numeric_expression(p): # Rules for parsing a numeric expression
	'''
	numeric_expression : LPAREN numeric_expression RPAREN
				| numeric_expression CIRCUMFLEX numeric_expression
				| numeric_expression TIMES numeric_expression
				| numeric_expression DIVIDE numeric_expression
				| numeric_expression PLUS numeric_expression
				| numeric_expression MINUS numeric_expression
				| empty
				| primary
	'''
	if(len(p)) == 4 : # perform the binary action specified below
		if p[2] == '+' :        # addition operation
			p[0] = p[1] + p[3]
		elif p[2] == '-' :      # sub operation
			p[0] = p[1] - p[3]
		elif p[2] == '*' :      # mul operation
			p[0] = p[1] * p[3]
		elif p[2] == '/' :      # div operation
			p[0] = p[1] / p[3]
		elif p[2] == '^' :      # power operation
			p[0] = p[1] ** p[3]
		elif p[1] == '(' :      # working inside of ()
			p[0] = p[2]
	else :
		if p[1] is not None : # make sure we are not working with an empty expression
			if type(p[1]).__name__ != 'list' : 
				if float(p[1]).is_integer() == True : # check to see if we are working with a float
					p[1] = int(p[1]) # if we are not convert to int 
				p[0] = p[1]
			else : #TODO better error handling, fatal exception
				print("ERROR INDEX REQUIRED")
				runtime.machine.error()
				exit()

def p_expr_uminus(p): # used to make negative numerical expressions example -1 -A different than - 1 - A
	'''
	 numeric_expression : MINUS numeric_expression %prec UMINUS
	 '''
	p[0] = -p[2]

def p_primary(p) : # contains the basic data that can make up a numeric expression, refer to tokenizer for details
	'''
	primary :            INTEGER
						| FLOAT
						| u_num_fn
						| b_num_fn
						| simple_numeric_variable
						| numeric_array
	'''

	p[0] = p[1]
def p_b_num_fn(p) : # process built-in functions abs, cos, tan etc...
	'''
	b_num_fn : B_NUM_FN empty
		| B_NUM_FN numeric_expression
	'''
	#p[2] holds the function argument
	if p[2] is not None : # if argument has a value pass it to the function
		p[0] = runtime.machine.eval_function(p[1], True,p[2])
	else : # An argument was not used so pass None
		p[0] = runtime.machine.eval_function(p[1], True,None)

def p_u_num_fn(p) : # process user defined function U_NUM_FN USER NUMERIC FUNCTION
	'''
	u_num_fn : FN numeric_expression
			| FN
	'''

	#p[2] holds the function argument
	if len(p) == 2 :
		p[0] = runtime.machine.eval_function(p[1], False,None) # function name, user defined, no argument
	else :
		if p[2] is not None : # if argument has a value pass it to the function
			p[0] = runtime.machine.eval_function(p[1], False,p[2]) # function name, user defined, argument
		
def p_simple_numeric_variable(p) : # rule to detect  a simple numeric variable and return the value
	'''
	simple_numeric_variable : SIMPLE_NUMERIC_VARIABLE
	'''
	tmp_var = runtime.machine.get_variable_value(p[1]) # lookup variable
	if tmp_var is not None : # if true we found it
		p[0] = tmp_var
	else : # TODO ADD ERROR HANDLING
		print("VARIABLE NOT FOUND")
		runtime.machine.error()
		exit()
	
def p_numeric_array(p) : # rule to detect  a simple numeric variable and return the value
	'''
	numeric_array : NUMERIC_ARRAY INTEGER RPAREN
					|  NUMERIC_ARRAY INTEGER COMMA INTEGER RPAREN
	'''
	if len(p) == 4 :
		tmp_var = runtime.machine.get_array_value(p[1], [p[2]]) # lookup variable
	else :
		tmp_var = runtime.machine.get_array_value(p[1], '['+str(p[2])+']['+str(p[4])+']') # lookup variable
	
	
	if tmp_var is not None : # if true we found a value
		p[0] = tmp_var		
	else : # TODO ADD ERROR HANDLING
		print("VALUE NOT FOUND")
		exit()
	
def p_numeric_variable(p) : # made up of simple numeric variables ie A, B, C and array's A(1), B(1,2)
	'''
	numeric_variable : simple_numeric_variable
					|	numeric_array
	'''
	p[0] = p[1]
def p_string_expression(p): # made up of string variables and literals
	'''
	string_expression : string_literal
						| string_variable
						| b_str_fn
	'''
	p[0] = p[1][1:-1]

def p_string_literal(p) : # rule to detect a quoted "string"
	'''
	string_literal : STRING_LITERAL
	'''
	p[0] = p[1]

def p_string_variable(p) : # grammar rule to handle string variables, string variables consist of letter followed by $
	'''
	string_variable : simple_string_variable
					| string_array
	'''
	p[0] = p[1]

def p_b_str_fn(p) : # process built-in functions abs, cos, tan etc...
	'''
	b_str_fn : B_STR_FN empty
		| B_STR_FN numeric_expression
	'''
	#p[2] holds the function argument
	if p[2] is not None : # if argument has a value pass it to the function
		p[0] = '"' + runtime.machine.eval_function(p[1], True,p[2]) + '"'
	else : # An argument was not used so pass None
		p[0] = +'"' + runtime.machine.eval_function(p[1], True,None) + '"'

def p_simple_string_variable(p) :
	'''
	simple_string_variable : STRING_VARIABLE
	'''
	# examples A$, B$, C$
	tmp_str = runtime.machine.get_variable_value(p[1]) # attempt to get the variables value
	if tmp_str is not None :
		p[0] = tmp_str
	else : #TODO ADD ERROR HANDLING
		print('VARIABLE NOT FOUND')
		exit() # TODO THROW ERROR

def p_string_array(p) :
	'''
	string_array : STRING_ARRAY numeric_expression RPAREN
					|  STRING_ARRAY numeric_expression COMMA numeric_expression RPAREN
	'''
	if len(p) == 4 :
		tmp_var = runtime.machine.get_array_value(p[1], [p[2]]) # lookup variable
	else :
		tmp_var = runtime.machine.get_array_value(p[1], '['+str(p[2])+']['+str(p[4])+']') # lookup variable
	
	if tmp_var is not None : # if true we found a value
		p[0] = '"' + tmp_var + '"'
	else : # TODO ADD ERROR HANDLING
		print("VALUE NOT FOUND")
		exit()
	
def p_empty(p):
	'''
	empty : LPAREN RPAREN
	
	'''
	p[0] = None

def p_error(p) :
#	runtime.machine.error()
#	if p is None :
	pass

parser = yacc.yacc()