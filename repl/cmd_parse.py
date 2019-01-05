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

from .cmd_tokenizer import *
import ply.yacc as command_yacc
from runtime import runtime
import os
import platform

if platform.system() == 'Windows' :
	cls_command = 'cls'
else :
	cls_command = 'clear'

command_help = {'CLS' :' - Clears the screen',
'LOAD' :'filename - Loads a bas file specified by filename',
'RUN' :'- Runs a loaded or entered program',
'DEBUG': '- Steps through the program line by line displaying various pieces of information',
'LIST' :'- Displays the program currently in memory',
'EXIT' :'- Exits the interpreter',
'HELP' :'- Displays help information'
}
def load_file(program) :
	try :
		with open(program, 'r') as file :
			source_code = file.readlines()
	except :
		print('Cannot read ', program)
	else :	
		for line in source_code :
			parser.parse(line, lexer=command_lexer)
		

def p_line(p):
	'''
	line : command
	'''

def p_command(p):
	'''
	command : list
				| exit
				| run
				| cls
				| erase
				| help
				| debug
				| load
				| program_line
				| empty
	'''
	
def p_list(p) :
	'''
	list : LIST
	'''
	for i in runtime.machine.instructions :
		print(i)
	
def p_program_line(p) :
	'''
	program_line : INT ANY_TEXT
					| INT
	'''
	if len(p) == 3 :
		runtime.machine.instructions.append([p[1], str(p[2])])
	
def p_help(p) :
	'''
	help : HELP 
	help : HELP ANY_TEXT
	'''
	if len(p) == 2 :
		for command in command_help :
			print(command, command_help[command])
	else :
		if p[2] in command_help :
			print(p[2], command_help[p[2]])
		else :
			print('Command not found')
	
def p_erase(p) :
	'''
	erase : ERASE
	'''
	runtime.machine.instructions.clear()
def p_cls(p) :
	'''
	cls : CLS
	'''	
	os.system(cls_command)
	
def p_run(p) :
	'''
	run : RUN
	'''
	runtime.machine.run()
def p_exit(p) :
	'''
	exit : EXIT
	'''
	exit()
	
def p_debug(p) :
	'''
	debug : DEBUG
	'''
	runtime.machine.run(debug=True)

def p_load(p) :
	'''
	load : LOAD ANY_TEXT
	'''
	load_file(p[2])
	
def p_empty(p) :
	'''
	empty :
	'''
	p[0] = None

def p_error(p) :
	print('Syntax Error')
parser = command_yacc.yacc()