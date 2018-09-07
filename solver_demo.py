from __future__ import print_function

import lingeling

def test1():
    S = lingeling.Solver()

    # create variables
    x = S.newVar()
    y = S.newVar()

    S.freeze(x)
    S.freeze(y)

    # add clauses to instance.
    # these clauses encode x XOR y
    S.addClause(-x, -y)
    S.addClause(x, y)

    # Solve with assumption x = 0. Should be SAT.
    r1 = S.solve(-x)
    assert r1 == 1
    print ('RESULT:', ('SAT' if r1 else 'UNSAT'))
    print ('x = %d; y = %d' % (S.modelValue(x), S.modelValue(y)))
    print

    # Let's try again, this time setting y = 0. Should be SAT again.
    r2 = S.solve(-y)
    assert r2 == 1
    print ('RESULT:', ('SAT' if r2 else 'UNSAT'))
    print ('x = %d; y = %d' % (S.modelValue(x), S.modelValue(y)))
    print

    # Solve with assumption x = y = 0. Should be UNSAT.
    r3 = S.solve(-x, -y)
    assert r3 == 0
    # print (S.modelValue(x))
    print ('RESULT:', ('SAT' if r3 else 'UNSAT'))


if __name__ == '__main__':
    test1()
