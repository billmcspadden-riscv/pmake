# vim: set tabstop=4 shiftwidth=4 noexpandtab
# ================================================================
# Filename:		Makefile
#
# Description:	Makefile for building.....

# Author(s):	Bill McSpadden (william.c.mcspadden@gmail.com)
#
# Revision:		See revision control log 
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
$(info SHELL: ${SHELL})

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

# Use the GNU Make Standard Library.  It provides a Make API
#	for useful data structures and functions.
include ${TEST_DIR_PATH}/lib/gmsl.git/gmsl

PMAKE_PATH		:= ${TEST_DIR_PATH}/../bin/pmake.py

# ===========================================================================
# Test
PMAKE_MAKEFILE					:= Makefile.py
ENV_PMAKE_CMD_LINE_VAR_NAME		:= COMMAND_LINE_VARIABLE
ENV_PMAKE_CMD_LINE_VAR_VAL 		:= foobar
# generate uniq testname for this test. add to assoc test array
LOGFILE							:= logfile.txt

# ===========================================================================
# Print out usefule Makefile variables

$(info ============================================)
$(info Makefile Variables:)
$(info     SHELL:                  ${SHELL})
$(info     TEST_DIR_PATH           ${TEST_DIR_PATH})
$(info     PMAKE_PATH              ${PMAKE_PATH})
$(info     LOGFILE                 ${LOGFILE})
$(info     COMMAND_LINE_VARIABLE   ${COMMAND_LINE_VARIABLE})
$(info ============================================)


#===========================================================================
# Rules

default:
	@echo "supported Makefile targets:";
	@echo "   all";
	@echo "   build -         compile/build the object";
	@echo "   run -           run the built object";
	@echo "   install -       install object into a location";
	@echo "   check -         check if the run passed or failed";
	@echo "   clean -         remove local artifacts";
	@echo "   clean_all -     same as 'clean' but also removes installed objects";
	@echo "   default -       this target"


all:


build:


install:


# TODO: need to add a check for a variable set to a number
# TODO: need to add a test for a variable not being set (and that it
#		can be optionally created and set within a pmake makefile
run:
	# Set env vars so that the pmake makefile can see what the values	\
	#	from the command line are supposed to be.						\
	export ENV_PMAKE_CMD_LINE_VAR_NAME=${ENV_PMAKE_CMD_LINE_VAR_NAME} ; \
	export ENV_PMAKE_CMD_LINE_VAR_VAL=${ENV_PMAKE_CMD_LINE_VAR_VAL} ; 	\
	${PMAKE_PATH} LOGFILE=${LOGFILE} ${ENV_PMAKE_CMD_LINE_VAR_NAME}=${ENV_PMAKE_CMD_LINE_VAR_VAL} >> ${LOGFILE} ; \
	if [ $$? -ne 0 ] ; 																					\
		then 																							\
		# stdout must go into logfile,  not test.failed. test.failed and test.passed are only			\
		# created in the check target.																	\
		echo "error (GNU make): setting_variable_from_command_line test failed with nonzero exit code" >> ${LOGFILE}    ; 		\
	else																											\
		echo "(GNU make) pmake exited with a zero exit status. yay" >> ${LOGFILE} ; 											\
		fi ;

check:
	rm -f test.passed test.failed ;
	bn=`basename $$PWD` ;																							\
	if ! [ -e ${LOGFILE} ] ;																						\
		then																										\
		echo "FAILED: (GNU make): $${bn} test failed.  no logfile after 'make run': ${LOGFILE}" >> test.failed ; 	\
		exit 1  ;																									\
		fi ;																										\
	grep --ignore-case --quiet error ${LOGFILE} ;																	\
	if [ $$? -eq 0 ] ;																								\
		then																										\
		echo "error (GNU make): $${bn} test failed.  keyword 'error' found in logfile: ${LOGFILE}" >> test.failed ;	\
		fi ;																										\
	grep               --quiet COMMAND_LINE_VARIABLE ${LOGFILE} ;													\
	if [ $$? -eq 1 ] ;																								\
		then																										\
		echo "error (GNU make): $${bn} test failed.  keyword 'COMMAND_LINE_VARIABLE' not found in logfile: ${LOGFILE}" >> test.failed ;	\
		fi ;																										\
	grep               --quiet LOGFILE ${LOGFILE} ;																	\
	if [ $$? -eq 1 ] ;																								\
		then																										\
		echo "error (GNU make): $${bn} test failed.  keyword 'LOGFILE' not found in logfile: ${LOGFILE}" >> test.failed ;	\
		fi ;																										\
	if ! [ -e test.failed ] ;																						\
		then																										\
		echo "PASSED: (GNU_MAKE): $${bn}" >> test.passed ;															\
		fi;

clean:
	rm -f test.passed test.failed ${LOGFILE}

# Cleans local artifacts and the install location
clean_all:



