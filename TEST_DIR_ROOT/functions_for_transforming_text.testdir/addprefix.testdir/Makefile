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

# default is first target so that it is run if make is invoked with
#   no target name
default:
	@echo "supported Makefile targets:";
	@echo "   all";
	@echo "   build";
	@echo "   run";
	@echo "   test";
	@echo "   clean";
	@echo "   clean_all";

all:


build:


install:

run:
	../../../pmake.py -f ./Makefile.py ; 										\
	if [$$? -ne 0 ] ; 															\
		then 																	\
		echo "error (GNU make): addprefix test failed" >> ./test.failed ; 		\
		fi ;
	../../../pmake.py -f ./Makefile.py addprefix_in_a_Rule ;					\
	if [$$? -ne 0 ] ; 															\
		then 																	\
		echo "error (GNU make): addprefix test failed" >> ./test.failed ; 		\
		fi ;


clean:
	rm -f test.passed test.failed

# Cleans local artifacts and the install location
clean_all:



