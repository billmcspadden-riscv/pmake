#! /usr/bin/env python3
# vim: set tabstop=4 shiftwidth=4 expandtab set textwidth=79
# ===========================================================================79
# Filename:     pmake.py
#
# Description:  Python script used as a replacement for GNU make
#
#               GNU Makefiles are replaceed with native python script fragments
#               using the classes, functions, variables and semantics found in
#               this file.
#
#               High level flow:
#                   pmake.py -f <makefile.py>    plus other switches
#                       process command line arguments
#                       process makefile(s) using exec() calls
#                       invoke make
#                           build list of targets
#                               expand "%" targets/prereq into individual targets
#                               build interconnection graph of targets
#                               build build-list
#                           run the build
#                       cleanup and exit
#                       
#
#
# Author(s):    Bill McSpadden (bill@riscv.org)
#
# History:      See revision control log
# ===========================================================================79





#============================================================================79
# Names already in use:  pymake, pmake, makepy
#   TODO: need to find another name for this toolsuite

import os               # needed for os command interactions
import glob             # needed for file list gathering useing wildcards
import re               # regular expression
import sys              # needed for command line arguments
import getopt           # needed for command line arguments
import collections      # needed for dequeues
from pathlib import Path
from inspect import currentframe, getframeinfo
from abc import ABC, abstractmethod

# Usage:  pymake [-d] [-f <makefile.py>] [target ...] [-D<var>[=<val]]
#   -d              turn on debugging (equivalent to --debug all)
#   -f              use <makefile.py>.  if none listed, use ./pymakefile.py
#   -D<var>[=val]   define pymake variable; set pymake variable to val
#   <target>        if none listed, default is first target in pymmakefile

# User controlled debug trace statement for debut of pmake
#   makefiles.
def TRACE(text = "") :
    cf = currentframe()
    of = cf.f_back
    fi = getframeinfo(of)
    filename = fi.filename
    print("TRACE: file: " + filename + " line: " + str(of.f_lineno) + " : " + text)
    return

def debug_basic(text) :
    if (_debug_basic) :
        print(text)

def debug_verbose(text) :
    if (_debug_verbose) :
        print(text)

def debug_implicit(text) :
    if (_debug_implicit) :
        print(text)

def _debug_jobs(text) :
    if (__debug_jobs) :
        print(text)

def _debug_makefile(text) :
    if (__debug_makefile) :
        print(text)

# ========================================================
# ========================================================
# Functions and definitions and data structures for pymake
# TODO: call the build/make process

#list_of_defined_targets     = list()    # List of "class Target"s
#PHONY                       = True
#targets_to_be_built         = list()    # List of strings,  which are the string names of the targets to be built
#TRACE("targets_to_be_built: " + str(targets_to_be_built))
#debug                       = ""
#build_order_dq              = list()    # The ordered list (dequeue) of targets to be built
#                                        #   for the targets_to_be_built
#list_of_variables_and_rules = list()    # List of include files
#
#list_of_default_makefiles   = ["makefile.py", "Makefile.py"]
#
#makefile_list               = []
#_debug_makefile             = False
#_debug_jobs                 = False
#_debug_implicit             = False
#_debug_verbose              = False
#_debug_basic                = False
#changedir                   = "./"

def get_target_class(target_name) :
    for target_class in list_of_defined_targets :
        if target_name == target_class.target :
            return target_class
        else :
            continue
    print("error: don't know how to make '" + target_name + "'. exiting")
    sys.exit(1)

def target_already_in_list(l, t) :
    for p in l :
        if p == t :
            return True
        else :
            return False
    TRACE("error: internal error")


# Recursive function
# TODO: check for infinite loop
def construct_build_list(ttb_list) :
    print("ttb_list: " + str(ttb_list))
    for ttb in ttb_list :
        target_class = get_target_class(ttb)
        print("target_class.target: " + target_class.target)
        print("target_class.prerequisites: " + str(target_class.prerequisites))
        for prereq in target_class.prerequisites :
            # check to see if the prereq has already appeared in the list
            # TODO:  need to check for circular dependencies
            if target_already_in_list(ttb_list, prereq) :
                continue
            # prereq was not found.  add to list
            ttb_list.append(prereq)
            TRACE("ttb_list before call to construct_build_list(): " + str(ttb_list))
            ttb_list = construct_build_list(ttb_list)
            TRACE("ttb_list after call to construct_build_list(): " + str(ttb_list))
            return(ttb_list)
    TRACE("")
    return(ttb_list)
            


