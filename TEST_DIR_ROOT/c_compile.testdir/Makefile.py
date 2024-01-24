#! /usr/bin/env python3


CC = "gcc"
CCFLAGS = " -c -g -O3"
LD = "gcc"


def cc__recipe(t) :
    echo("building " + t.target)
    cmd = CC + CCFLAGS + " -o " + t.target + " " + ' '.join(t.prerequisites)
    echo("cmd: " + cmd)
    os.system(cmd)

Rule("hello.o", [ "hello.c" ], cc__recipe)

def clean__recipe(t) :
    os.system("rm -f *.o hello")

Rule("clean", [], clean__recipe)



