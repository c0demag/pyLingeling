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
def lingeling_set_output(picosat, fileout):
    lingeling_set_output_fd(picosat, fileout.fileno())

%}
