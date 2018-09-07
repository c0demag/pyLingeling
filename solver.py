from __future__ import print_function

import lingeling
import tempfile
import time

class Solver(object):
    def __init__(self, log=None):
        "Create a solver object."
        self.p = lingeling.lglinit()
        self.last_sat_result = None
        self.solver_time = 0.0

    def newVar(self):
        "Return a new variable."
        return lingeling.lglincvar(self.p)

    def addClause(self, *ls):
        "Add this clause to the solver."
        assert len(ls) > 0
        for l in ls:
            lingeling.lgladd(self.p, l)
        lingeling.lgladd(self.p, 0)

    def solve(self, *ls):
        "Check satisfiability under the given assumptions."
        t1 = time.time()
        for l in ls:
            lingeling.lglassume(self.p, l)
        r = lingeling.lglsat(self.p)
        t2 = time.time()
        self.solver_time += (t2 - t1)
        if r == lingeling.LGL_SATISFIABLE:
            self.last_sat_result = True
            return True
        elif r == lingeling.LGL_UNSATISFIABLE:
            self.last_sat_result = False
            return False
        else:
            self.last_sat_result = None
            raise TimeoutError("Lingeling returned unknown.")

    def modelValue(self, l, default=None):
        if self.last_sat_result is not None and not self.last_sat_result:
            raise RuntimeError('modelValue can only be invoked when solve returns SAT.')
        v = lingeling.lglderef(self.p, l)
        if v == 1:
            return True
        elif v == -1:
            return False
        else:
            if default is None:
                raise ValueError("No assignment for literal: %d" % l)
            else:
                return default

    def freeze(self, l):
        lingeling.lglfreeze(self.p, l)

def test1():
    S = Solver()

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
