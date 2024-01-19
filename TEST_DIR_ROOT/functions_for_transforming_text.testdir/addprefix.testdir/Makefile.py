#! /usr/bin/env python3

l = [ "a", "b" ]
l_ret = addprefix("foo/", l)

print("l_ret: ", str(l_ret))

# 'addprefix()' outside of a Rule
for i in range(0, len(l)) :
    if l_ret[i] != "foo/" + l[i] :
        echo("error: addprefix incorrect.  expected: 'foo/" + l[i] + "' received: '" + l_ret[i] + "'")
        sys.exit(1)
    else :
        pass

Path('./test.passed').touch()

def dummy(t) :
    True

Rule("default", [], dummy, PHONY)

def addprefix_in_a_Rule__recipe(t) :
    l = [ "aa", "bb" ]
    l_ret = addprefix("goo/", l)
    for i in range(0, len(l)) :
        if l_ret[i] != "goo/" + l[i] :
            echo("error: addprefix incorrect().  expected: 'goo/" + l[i] + "' received: '" + l_ret[i] + "'")
            sys.exit(1)
        else :
            pass

Rule(
    "addprefix_in_a_Rule", 
    [], 
    addprefix_in_a_Rule__recipe, 
    PHONY,
    "check addprefix() functionality within a recipe"
    )


