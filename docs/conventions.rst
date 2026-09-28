Conventions
===========

Docstrings
----------

Docstrings are reStructuredText field lists, read by ``sphinx.ext.autodoc``:

.. code-block:: python

   def forced_sigma(self, E: float, sigma_0: float = 0.0) -> float:
       """Return the σ at which the two currents meet.

       :param E: energy scale; any real value, 0 included
       :param sigma_0: starting position of σ; any real value
       :returns: 0.5, exactly
       """

Types come from the annotations (``autodoc_typehints = 'description'``), so the
field lists do not repeat them. A docstring tells the caller what to do; it does
not record history. The history of a result lives in the wiki.

Confidence tiers
----------------

Every registry equation carries one, strongest first: ``ESTABLISHED``,
``THEORETICAL``, ``CONJECTURE``, ``OPEN``. A tier is a claim about the
mathematics, not about the code: the code runs at every tier.

Registry modules
----------------

A registry module is a directory ``modules/<name>/`` with ``maths.py`` (the
mathematics as plain functions), ``tools.py`` (an ``EquationModule`` subclass that
publishes them as a formulary), and ``manifest.json`` (provenance and UI
registration). See :mod:`ValaQuenta.engine.registry` for the six steps to add one.

Arithmetic
----------

``fractions.Fraction`` is exact where the mathematics is exact. Floats appear
only at an output boundary.
