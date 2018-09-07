/* -*- swig -*- */
/* SWIG interface file to create the Python API for Lingeling */
/* author: Pramod Subramanyan <pramod.subramanyan@gmail.com> */
/* Heavily based on the pyPicoSAT version written
   by Andrea Micheli <micheli.andrea@gmail.com> */

%include "typemaps.i"

/***************************************************************************/

/* EXTRA_SWIG_CODE_TAG */


/* %typemap(in) FILE * { */
/* %#if PY_VERSION_HEX < 0x03000000 */
/*   if (!PyFile_Check($input)) { */
/*       PyErr_SetString(PyExc_TypeError, "Need a file!"); */
/*       goto fail; */
/*   } */
/*   $1 = PyFile_AsFile($input); */
/* %#else */
/*   int fd = PyObject_AsFileDescriptor($input); */
/*   $1 = fdopen(fd, "w"); */
/* %#endif */
/* } */



%ignore lglsetout ;

%module lingeling
%{
#include "lglib.h"
/* EXTRA_C_INCLUDE_TAG */
%}

%include "lglib.h"
/* EXTRA_SWIG_INCLUDE_TAG */

%{

/* EXTRA_C_STATIC_CODE_TAG */

%}


%inline %{

/* EXTRA_C_INLINE_CODE_TAG */
static FILE* lingeling_set_output_fd(LGL* self, int fd) {
    FILE* fout = fdopen(fd, "w");
    lglsetout(self, fout);
    return fout;
}

static void lingeling_flushout(FILE* fout) {
    fflush(fout);
}

%}


%pythoncode %{

## EXTRA_PYTHON_CODE_TAG
import tempfile
import time

def lingeling_set_output(picosat, fileout):
    lingeling_set_output_fd(picosat, fileout.fileno())

class Solver(object):
    def __init__(self):
        "Create a solver object."
        self.p = lglinit()
        self.last_sat_result = None
        self.solver_time = 0.0

    def __del__(self):
        "Destroy this solver object."
        lglrelease(self.p)

    def newVar(self):
        "Return a new variable."
        return lglincvar(self.p)

    def addClause(self, *ls):
        "Add this clause to the solver."
        assert len(ls) > 0
        for l in ls:
            lgladd(self.p, l)
        lgladd(self.p, 0)

    def solve(self, *ls):
        "Check satisfiability under the given assumptions."
        t1 = time.time()
        for l in ls:
            lglassume(self.p, l)
        r = lglsat(self.p)
        t2 = time.time()
        self.solver_time += (t2 - t1)
        if r == LGL_SATISFIABLE:
            self.last_sat_result = True
            return True
        elif r == LGL_UNSATISFIABLE:
            self.last_sat_result = False
            return False
        else:
            self.last_sat_result = None
            raise TimeoutError("Lingeling returned unknown.")

    def modelValue(self, l, default=None):
        if self.last_sat_result is not None and not self.last_sat_result:
            raise RuntimeError('modelValue can only be invoked when solve returns SAT.')
        v = lglderef(self.p, l)
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
        lglfreeze(self.p, l)

%}