# The main process for building the target(s)
# TODO: i kept getting errors when trying to access 'targets_to_be_built' as
#   a global variable.  something about "local variable, 'targets_to_be_built'
#   not set".  this only popped up after some code refactoring.  figure this
#   out!!!
def make(targets_to_be_built) :
    # Process command line arguments
    #print("list_of_defined_targets: " + str(list_of_defined_targets))
    if (len(targets_to_be_built) == 0) :
        # No targets passed on command line.  Default: Find first target in 
        #   list_of_defined_targets and put that into
        #   targets_to_be_built
        targets_to_be_built.append(list_of_defined_targets[0].target)

    print("targets_to_be_built: " + str(targets_to_be_built))
    # Process the list of targets to see what needs to be built
    #   and in which order.
    TRACE("targets_to_be_built: " + str(targets_to_be_built))
    targets_to_be_built = construct_build_list(targets_to_be_built)
    targets_to_be_built.reverse()
    TRACE("targets_to_be_built: " + str(targets_to_be_built))

    # Invoke the build recipe for targets

    target_found = False
    for ttb in targets_to_be_built :
        print("ttb: " + ttb)
        for t in list_of_defined_targets :
            print("t.target: " + t.target)
            if (ttb == t.target) :
                target_found = True
                t.recipe(t)
                break
        if target_found == False :
            print("error: target '" + str(ttb) + "' not specified")
        target_found = False

def echo(text, append_or_create = ">>", filename = "/dev/null") :
    match append_or_create :
        case ">>" :
            f = open(filename, "a")
            pass
        case ">" :
            f = open(filename, "w")
            pass
        case _ :
            
            pass

    f.write(text + "\n")
    sys.stdout.write(text + "\n")

# GNU make function, '$(info) always goes to stdout
def info(text) :
    echo(text, ">>", "/dev/null")



# ========================================================
# Functions that duplicate make functions.
def wildcard(s) :
    return glob.glob(s)

def patsubst(pattern, replacement, text) :
    l = list()
    m1 = re.match('(\S*)%(\S*)', pattern)
    m1g1 = m1.group(1)
    m1g2 = m1.group(2)

    m2 = re.match('(\S*)%(\S*)', replacement)
    m2g1 = m2.group(1)
    m2g2 = m2.group(2)

    for s in text :
        m3 = re.match(m1g1 + '(\S*)' + m1g2, s)
        m3g1 = m3.group(1)
        l.append(m2g1 + m3g1 + m2g2)

    return l

def addsuffix(suffix, name_list) :
    l = list()
    for name in name_list :
        l.append(name + suffix)
    return l

def addprefix(prefix, name_list) :
    l = list()
    for name in name_list :
        l.append(prefix + name)
    return l


# Functions that duplicate make functions.
# ========================================================

# ========================================================
# Classes

# Class: Rule
#   This is the basic class for pmake.  It is meant to emcompass what
#   a GNU Makefile rule is,  but in a Python class.  It contains a
#   target,  an optional list of prerequisites and a recipe (implemented
#   as a Python callback function).
class Rule:   # base class
    def dummy(self) :
        print("hello from dummy()")
        pass

    target = "Unnamed"
    prerequisites = { }
    phony = False 
    target_description = ""

    def __init__(self, target, prerequisites, recipe = dummy, phony = False, description = "") :
        self.target = target
        self.phony = phony
        #TODO: add to list of targets
        self.prerequisites = prerequisites
        self.recipe = recipe
        list_of_defined_targets.append(self)
        self.target_description = description

    def PHONY(self) :
        self.PHONY = True

    def print(self) :
        print("target: ", self.target)

# NOTE: using a function interface does not work in general.  The variables
#   in the included code, would all be local varables and would not be seen
#   by the make() function.  However,  in the included code,  one could mark
#   variables as 'global' and this would solve the problem.
def include(makefile) :
    TRACE("including (and exec()'ing) " + makefile + "...")
    if ( os.path.isfile(makefile) == False ) :
        TRACE("error: pmake makefile, " + makefile + "does not exist")
    else :
        exec(open(makefile).read())


# Functions and definitions and data structures for pymake
# TODO: call the build/make process
# ========================================================

def print_usage(invocation) :
    print(invocation + " usage: " + invocation + " [-h] [-u] [-f <makefile.py>]")
    print("    -h -u                     print out help/usage message")
    print("    -f, --makefile            use <makefile.py>. multiple -f switches may be given")
    print("                              if no  makefile is given, pmake looks for ./Makefile.py or ./makefile.py in that order")
    print("    -d                        turn on debugging.  equivalent to '--debug all'")
    print("    --debug [a|b|v|i|j|m|n]   turn on debugging level: all, basic, verbose, implicit, jobs, makefile")
    print("                              this is meant to loosely follow the GNU Make debug pattern")
    print("                              multiple --debug switches allowed")
    print("    -C/--directory <dir>      change to <dir> before searching and reading makefiles")
    print("    <var>=<val>               creates or overrides a pmake makefile variable named <var> and assigns it the value, <val>. ")

print("Starting up pmake ...")
list_of_defined_targets     = list()    # List of "class Target"s
PHONY                       = True
targets_to_be_built         = list()    # List of strings,  which are the string names of the targets to be built
debug                       = ""
build_order_dq              = list()    # The ordered list (dequeue) of targets to be built
                                        #   for the targets_to_be_built
list_of_variables_and_rules = list()    # List of include files

