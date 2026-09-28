ValaQuenta
==========

**The derivation engine.** Pure mathematics. Runnable code. No physical
substrate required. Licensed GPL-3.0-only.

ValaQuenta is a Python package of exact mathematical engines. Each engine is a
module you can import and call, and each is also a plugin of the ValaQuenta
Format that the derivation browser lists and runs.

.. code-block:: python

   >>> from ValaQuenta.noether import NoetherCurrents
   >>> NoetherCurrents().forced_sigma(1000.0, sigma_0=-3.0)   # any E, any σ₀
   0.5

Install and the quick start are in the
`README <https://github.com/michaelrendier/ValaQuenta#readme>`_.

.. toctree::
   :maxdepth: 2
   :caption: Reference

   conventions
   api/index
   listings
   locations

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
