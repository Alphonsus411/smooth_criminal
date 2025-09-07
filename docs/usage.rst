Uso
===

Instalación básica::

   pip install smooth-criminal

Ejemplo rápido:

.. code-block:: python

   from smooth_criminal import smooth

   @smooth
   def mi_funcion(x):
       return x * 2


Ejemplos
--------

Para probar las demos instala las dependencias adicionales::

   pip install -e . -r examples/requirements.txt

Luego ejecuta la aplicación de Streamlit::

   streamlit run examples/benchmark_streamlit.py

Ejecución en línea
------------------

Sin instalar nada puedes abrir el ejemplo en Binder:

.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Alphonsus411/smooth_criminal/HEAD?urlpath=streamlit/examples/benchmark_streamlit.py
   :alt: Binder

Si prefieres Streamlit Cloud, visita: https://smooth-criminal-demo.streamlit.app
