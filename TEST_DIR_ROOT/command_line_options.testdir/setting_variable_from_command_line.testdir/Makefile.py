#! /usr/bin/env python3

try:
    COMMAND_LINE_VARIABLE
except NameError:
    echo("error: the command line variable, 'COMMAND_LINE_VARIABLE', was not set")
    COMMAND_LINE_VARIABLE = None
else:
    echo("COMMAND_LINE_VARIABLE: " + COMMAND_LINE_VARIABLE)



def dummy(t) :
    True

Rule("default", [], dummy, PHONY)