list_of_default_makefiles   = ["makefile.py", "Makefile.py"]

makefile_list               = []
_debug_makefile             = False
_debug_jobs                 = False
_debug_implicit             = False
_debug_verbose              = False
_debug_basic                = False
changedir                   = "./"
# Process command line arguments
# For the following code, I couldn't figure out how to
#   extract the target names from the command line.  They
#   are the extra arguments on the command line that are
#   not defined options.
#
#   All in all, it doesn't appear that getopt allows me to build
#   command line arguments that match GNU make,  and I really want
#   that.  I want the migration from GNU make to pmake to be as
#   straightforward as possible
#
#
#opts, args = getopt.getopt(sys.argv[1:], "huf:", ["makefile="])
#print("opts: " + str(opts))
#for opt, arg in opts :
#    if (opt == '-h') or (opt == '-u') :
#        print_usage(sys.argv[0])
#        sys.exit(0)
#    elif opt in ('-f', "--makefile") :
#        if os.path.isfile(arg) == False :
#            TRACE("error: makefile, " + arg + ", does not exist")
#            sys.exit(1)
#        else :
#            makefile_list.append(arg)
#    else :
#        # TODO:  fill out
#        targets_to_be_built.append(arg)

skip_next = False
for i in range(1, len(sys.argv)) :
    # TODO: skip_next is UGLY.  fix it
    if skip_next == True :
        skip_next = False
        continue
    arg = sys.argv[i]
#    TRACE("i: " + str(i) + " arg: " + arg)
    if (arg == '-h') or (arg == '-u') :
        print_usage(sys.argv[0])
        sys.exit(0)
    elif arg in ('-f', "--makefile") :
        arg_next = sys.argv[i+1]
        makefile_list.append(arg_next)
        skip_next = True

    elif arg in ('-d') :
        _debug_makefile = True
        _debug_jobs = True
        _debug_implicit = True
        _debug_verbose = True
        _debug_basic = True

    elif arg in ('--debug') :
        arg_next = sys.argv[i + 1]
        match arg_next :
            case "a" :
                _debug_makefile = True
                _debug_jobs = True
                _debug_implicit = True
                _debug_verbose = True
                _debug_basic = True
            case "b" :
                _debug_basic = True
            case "v" :
                _debug_verbose = True
            case "i" :
                _debug_implicit = True
                _debug_basic = True      # Per GNU make
            case "j" :
                _debug_jobs = True
            case "m" :
                _debug_makefile = True
            case "n" :
                _debug_makefile = False
                _debug_jobs = False
                _debug_implicit = False
                _debug_verbose = False
                _debug_basic = False
            case _ :
                TRACE("fatal error: illegal option to --debug: " + arg_next)
                sys.exit(1)
        skip_next = True

    elif arg in ('-C', '--directory') :
        TRACE("processing -C/--directory switch")
        arg_next = sys.argv[i + 1]
        if os.path.isdir(arg_next) == False :
            print("error: directory, " + arg_next + ", does not exist")
            sys.exit(1)
        changedir       = True
        changedir_dir   = arg_next
        skip_next       = True

    elif re.search('\S+=\S+', arg) != None :
        m = re.match('(\S+)=(\S+)', arg)
        TRACE( "setting up a variable from the command line: " + m.group(1) + " = " + m.group(2) )
        exec(m.group(1) + " = " + 'm.group(2)')


    else :
        # TODO:  fill out
        TRACE("adding '" + arg + "' to targets_to_be_built")
        targets_to_be_built.append(arg)


    

if len(makefile_list) == 0 :
    for f in list_of_default_makefiles :
        if os.path.isfile(f) == True :
            makefile_list.append(f)
            break
        else :
            continue
else :
    # do nothing
    pass
        
if len(makefile_list) == 0 :
    TRACE("error: no makefile specified or inferred")
    print_usage(sys.argv[0])
    # TODO: GNU make has default makefile rules.  We should
    #   replicate them. For now, we're exiting.
    sys.exit(1);
else :
    pass


for makefile in makefile_list :
# NOTE: using a function interface does not work in general.  The variables
#   in the included code, would all be local varables and would not be seen
#   by the make() function.  However,  in the included code,  one could mark
#   variables as 'global' and this would solve the problem.
#    include(makefile)
    if changedir == True :
        debug_verbose("changing to directory, " + changedir_dir)
        cwd_old = os.getcwd()
        os.chdir(changedir_dir)
        cwd_new = os.getcwd()
        if cwd_old == cwd_new :
            print("error: unable to chdir to " + changedir_dir + " old dir: " + cwd_old + " new dir: " + cwd_new)
            sys.exit(1)
        else :
            pass
    else :
        pass
    debug_verbose("executing makefile, " + makefile + " ...")
    if os.path.isfile(makefile) == False :
        print("error: makefile, " + makefile + ", does not exist")
        sys.exit(1)
    else :
        exec(open(makefile).read())

TRACE("targets_to_be_built before call to make(): " + str(targets_to_be_built))
make(targets_to_be_built)



