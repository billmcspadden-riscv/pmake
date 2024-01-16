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
    echo "building ${TARGET}" | tee logfile    # echo with output redirection
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
    echo("building " + rule.target, ">>", "logfile")    # echo with output redirection
    os,system(CC + " " + CCFLAGS + " " + rule.prerequisites + " " + " -o" + rule.target)

Rule("%.o", "%.c", c_compile__recipe)

```

The main hook in this methodology, is the python 

The main goals of pmake are:

1. Exclusivelyu use python in the make specification file (usually referred to as "the makefile").
1. Follow the "target - prerequistes - recipe" pattern that most versions of make use.
1. Support common functions and variables used by GNU make so that learning how to 
write a pmake makefile (usually named 'Makefile.py') is not too ornerous.  For example,
the GNU make function, `$(patsubst pattern,replacement,text)` is reimplemented as a python
function, `patsubst(pattern, replacement, text)`.  We
hope that simple GNU makefiles can easily be ported to pmake.)
1. Support pattern matching semantics in Rules
1. Inclusion of other Makefiles (for common code and for hierarchical makefiles)

## Replicated features of GNU make (strengths of GNU make)

The main benefit of make (in the author's perspective), is the target-prerequisites-recipe
semantic.  The construction of targets are self-documenting.  And if rules
are written correctly, the target will always be correctly built whenever
any of the prerequisites change. 

This pattern has been used for decades and is a proven method for building projects.

The ability to include other makefiles enables code re-use, hierarchical build
processes ...  MORE TEXT HERE

When using make variables,  strings are known by the context.  Such is not the
case in python.  Strings must be quoted.  There is no clean way around this.
There will be lots of quotes in the Makefile.py file.



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

Lack of data structures.  In order to have some support of larger data 
structures,  one needs to use a library. The GNU Makse Standard Library 
is one such library,  but its usage is a bit difficult.  We do not intend to
replicate the GMSL functionality in this project.  Use the native python structures
to build useful higher-level structures.  (This is the purpose of this
project, after all.)

Backslashitis.  Anyone who has written a recipe for a GNU make rule,  knows
the pain of having to use backslashes for line continuation in the recipe. 
Recipes in GNU make are one long bash command line.  To make them readable,
a backslash + newline is used.  But this leads to numerous problems.  First,
if you have something,  even a space, after the backslash,  you get a bash syntax
error.  And the error is seldom obvious.  bash line numbers (in the bash error 
message) for the recipe are meaningless since the bash command is just one
long line.  Second, and more tedious,  it's hard
to keep the backslashes from looking ragged.  Third,  it's easy to forget a 
backslash, which may or may not lead to a syntax error,  but is almost always a 
functional error.

A nice feature of Gnu make,  is that the recipe sits as part of the target-prereqs-recipe
construct.  I cannot figure out how to replicate this in python. So,  we use a python
function as the recipe (which takes as a parameter, a pointer to the calling class thereby
giving you access to the piec:w
es needed for running the recipe).  Also,  the recipe function
definition must exist before the instantiation of the Rule.  Well, that's not quite
true;  there is a method for forward declaring the function,  but adding that line of code
is not much better than defining the (usually short) function ahead of the Rule instance.


## Testing pmake and the `TEST_DIR_ROOT/` directory

See TESTING.md

## Coding Style

See CODING_STYLE.md

## Overall flow

