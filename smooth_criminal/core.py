import statistics
from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

from numba import jit
import numpy as np
import asyncio
import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmoothCriminal")

def smooth(func):
    try:
        jit_func = jit(nopython=True, cache=True)(func)
        def wrapper(*args, **kwargs):
            logger.info("You've been hit by... a Smooth Criminal!")
            return jit_func(*args, **kwargs)
        return wrapper
    except Exception:
        def fallback(*args, **kwargs):
            logger.warning("Beat it! Numba failed. Falling back.")
            return func(*args, **kwargs)
        return fallback

def moonwalk(func):
    async def wrapper(*args, **kwargs):
        logger.info("Moonwalk complete — your async function is now gliding!")
        return await func(*args, **kwargs)
    return wrapper

def thriller(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("🎬 It’s close to midnight… benchmarking begins (Thriller Mode).")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"🧟 ‘Thriller’ just revealed a performance monster: {end - start:.6f} seconds.")
        return result
    return wrapper

def jam(workers=4):
    """
    Decorador que permite ejecutar funciones sobre listas en paralelo.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(args_list):
            logger.info(f"🎶 Don't stop 'til you get enough... workers! (x{workers})")
            results = []
            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_arg = {executor.submit(func, arg): arg for arg in args_list}
                for future in as_completed(future_to_arg):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"Worker failed on input {future_to_arg[future]}: {e}")
            return results
        return wrapper
    return decorator

def black_or_white(mode="auto"):
    """
    Optimiza tipos numéricos de arrays de entrada: float32/int32 o float64/int64.
    Modes:
        - "light": usa float32 / int32
        - "precise": usa float64 / int64
        - "auto": decide según el tamaño del array
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            converted_args = []
            for arg in args:
                if isinstance(arg, np.ndarray):
                    if mode == "light":
                        arg = _convert_to_light(arg)
                        logger.info("🌓 It's black or white! Using light types (float32/int32).")
                    elif mode == "precise":
                        arg = _convert_to_precise(arg)
                        logger.info("🌕 Going for precision! Using float64/int64.")
                    elif mode == "auto":
                        if arg.size > 1e6:
                            arg = _convert_to_light(arg)
                            logger.info("🌓 Auto mode: array is large, switching to float32/int32.")
                        else:
                            arg = _convert_to_precise(arg)
                            logger.info("🌕 Auto mode: small array, using float64/int64.")
                converted_args.append(arg)
            return func(*converted_args, **kwargs)
        return wrapper
    return decorator

def _convert_to_light(arr):
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.int32)
    elif np.issubdtype(arr.dtype, np.floating):
        return arr.astype(np.float32)
    return arr

def _convert_to_precise(arr):
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.int64)
    elif np.issubdtype(arr.dtype, np.floating):
        return arr.astype(np.float64)
    return arr

def beat_it(fallback_func=None):
    """
    Intenta ejecutar la función principal. Si falla, recurre al fallback.
    Si no se proporciona fallback, muestra un mensaje y lanza la excepción original.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning("🧥 Beat it! Something failed... Switching to fallback.")
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                else:
                    logger.error("No fallback provided. Rethrowing exception.")
                    raise e
        return wrapper
    return decorator

def bad(parallel=False):
    """
    Aplica optimizaciones agresivas con Numba (fastmath, parallel, cache).
    Usar con precaución: puede alterar precisión numérica o portabilidad.
    """
    def decorator(func):
        try:
            jit_func = jit(nopython=True, fastmath=True, cache=True, parallel=parallel)(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info("🕶 Who's bad? This function is. Activating aggressive optimizations.")
                return jit_func(*args, **kwargs)
            return wrapper
        except Exception as e:
            logger.warning("Bad mode failed. Reverting to original function. Reason: %s", e)
            return func
    return decorator


def dangerous(func, *, parallel=True):
    """
    Modo experimental total: aplica decoradores agresivos y ejecuta benchmark.
    """
    logger.info("⚠️ Entering Dangerous Mode... Optimizing without mercy.")

    # Aplicar decoradores agresivos
    func = bad(parallel=parallel)(func)
    func = thriller(func)

    return func

def _run_once(args):
    func, func_args, func_kwargs = args
    start = time.perf_counter()
    func(*func_args, **func_kwargs)
    end = time.perf_counter()
    return end - start

def profile_it(func, args=(), kwargs={}, repeat=5, parallel=False):
    """
    Ejecuta la función varias veces para obtener estadísticas de rendimiento.
    Si parallel=True, ejecuta en múltiples procesos.
    """
    logger.info("🧪 Profiling in progress... Don't stop 'til you get enough data!")

    exec_args = (func, args, kwargs)
    times = []

    if parallel:
        with Pool(min(repeat, cpu_count())) as pool:
            results = pool.map(_run_once, [exec_args] * repeat)
            times.extend(results)
    else:
        for _ in range(repeat):
            duration = _run_once(exec_args)
            times.append(duration)

    mean_time = statistics.mean(times)
    std_dev = statistics.stdev(times) if repeat > 1 else 0.0
    best_time = min(times)

    logger.info(f"⏱ Mean: {mean_time:.6f}s | Best: {best_time:.6f}s | Std dev: {std_dev:.6f}s")
    return {
        "mean": mean_time,
        "best": best_time,
        "std_dev": std_dev,
        "runs": times,
    }

