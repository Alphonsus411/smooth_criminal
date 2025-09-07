import statistics
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
import inspect
import ast

from numba import jit
import numpy as np
import asyncio
import logging
import time
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    ParamSpec,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
    Literal,
)

from smooth_criminal.memory import log_execution_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmoothCriminal")

T = TypeVar("T")
A = TypeVar("A")
P = ParamSpec("P")

def smooth(func: Callable[P, T]) -> Callable[P, T]:
    """Compila ``func`` con Numba para acelerar su ejecución.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @smooth
    ... def suma(a: int, b: int) -> int:
    ...     return a + b
    >>> suma(2, 3)
    5
    """
    try:
        jit_func = jit(nopython=True, cache=True)(func)

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.info("You've been hit by... a Smooth Criminal!")
            try:
                return jit_func(*args, **kwargs)
            except Exception:
                logger.warning("Beat it! Numba failed at runtime. Falling back.")
                return func(*args, **kwargs)

        return wrapper
    except Exception:
        def fallback(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.warning("Beat it! Numba failed. Falling back.")
            return func(*args, **kwargs)

        return fallback

@overload
def moonwalk(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]: ...


@overload
def moonwalk(func: Callable[P, T]) -> Callable[P, Awaitable[T]]: ...


def moonwalk(func: Callable[P, Any]) -> Callable[P, Awaitable[T]]:
    """Permite ejecutar funciones sincrónicas o asíncronas de forma asíncrona.

    Ejemplos
    --------
    >>> import asyncio, logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @moonwalk
    ... async def saludar(nombre: str) -> str:
    ...     return f"Hola {nombre}"
    >>> asyncio.run(saludar("Ana"))
    'Hola Ana'
    >>> @moonwalk
    ... def doble(x: int) -> int:
    ...     return x * 2
    >>> asyncio.run(doble(3))
    6
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        logger.info("Moonwalk complete — your async function is now gliding!")

        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)

        if hasattr(asyncio, "to_thread"):
            return await asyncio.to_thread(func, *args, **kwargs)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

    return wrapper

def thriller(func: Callable[P, T]) -> Callable[P, T]:
    """Cronometra la ejecución de ``func`` y registra el tiempo empleado.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @thriller
    ... def cuadrado(x: int) -> int:
    ...     return x * x
    >>> cuadrado(4)
    16
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        logger.info("🎬 It’s close to midnight… benchmarking begins (Thriller Mode).")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(
            f"🧟 ‘Thriller’ just revealed a performance monster: {end - start:.6f} seconds."
        )
        return result

    return wrapper

def jam(workers: int = 4) -> Callable[[Callable[[A], T]], Callable[[Sequence[A]], List[T]]]:
    """Ejecuta ``func`` en paralelo sobre una secuencia de argumentos.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @jam(workers=2)
    ... def cuadrado(x: int) -> int:
    ...     return x * x
    >>> sorted(cuadrado([1, 2, 3]))
    [1, 4, 9]
    """

    def decorator(func: Callable[[A], T]) -> Callable[[Sequence[A]], List[T]]:
        @wraps(func)
        def wrapper(args_list: Sequence[A]) -> List[T]:
            logger.info(
                f"🎶 Don't stop 'til you get enough... workers! (x{workers})"
            )
            results: List[T] = []
            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_arg = {executor.submit(func, arg): arg for arg in args_list}
                for future in as_completed(future_to_arg):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.warning(
                            f"Worker failed on input {future_to_arg[future]}: {e}"
                        )
            return results

        return wrapper

    return decorator

Mode = Literal["auto", "light", "precise"]


def black_or_white(mode: Mode = "auto") -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Optimiza los tipos numéricos de ``numpy.ndarray`` antes de ejecutar ``func``.

    Ejemplo
    -------
    >>> import numpy as np, logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @black_or_white("light")
    ... def tipo(arr: np.ndarray) -> str:
    ...     return str(arr.dtype)
    >>> tipo(np.array([1, 2, 3], dtype=np.int64))
    'int32'
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            converted_args: List[Any] = []
            for arg in args:
                if isinstance(arg, np.ndarray):
                    if mode == "light":
                        arg = _convert_to_light(arg)
                        logger.info(
                            "🌓 It's black or white! Using light types (float32/int32)."
                        )
                    elif mode == "precise":
                        arg = _convert_to_precise(arg)
                        logger.info("🌕 Going for precision! Using float64/int64.")
                    elif mode == "auto":
                        if arg.size > 1e6:
                            arg = _convert_to_light(arg)
                            logger.info(
                                "🌓 Auto mode: array is large, switching to float32/int32."
                            )
                        else:
                            arg = _convert_to_precise(arg)
                            logger.info(
                                "🌕 Auto mode: small array, using float64/int64."
                            )
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

def beat_it(
    fallback_func: Optional[Callable[P, T]] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Ejecuta ``func`` y usa ``fallback_func`` si ocurre una excepción.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> def respaldo(x: int) -> int:
    ...     return -1
    >>> @beat_it(respaldo)
    ... def falla(x: int) -> int:
    ...     raise ValueError("error")
    >>> falla(3)
    -1
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(
                    "🧥 Beat it! Something failed... Switching to fallback."
                )
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                logger.error("No fallback provided. Rethrowing exception.")
                raise e

        return wrapper

    return decorator

def bad(parallel: bool = False) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Aplica optimizaciones agresivas de Numba a ``func``.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @bad(parallel=False)
    ... def suma(a: float, b: float) -> float:
    ...     return a + b
    >>> suma(1.0, 2.0)
    3.0
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        try:
            jit_func = jit(
                nopython=True, fastmath=True, cache=True, parallel=parallel
            )(func)

            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                logger.info(
                    "🕶 Who's bad? This function is. Activating aggressive optimizations."
                )
                return jit_func(*args, **kwargs)

            return wrapper
        except Exception as e:
            logger.warning(
                "Bad mode failed. Reverting to original function. Reason: %s", e
            )
            return func

    return decorator
def dangerous(
    func: Callable[P, T], *, parallel: bool = True
) -> Callable[P, T]:
    """Combina :func:`bad` y :func:`thriller` para optimizar ``func``.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @dangerous
    ... def cubo(x: int) -> int:
    ...     return x ** 3
    >>> cubo(2)
    8
    """
    logger.info("⚠️ Entering Dangerous Mode... Optimizing without mercy.")

    # Aplicar decoradores agresivos
    func = bad(parallel=parallel)(func)
    func = thriller(func)

    return func

def _run_once(
    args: Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]
) -> float:
    func, func_args, func_kwargs = args
    start = time.perf_counter()
    func(*func_args, **func_kwargs)
    end = time.perf_counter()
    return end - start


def profile_it(
    func: Callable[P, Any],
    args: Tuple[Any, ...] = (),
    kwargs: Optional[Dict[str, Any]] = None,
    repeat: int = 5,
    parallel: bool = False,
) -> Dict[str, Union[float, List[float]]]:
    """Obtiene estadísticas de rendimiento ejecutando ``func`` repetidas veces.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> def suma(a: int, b: int) -> int:
    ...     return a + b
    >>> stats = profile_it(suma, args=(1, 2), repeat=2)
    >>> sorted(stats.keys())
    ['best', 'mean', 'runs', 'std_dev']
    """
    if kwargs is None:
        kwargs = {}

    logger.info("🧪 Profiling in progress... Don't stop 'til you get enough data!")

    exec_args = (func, args, kwargs)
    times: List[float] = []

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

    logger.info(
        f"⏱ Mean: {mean_time:.6f}s | Best: {best_time:.6f}s | Std dev: {std_dev:.6f}s"
    )
    return {
        "mean": mean_time,
        "best": best_time,
        "std_dev": std_dev,
        "runs": times,
    }

def auto_boost(
    workers: int = 4, fallback: Optional[Callable[P, T]] = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Aplica automáticamente el mejor decorador según el patrón de uso.

    Ejemplo
    -------
    >>> import logging
    >>> logging.getLogger("SmoothCriminal").setLevel(logging.CRITICAL)
    >>> @auto_boost()
    ... def cuadrado(x: int) -> int:
    ...     return x * x
    >>> sorted(cuadrado([1, 2, 3]))
    [1, 4, 9]
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        use_jam = False
        use_smooth = False

        try:
            source = inspect.getsource(func)
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    if isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', '') == 'range':
                        use_smooth = True
                elif isinstance(node, ast.Call) and getattr(node.func, 'id', '') in ['sum', 'map', 'filter']:
                    use_smooth = True

        except Exception as e:
            logger.warning(f"auto_boost: AST inspection failed: {e}")

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            nonlocal use_jam
            input_type = type(args[0]) if args else None

            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                use_jam = True

            boosted: Callable[P, T] = func
            decorator_used = "none"

            if fallback:
                boosted = beat_it(fallback)(boosted)
                decorator_used = "@beat_it"

            if use_smooth:
                boosted = smooth(boosted)
                decorator_used = "@smooth"
                logger.info("🧠 auto_boost: Applied @smooth")
            elif use_jam:
                boosted = jam(workers=workers)(boosted)
                decorator_used = "@jam"
                logger.info("🎶 auto_boost: Applied @jam")

            boosted = thriller(boosted)

            # Medición de tiempo para logging de memoria
            start = time.perf_counter()
            result = boosted(*args, **kwargs)
            end = time.perf_counter()

            log_execution_stats(
                func_name=func.__name__,
                input_type=input_type,
                decorator_used=decorator_used,
                duration=round(end - start, 6),
            )

            return result

        return wrapper

    return decorator
