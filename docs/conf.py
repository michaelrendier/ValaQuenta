# Sphinx build configuration for ValaQuenta.
# Docstring standard: reStructuredText field lists, consumed natively by
# sphinx.ext.autodoc. No napoleon -- Google/NumPy styles are NOT the standard
# here. See ~/.clauderc_memory, DOCSTRINGS INSTRUCT FUNCTION.
import os, sys
sys.path.insert(0, os.path.abspath('../..'))

project   = 'ValaQuenta'
author    = 'Cody Michael Allison'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]
autodoc_member_order   = 'bysource'
autodoc_typehints      = 'description'
intersphinx_mapping    = {'python': ('https://docs.python.org/3', None),
                          'numpy':  ('https://numpy.org/doc/stable/', None)}
html_theme = 'alabaster'
nitpicky   = False
exclude_patterns = ['_build', 'gen_api.py', 'gen_listings.py']
autodoc_mock_imports = ['PyQt5', 'vispy', 'sounddevice', 'qtermwidget']
release = version = '0.159'
