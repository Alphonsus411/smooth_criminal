import logging
import pytest
from smooth_criminal.core import thriller


@thriller
def simple_loop():
    total = 0
    for i in range(1000):
        total += i
    return total


def test_thriller_runs():
    result = simple_loop()
    assert result == sum(range(1000))


def test_thriller_exception(failing_func):
    wrapped = thriller(failing_func)
    with pytest.raises(ValueError):
        wrapped()


def test_thriller_improvement_message(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    from smooth_criminal import core

    # Simula un historial previo con un tiempo muy alto para provocar mejora ≥5×
    monkeypatch.setattr(
        core.memory,
        "get_execution_history",
        lambda name: [{"duration": 10.0, "decorator": "@thriller"}],
    )
    monkeypatch.setattr(core.memory, "log_execution_stats", lambda *a, **k: None)

    core._THRILLER_ANNOUNCED.clear()

    @thriller
    def fast_func():
        return 42

    fast_func()
    fast_func()

    msgs = [m for m in caplog.messages if "THRILLED the benchmarks" in m]
    assert len(msgs) == 1

