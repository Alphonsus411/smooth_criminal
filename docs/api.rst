API
===

.. automodule:: smooth_criminal.core
   :members:

Ejemplo ``mj_mode``
-------------------

El decorador :func:`smooth_criminal.core.mj_mode` elige aleatoriamente uno de
los otros decoradores y muestra un mensaje inspirado en Michael Jackson.

.. code-block:: python

   >>> import random, logging
   >>> from smooth_criminal import mj_mode
   >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
   >>> random.seed(0)
   >>> @mj_mode
   ... def identidad(x):
   ...     return x
   >>> identidad([1, 2])
   [1, 2]  # Posible salida: "🥁 Jam session with 4 workers!"

.. automodule:: smooth_criminal.benchmark
   :members:

.. automodule:: smooth_criminal.memory
   :members:

