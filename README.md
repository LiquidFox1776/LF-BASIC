# LF-BASIC
LF-BASIC is a BASIC interpreter based roughly on Minimal BASIC (https://www.ecma-international.org/publications/files/ECMA-ST-WITHDRAWN/ECMA-55,%201st%20Edition,%20January%201978.pdf). It is written in Python and uses ply (https://github.com/dabeaz/ply) for the lexer and parser. This project is still a work in progress but it is functional and capable of running The Oregon Trail 1978 https://github.com/LiquidFox1776/oregon-trail-1978-basic.

## Prerequisites 
This project depends on ply and can be installed with the following command `pip install ply`

## Usage
The interpreter can be run in an interactive shell or the interpreter can accept command line arguments to load a file from the command line, see the below usage for the arguments that the interpreter will accept

```usage: BASIC.py [-h] [--file]

optional arguments:
  -h, --help  show this help message and exit
  --file, -f  Program file to run
```

#### Examples
```
python BASIC.py -f yourprogram.bas
python BASIC.py yourprogram.bas
```

#### Interactive Shell Commands
The following commands are available when running in the interactive shell
```
CLS - Clears the screen
LOAD filename - Loads a bas file specified by filename
RUN - Runs a loaded or entered program
DEBUG - Steps through the program line by line displaying various pieces of information
LIST - Displays the program currently in memory
EXIT - Exits the interpreter
HELP - Supposed to display help information, but does not do so currently
```

Program lines can be entered in the  the interactive shell by typing a line number followed by a statement followed by the enter key. Once the program is entered in that manner a `RUN` or `DEBUG` command can be issued to run the BASIC program

## Notes
This is still a work in progress with some known issues and will take some time before I consider it to be stable.
I estimate that I will perform some updates to this project at least once a week.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
