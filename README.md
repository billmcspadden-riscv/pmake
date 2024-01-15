# pmake
make replacement using python

'pmake' is intended as a simple replacement tool for GNU make. It uses GNU make
as a pattern for a build tool.  GNU make has been used for decades but
it has its limitations.

As far as possible,  the documentation and nomenclature used in describing
this tool follows the nomenclature used in the GNU manual, "GNU Make",  by
Stallman, McGrath and Smith.

An example GNU Makefile looks something like this:

```
C_SRC       := $(wildcard *.c)
C_OBJS      := $(patsubst %.c,%.o,${C_SRC} )
TARGET      := hello
CC          := gcc
CCFLAGS     := -O3 -g
LD          := ${CC}

${TARGET} : ${C_OBJS}
    ${LD} -o $@ ${C_OBJS}

%.o : %.c
    ${CC} ${CFLAGS} $< -o $@

```

An equivalent pmake Makefile looks something like this:

```
C_SRC       = wildcard('*.c')
C_OBJS      = patsubst('%.c', '%.o', C_SRC)
TARGET      = "hello"
CC          = "gcc"
CCFLAGS     = "-O3 -g"
LD          = CC

def target__recipe(rule) :
    os.system(LD + "-o " + rule.target + C_OBJS)

Rule(
    TARGET,
    C_OBJS,
    target__recipe(self),
    PHONY,
    "description of target.  optional.  for documentation purposes"
    )

def c_compile__recipe(rule) :
    echo("building " + rule.target, ">>", "logfile")
    os,system(CC + " " + CCFLAGS + " " + rule.prerequisites + " " + " -o" + rule.target)

Rule("%.o", "%.c", c_compile__recipe)

```

The main hook in this methodology, is the python 

The main goals of pmake are:

1. Exclusivelyu use python in the make specification file (usually referred to as "the makefile").
1. Follow the "target - prerequistes - recipe" pattern that most versions of make use.
1. Support common functions and variables used by GNU make so that learning how to 
write a pmake makefile (usually named 'Makefile.py') is not too ornerous.  For example,
the GNU make function, `$patsubst(pattern,replacement,text)` is reimplemented as a python
function, `patsubst(pattern, replacement, text)`.  We
hope that simple GNU makefiles can easily be ported to pmake.)
1. Support pattern matching semantics in Rules
1. Inclusion of other Makefiles (for common code and for hierarchical makefiles)

## Replicated features of GNU make


## Non-replicated features of GNU make  (weaknesses of GNU make)

One of the more confusing aspects of GNU make, is that there are two types of
variables that are supported:

- "recursively expanded variables" of the sort: `FOO = hello.c`
- "simply expanded variables" of the sort: `FOO := hello.c`
- `$@`, `$<` and other automatic variables are not directly supported as python's
naming convention does not allow these as variable names.

Make variables (as opposed to shell variables, used in recipes) and make functions,
are typically used when building target and prerequisite names.  These names are
then used in the `<target> : <orerequisite>` portion of a Rule.  However, using the 
make variable name in a recipe is problematic.  Expansion of the make variable 
within a recipe is prone to error.

Lack of data structures.
