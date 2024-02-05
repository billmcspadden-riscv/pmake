#! /usr/bin/env python3

s = "a b"
s_ret = addprefix("foo/", s)

# 'addprefix()' outside of a Rule
l       = s.split()
l_ret   = s_ret.split()
print("l_ret: ", str(l_ret))

for i in range(0, len(l)) :
    if l_ret[i] != "foo/" + l[i] :
        echo("error: addprefix incorrect.  expected: 'foo/" + l[i] + "' received: '" + l_ret[i] + "'")
        sys.exit(1)
    else :
        pass

Path('./test.passed').touch()

def dummy(t) :
    return 0

Rule("default", [], dummy, PHONY)

def addprefix_in_a_Rule__recipe(t) :
    s = "aa bb"
    l = s.split()
    s_ret = addprefix("goo/", s)
    l_ret = s_ret.split()
    for i in range(0, len(l)) :
        if l_ret[i] != "goo/" + l[i] :
            echo("error: addprefix incorrect().  expected: 'goo/" + l[i] + "' received: '" + l_ret[i] + "'")
            return 1
        else :
            pass
    return 0

Rule(
    "addprefix_in_a_Rule", 
    [], 
    addprefix_in_a_Rule__recipe, 
    PHONY,
    "check addprefix() functionality within a recipe"
    )


