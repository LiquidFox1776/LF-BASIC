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

import os
import argparse
from repl import cmd_parse
import sys
		

def main() :
	cmd_parse.parser.parse('CLS', lexer=cmd_parse.command_lexer)
	print("LF-BASIC")
	print("Created by LiquidFox1776 2018")
	print("\n\n")
	
	while True :
		line = input(">")
		cmd_parse.parser.parse(line, lexer=cmd_parse.command_lexer)		

if __name__ == '__main__' :
	if len(sys.argv) == 1 :
		main()
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--file', '-f' ,help='Program file to run', required=False, action='store_true')
	args, unknown = arg_parser.parse_known_args()
	args.file = unknown[0] # we will attempt to use the first arg as a file
    
	if args.file != '' :
		cmd_parse.load_file(args.file)
		cmd_parse.parser.parse("RUN", lexer=cmd_parse.command_lexer)		
	else : # interactive mode
		main()