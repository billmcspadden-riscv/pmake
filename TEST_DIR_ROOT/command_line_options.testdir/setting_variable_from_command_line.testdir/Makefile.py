#! /usr/bin/env python3

#=====================================================================
# The following pmake variables are being set from the command line
#   when processing the command line arguments.
#
# TODO: replace the following with ifdef.   Can do?
#   GNU make does something like:
#       ifndef <var>
#           <var> := <something>
#       endif
#   GNU make also  has ...
#       <var> ?= <something>
#   ... where <var> is set to <something> if <var> does not exist
#   How to replicate in pmake?

ENV_PMAKE_CMD_LINE_VAR_NAME = os.getenv('ENV_PMAKE_CMD_LINE_VAR_NAME')
if ENV_PMAKE_CMD_LINE_VAR_NAME == None :
    echo("error (pmake): env var 'ENV_PMAKE_CMD_LINE_VAR_NAME' was not set")
    # Can't do any further testing,  so exit
    sys.exit(1)

ENV_PMAKE_CMD_LINE_VAR_VAL = os.getenv('ENV_PMAKE_CMD_LINE_VAR_VAL')
if ENV_PMAKE_CMD_LINE_VAR_VAL == None :
    echo("error (pmake): env var 'ENV_PMAKE_CMD_LINE_VAR_VAL was not set")
    # Can't do any further testing,  so exit
    sys.exit(1)

if ENV_PMAKE_CMD_LINE_VAR_NAME != 'COMMAND_LINE_VARIABLE' :
    echo("error (pmake): name of command line variable is incorrect. expected: 'COMMANDLINE_VARIABLE'.  received: '" + ENV_PMAKE_CMD_LINE_VAR_NAME + "'")
    sys.exit(1)

# Now for the meat of the test.  Attempt to access the variable.
try:
    COMMAND_LINE_VARIABLE
except NameError:
    echo("error (pmake): the command line variable, 'COMMAND_LINE_VARIABLE', was not set")
    sys.exit(1)
else:
    echo("COMMAND_LINE_VARIABLE: " + COMMAND_LINE_VARIABLE)

if COMMAND_LINE_VARIABLE != ENV_PMAKE_CMD_LINE_VAR_VAL :
    echo("error (pmake): incorrect value for COMMAND_LINE_VARIABLE. expected: " + ENV_PMAKE_CMD_LINE_VAR_VAL + " received: " + COMMAND_LINE_VARIABLE)



try:
    LOGFILE
except NameError:
    echo("error (pmake): the command line variable, 'LOGFILE', was not set")
    LOGFILE = "logfile_set_by_pmake.txt"
else:
    echo("LOGFILE: " + LOGFILE, ">>", LOGFILE)



def dummy(t) :
    True

Rule("default", [], dummy, PHONY)


