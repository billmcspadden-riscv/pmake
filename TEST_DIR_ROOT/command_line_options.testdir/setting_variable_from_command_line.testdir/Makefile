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

uniq_testname = \
	$(addprefix pmake__,$(shell echo $1 | sed 's/ /_/g' | sed 's/-/_/g' | sed 's/=/_/g' | sed 's/__/_/g'))

PMAKE_PATH		:= ${TEST_DIR_PATH}/../bin/pmake.py
LOGFILE			:= pmake_logfile.txt

add_test = \
$(strip \
$(call set,PMAKE_ARGS_AA,$(call uniq_testname,$1),$1) \
$(call set,ENV_VAR_NAME_AA,$(call uniq_testname,$1),$2) \
$(call set,ENV_VAR_VAL_AA,$(call uniq_testname,$1),$3) \
$(call set,LOGFILE_AA,$(call uniq_testname,$1),$(call uniq_testname,$1).artifactdir/${LOGFILE}) \
$(call set_insert,$(call uniq_testname,$1),$4) \
)

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

# ===========================================================================
# Convert gmsl assoc arrays into text suitable for bash assoc arrays
PMAKE_ARGS_AA_FOR_SH 	:= $(foreach var,${TESTLIST},["$(var)"]="$(call get,PMAKE_ARGS_AA,$(var))" )
ENV_VAR_NAME_AA_FOR_SH 	:= $(foreach var,${TESTLIST},["$(var)"]="$(call get,ENV_VAR_NAME_AA,$(var))" )
ENV_VAR_VAL_AA_FOR_SH 	:= $(foreach var,${TESTLIST},["$(var)"]="$(call get,ENV_VAR_VAL_AA,$(var))" )
LOGFILE_AA_FOR_SH		:= $(foreach var,${TESTLIST},["$(var)"]="$(call get,LOGFILE_AA,$(var))" )

# ===========================================================================
# Print out usefule Makefile variables

$(info ============================================)
$(info Makefile Variables:)
$(info     SHELL:                  ${SHELL})
$(info     TEST_DIR_PATH           ${TEST_DIR_PATH})
$(info     PMAKE_PATH              ${PMAKE_PATH})
$(info     LOGFILE                 ${LOGFILE})
$(info     TESTLIST                ${TESTLIST})
$(info ============================================)




#===========================================================================
# Rules

default:
	@echo "supported Makefile targets:";
	@echo "   default -       this target"
	@echo "   build -         compile/build the object";
	@echo "   run -           run the built object";
	@echo "   check -         check if the run passed or failed";
	@echo "   clean -         remove local artifacts";

TESTDIRS = $(wildcard *.testdirs)

.PHONY: run
run:
	@echo "making \"$@\" in $$PWD" ;
	@for testdir in ${TESTDIRS}; 										\
		do																\
		if [ ! -e $$testdir/Makefile ] ;								\
			then														\
			echo "ERROR: no Makefile in $$testdir." >> test.failed;		\
			fi ;														\
		make -C $$testdir $@ ;											\
		if [ $$? -ne 0 ] ;                                              			\
			then                                                            		\
			echo "'make -C $$testdir $@' exited with nonzero exit status" >> test.failed ;	\
			fi ;																			\
		done;
	if [ ! -z "${TESTLIST}" ] ;															\
		then																		\
		make run_tests ;															\
		if [ $$? -ne 0 ] ;                                              			\
			then                                                            		\
			echo "'make run_tests' exited with nonzero exit status" >> test.failed ;	\
			fi ;																			\
		fi;



# TODO: redirect stderr to logfile
# TODO: replace test.failed with something else.  test.failed only used by target 'check'
.PHONY: run_tests
run_tests:
	@echo "making \"$@\" in $$PWD" ;
	declare -A pmake_args_aa=( ${PMAKE_ARGS_AA_FOR_SH} ) ; 				\
	declare -A env_var_name_aa=( ${ENV_VAR_NAME_AA_FOR_SH} ) ; 			\
	declare -A env_var_val_aa=( ${ENV_VAR_VAL_AA_FOR_SH} ) ; 			\
	declare -A logfile_aa=( ${LOGFILE_AA_FOR_SH} ) ; 					\
	for testname in ${TESTLIST} ; 										\
		do 																\
		mkdir -p $$testname.artifactdir || ( echo "unable to create $$testname.artifactdir" >> ./${LOGFILE} ; exit $$? ; ) ; 	\
		# Set env vars so that the pmake makefile can see what the values														\
		#	from the command line are supposed to be.																			\
		export ENV_PMAKE_CMD_LINE_VAR_NAME=$${env_var_name_aa[$$testname]} ;													\
		export ENV_PMAKE_CMD_LINE_VAR_VAL=$${env_var_val_aa[$$testname]} ;														\
		${PMAKE_PATH} $${pmake_args_aa[$$testname]} >> $${logfile_aa[$$testname]} ; 											\
		if [ $$? -ne 0 ] ; 																										\
			then 																												\
			# stdout must go into logfile,  not test.failed. test.failed and test.passed are only								\
			# created in the check target.																						\
			echo "error (GNU make): setting_variable_from_command_line test failed with nonzero exit code" >> $${logfile_aa[$$testname]} ; 		\
		else																																	\
			echo "(GNU make) pmake exited with a zero exit status. yay" >> $${logfile_aa[$$testname]} ; 										\
			fi ;																																\
		done ;


