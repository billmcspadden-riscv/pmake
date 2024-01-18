#! /usr/bin/env python3

#=====================================================================

# In order to do some reasonable self-checking in this test,  we need
#   a mechanism to get the names of the command line arguments and
#   their values.  To do this,  we will use environment variables to
#   get the expacted names and values. The test driver (the GNU makefile)
#   must set these env vars and then pass the same values on the
#   pmake invocation.
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

# The following bit of code shows how pmake can access command
#   line settings of pmake variables
#
# TODO: To make this more like GNU Make, replace the following with ifdef.   Can do?
#   GNU make does something like:
#       ifndef <var>
#           <var> := <something>
#       endif
#   GNU make also  has ...
#       <var> ?= <something>
#   ... where <var> is set to <something> if <var> does not exist
#   How to replicate in pmake?

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

# We don't actually use LOGFILE in this test for any specific purpose.
#   But other tests will typically use the logfile for reporting test
#   status, especially errors.
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

def access_command_line_variable_from_within_rule__recipe(t) :
    echo("COMAND_LINE_VARIABLE: " + COMMAND_LINE_VARIABLE)

Rule(
    "access_command_line_variable_from_within_rule",
    [], 
    access_command_line_variable_from_within_rule__recipe, 
    PHONY
    )


