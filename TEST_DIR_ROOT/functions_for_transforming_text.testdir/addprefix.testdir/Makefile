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
include ./Makefile.header
include ${TEST_DIR_PATH}/lib/pmake/Makefile.common.top

# ===========================================================================
# Test
PMAKE_MAKEFILE					:= Makefile.py
PMAKE_ARGS						:= -f ${PMAKE_MAKEFILE}
TARGET							:= 
PMAKE_ARGS						+= ${TARGET}
ENV_PMAKE_CMD_LINE_VAR_NAME		:= 
ENV_PMAKE_CMD_LINE_VAR_VAL 		:= 
PMAKE_ARGS						+= 

TESTLIST	:= $(call add_test,${PMAKE_ARGS},${ENV_PMAKE_CMD_LINE_VAR_NAME},${ENV_PMAKE_CMD_LINE_VAR_VAL},${TESTLIST})

## ===========================================================================
# Test
PMAKE_MAKEFILE					:= Makefile.py
PMAKE_ARGS						:= -f ${PMAKE_MAKEFILE}
TARGET							:= addprefix_in_a_Rule
PMAKE_ARGS						+= ${TARGET}
ENV_PMAKE_CMD_LINE_VAR_NAME		:= 
ENV_PMAKE_CMD_LINE_VAR_VAL 		:= 
PMAKE_ARGS						+= 

TESTLIST	:= $(call add_test,${PMAKE_ARGS},${ENV_PMAKE_CMD_LINE_VAR_NAME},${ENV_PMAKE_CMD_LINE_VAR_VAL},${TESTLIST})

include ${TEST_DIR_PATH}/lib/pmake/Makefile.common.bottom

