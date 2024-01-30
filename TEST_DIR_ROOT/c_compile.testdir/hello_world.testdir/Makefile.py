#! /usr/bin/env python3


CC = "gcc"
CCFLAGS = " -c -g -O3"
LD = "gcc"

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

Rule("hello.o", [ "hello.c" ], cc__recipe)

Rule("a.o", [ "a.c" ], cc__recipe)
Rule("b.o", [ "b.c" ], cc__recipe)

def clean__recipe(t) :
    return os.system("rm -f *.o hello")

Rule("clean", [], clean__recipe)



