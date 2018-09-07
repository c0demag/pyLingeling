import os
from setuptools import setup
from distutils.extension import Extension
from datetime import datetime

LINGELING_VERSION='160707'
LINGELING_DIR='lingeling'

PYLINGELING_MINOR_VERSION='%s' % datetime.utcnow().strftime("%y%m%d%H%M")
# Major number is Picosat Version, minor number creation date of the bindings
PYLINGELING_VERSION='%s.%s' % (LINGELING_VERSION, PYLINGELING_MINOR_VERSION)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build from SWIG definition
lingeling_ext = Extension('_lingeling',
                        [os.path.join(BASE_DIR, 'lingeling_python.i')],
                        swig_opts=['-I%s' % os.path.join(BASE_DIR, LINGELING_DIR)],
                        include_dirs=[LINGELING_DIR],
                        library_dirs=[LINGELING_DIR],
                        libraries=['lgl'],
                        language='c',
                    )


short_description="Lingeling SAT-Solver Wrapper"
long_description=\
"""
============================
Lingeling SAT-Solver Wrapper
============================

pyLingeling provides a basic wrapping around the efficient Lingeling SAT-Solver.

To build this wrapper you need SWIG to be installed.

Lingeling is developed by Armin Biere, for more information: http://fmv.jku.at/lingeling/
"""

setup(name='pyLingeling',
      version=PYLINGELING_VERSION,
      author='Pramod Subramanyan',
      author_email='pramod.subramanyan@gmail.com',
      url='https://github.com/pramodsu/pyLingeling/',
      license='BSD',
      description=short_description,
      long_description=long_description,
      ext_modules=[lingeling_ext],
      py_modules=['lingeling', 'solver'],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
  )