# TODO: Need to handle "expected errors".  That is,  there is a class of
#		tests were we want to check that an error was detected and reported.
#		"reported" can mean: 1) that the exit code was non-zero  2) that
#		the word "error" should appear in the log file.
check :
	@echo "$$PWD: making \"$@\"" ;
	@rm -f test.passed test.failed ;
	@for testdir in ${TESTDIRS}; 										\
		do																\
		if [ ! -e $$testdir/Makefile ] ;								\
			then														\
			echo "ERROR: no Makefile in $$testdir." >> test.failed;		\
			fi ;														\
		make -C $$testdir $@ ;											\
		if [ $$? -ne 0 ] ;                                              			\
			then                                                            		\
			echo "'make -C $$testdir $@' exited with nonzero exit status" >> test.failed ;	\
			fi ;																			\
		if [ -e $$testdir/test.failed ] ;										\
			then																\
			echo "ERROR: test.failed exists in $$testdir." >> test.failed;		\
			cat $$testdir/test.failed >> test.failed ;							\
			fi ;																\
		if [ ! -e ./test.failed ] ;												\
			then																\
			if [ -e $$testdir/test.passed ] ;									\
				then															\
				echo "test.passed exists in $$testdir" >> test.passed ;			\
				cat $$testdir/test.passed >> test.passed ;						\
				fi ;															\
			fi;																	\
		done;
	@for testname in ${TESTLIST} ; 																							\
		do 																													\
		# Go through each of testname artifact dirs looking for errors 														\
		#	in the logfile 																									\
		artifactdir=$${testname}.artifactdir ; 																				\
		if [ ! -e $${artifactdir} ; 																						\
			then 																											\
			echo "error: $${artifactdir} not found" >> test.failed; 														\
		else  																												\
			rm -f test.passed test.failed ; 																				\
			pushd $${artifactdir} ; 																						\
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
			if ! [ -e test.failed ] ;																						\
				then																										\
				echo "PASSED: (GNU_MAKE): $${bn}" >> test.passed ;															\
				fi; 																										\
			popd ; 																											\
			fi ; 																											\
		done ;
	@for testname in ${TESTLIST} ; 																							\
		do 																													\
		# Look for test.failed files (test.passed files) in each of the 													\
		# artifact dirs and sum up the failures and put them in test.failed/test.passed 									\
		artifactdir=$${testname}.artifactdir ; 																				\
		if [ -e $$artifactdir/test.failed ] ;																				\
			then																											\
			echo "$$artifactdir/test.failed exists." >> test.failed;														\
			cat $$artifactdir/test.failed >> test.failed ;																	\
			fi;																												\
		if [ -e $$artifactdir/test.passed ] ;																				\
			then																											\
			if [ -e $$artifactdir/test.failed ] ;																			\
				then																										\
				echo "both $$artifactdir/test.failed exists AND $$artifactdir/test.passed exists." >> test.failed;			\
				cat $$artifactdir/test.failed >> test.failed ;																\
			else 																											\
				echo "$$PWD/$$artifactdir/test.passed exists." >> test.passed;												\
				fi; 																										\
			fi;																												\
		if [ ! -e $$artifactdir/test.failed ] ;																				\
			then																											\
			if [ ! -e $$artifactdir/test.passed ] ;																			\
				then																										\
				echo "neither $$PWD/$$artifactdir/test.failed nor test.passed exists." >> test.failed ; 					\
				fi ;																										\
			fi;																												\
		done ;


check_old:
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
	if ! [ -e test.failed ] ;																						\
		then																										\
		echo "PASSED: (GNU_MAKE): $${bn}" >> test.passed ;															\
		fi;

clean:
	rm -f test.passed test.failed ${LOGFILE} 
	rm -rf *.artifactdir

# Cleans local artifacts and the install location
clean_all:



