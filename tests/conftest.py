import os
# Previously ignored due to a typo in the file name. The
# test file has been renamed correctly so we no longer
# need to skip it during collection.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import asyncio
import numpy as np
import pytest


@pytest.fixture
def failing_func():
    """Función sincrónica que siempre lanza un ValueError."""
    def _func(*args, **kwargs):
        raise ValueError("boom")

    return _func


@pytest.fixture
def failing_async_func():
    """Función asíncrona que siempre lanza un ValueError."""
    async def _func(*args, **kwargs):
        raise ValueError("boom")

    return _func


@pytest.fixture
def simple_array():
    """Pequeño arreglo NumPy para pruebas."""
    return np.array([1.0, 2.0, 3.0], dtype=np.float64)


@pytest.fixture
def numbers():
    """Lista sencilla de enteros para reutilizar en varias pruebas."""
    return [1, 2, 3, 4, 5]

