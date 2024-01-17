#! /usr/bin/env python3

# TODO: replace the following with ifdef.   Can do?
#   GNU make does something like:
#       ifndef <var>
#           <var> := <something>
#       endif
#   GNU make also  has ...
#       <var> ?= <something>
#   ... where <var> is set to <something> if <var> does not exist
#   How to replicate in pmake?


try:
    COMMAND_LINE_VARIABLE
except NameError:
    echo("error: the command line variable, 'COMMAND_LINE_VARIABLE', was not set")
    COMMAND_LINE_VARIABLE = None
else:
    echo("COMMAND_LINE_VARIABLE: " + COMMAND_LINE_VARIABLE)

try:
    LOGFILE
except NameError:
    echo("error: the command line variable, 'LOGFILE', was not set")
    LOGFILE = "logfile_set_by_pmake.txt"
else:
    echo("LOGFILE: " + LOGFILE, ">>", LOGFILE)



def dummy(t) :
    True

Rule("default", [], dummy, PHONY)


