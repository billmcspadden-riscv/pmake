#! /usr/bin/env python3

# Recipes should return 0 for pass, non-zero for failure, just
#   like bash commands

CC = "gcc"
CCFLAGS = " -c -g -O3"
LD = "gcc"

Rule("build", [ "hello" ], phony = True)

def run__recipe(t) :
    if os.path.isfile("hello") == False :
        echo("error: executable, 'hello', does not exist")
        return 1
    else :
        ret = os.system("./hello")
        if ret != 0 :
            echo("error: executable, 'hello', exited with non-zero error code: " + str(ret))
            return ret
        else :
            return 0


Rule("run", [ "build" ], run__recipe, phony = True)

def ld__recipe(t) :
    echo("building " + t.target)
    cmd = LD + " -o " + t.target + " " + ' '.join(t.prerequisites) 
    echo("cmd: " + cmd)
    return os.system(cmd)

Rule("hello", ["hello.o", "a.o", "b.o"], ld__recipe)


def cc__recipe(t) :
    echo("building " + t.target)
    cmd = CC + CCFLAGS + " -o " + t.target + " " + ' '.join(t.prerequisites)
    echo("cmd: " + cmd)
    return os.system(cmd)


# The following individual rules ....

#Rule("hello.o", [ "hello.c" ], cc__recipe)
#Rule("a.o", [ "a.c" ], cc__recipe)
#Rule("b.o", [ "b.c" ], cc__recipe)

# ... get replace with this one  pattern rule

Rule("%.o", [ "%.c" ], cc__recipe)

def clean__recipe(t) :
    return os.system("rm -f *.o hello")

Rule("clean", [], clean__recipe, phony = True)

def test__recipe(t) :
    echo ("building " + t.target)
    # TODO: Need to support MAKELEVEL and MAKEFILE_LIST as well
    #       Should these be handled by env vars rather than by command line?
    #       I don't like that the user, writing Makefile.py, has to support 
    #       these.
    cmd = MAKE + " -f Makefile.pattern_rule.py clean"
    echo ("executing: " + cmd)
    ret = os.system(cmd)
    if ret != 0 :
        return ret

    cmd = MAKE + " -f Makefile.pattern_rule.py build"
    echo ("executing: " + cmd)
    ret = os.system(cmd)
    if ret != 0 :
        return ret

    cmd = MAKE + " -f Makefile.pattern_rule.py run"
    echo ("executing: " + cmd)
    ret = os.system(cmd)
    if ret != 0 :
        return ret
    return 0

Rule("test", [], test__recipe, phony = True)

