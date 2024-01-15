#! /usr/bin/env python3



def run__recipe(t) :
    # If we are in this directory and exiting this recipe,  then
    #   the test passed
    echo("building target, " + t.target, ">>", "test.passed")
    sys.exit(0)
    
Rule(
    "run",                      # target
    [],                         # prerequisites
    run__recipe,                # recipe
    PHONY,                      # is target phony or not
    "check if -C/--directory switch(es) worked"     # target descr
    )


