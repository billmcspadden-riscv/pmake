# vim: set tabstop=4 shiftwidth=4 noexpandtab
# ================================================================
# Filename:		Makefile
#
# Description:	Makefile for building and running tests of pmake
#
# Author(s):	Bill McSpadden (bill@riscv.org)
#
# Revision:		See git log
#
# ================================================================
#
#===========================================================================
# Makefile Variables
#
# SHELL is set to /bin/sh as default for make
#	On Ubuntu,  /bin/sh is a symlink to /bin/dash
#	/bin/dash does not behave much like bash.
#	I want bash to be the shell we use in this environment,
#	not dash.
SHELL := /bin/bash

# TEST_DIR_PATH_KEYDIR is the directory name under which the
#	test directory exists.  This directory contains the items
#	needed to build and run RISC-V tests.  This keyword is needed
#	in order that this makefile and all 'included' makefiles can
#	find the consistent set of tools for building and running
#	tests.
TEST_DIR_PATH_KEYDIR := TEST_DIR_ROOT

# TEST_DIR_PATH is the full directory path to the current test
#	directory.  This is an important variable for running in this 
#	particular enviornment.
TEST_DIR_PATH	:= $(shell 														\
	sandbox_root=$$PWD ;														\
	if [[ "$$sandbox_root" =~ /${TEST_DIR_PATH_KEYDIR}/ ]] ; 					\
		then 																	\
		while [ ! `basename $$sandbox_root` == ${TEST_DIR_PATH_KEYDIR} ] ;		\
			do																	\
			sandbox_root=`dirname $$sandbox_root`; 								\
			if [[ $sandbox_root == "/" ]] ;										\
                then															\
		        echo "NULL" ;													\
                break ;															\
                fi;																\
			done ;																\
		echo "$$sandbox_root" ;													\
	else																		\
		echo "NULL" ;															\
		fi;																		\
	)

include ${TEST_DIR_PATH}/lib/pmake/Makefile.common.top

# ===========================================================================
# Test
PMAKE_MAKEFILE					:= Makefile.py
PMAKE_ARGS						:= -f ${PMAKE_MAKEFILE}
TARGET							:= 
PMAKE_ARGS						+= ${TARGET}
ENV_PMAKE_CMD_LINE_VAR_NAME		:= COMMAND_LINE_VARIABLE
ENV_PMAKE_CMD_LINE_VAR_VAL 		:= foobar
PMAKE_ARGS						+= ${ENV_PMAKE_CMD_LINE_VAR_NAME}=${ENV_PMAKE_CMD_LINE_VAR_VAL} 

TESTLIST	:= $(call add_test,${PMAKE_ARGS},${ENV_PMAKE_CMD_LINE_VAR_NAME},${ENV_PMAKE_CMD_LINE_VAR_VAL},${TESTLIST})

## ===========================================================================
# Test
PMAKE_MAKEFILE					:= Makefile.py
PMAKE_ARGS						:= -f ${PMAKE_MAKEFILE}
TARGET							:= 
PMAKE_ARGS						+= ${TARGET}
ENV_PMAKE_CMD_LINE_VAR_NAME		:= COMMAND_LINE_VARIABLE
ENV_PMAKE_CMD_LINE_VAR_VAL 		:= 3
PMAKE_ARGS						+= ${ENV_PMAKE_CMD_LINE_VAR_NAME}=${ENV_PMAKE_CMD_LINE_VAR_VAL}

TESTLIST	:= $(call add_test,${PMAKE_ARGS},${ENV_PMAKE_CMD_LINE_VAR_NAME},${ENV_PMAKE_CMD_LINE_VAR_VAL},${TESTLIST})

include ${TEST_DIR_PATH}/lib/pmake/Makefile.common.bottom

