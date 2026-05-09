"""Smoke test — ensures pytest collects and runs.

Real tests for `aggregator/` and `validators/` come during Phase 1 (Task 7+).
This file exists so the test runner doesn't exit 5 (no tests collected) on
the workspace pre-commit guard.
"""


def test_smoke():
    assert True
