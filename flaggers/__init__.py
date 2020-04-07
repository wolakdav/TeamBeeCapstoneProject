import importlib
from os.path import dirname, basename, isfile, join
from glob import glob

_dont_import = ['__init__.py', 'boilerplate.py']

# Finds all *.py files in current directory except specified.
# Note that this also includes flagger.py
_modules = glob(join(dirname(__file__), '*.py'))
_modules = ['.' + basename(f)[:-3] for f in _modules 
            if not list(filter(f.endswith, _dont_import))]
# Import them. Order doesn't matter.
for m in _modules:
  importlib.import_module(m, 'flaggers')
