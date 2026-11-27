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


# The docstrings are written for a reader at a terminal, where |x| is an absolute value or a norm. In reST a bare pair of vertical bars is a
# substitution reference, so each bar outside an inline literal is escaped here, at build time, and the source stays readable as plain text.
import re as _re


def _escape_bars(app, what, name, obj, options, lines):
    """autodoc-process-docstring: escape ``|`` (outside ``double-backtick`` literals) so it is not read as a substitution reference."""
    for i, line in enumerate(lines):
        parts = _re.split(r'(``[^`]*``)', line)
        lines[i] = ''.join(p if p.startswith('``') and p.endswith('``') and len(p) > 3 else p.replace('\\|', '|').replace('|', '\\|') for p in parts)


def setup(app):
    app.connect('autodoc-process-docstring', _escape_bars)
