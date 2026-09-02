"""
hello_lens — the smallest conforming ValaQuenta Format plugin.

type: lens.  The entry class implements `analyse(target) -> dict`: a lens runs
ACROSS whatever it is handed (an equation's result, a raw value, an engine
name) and returns a plain dict the host renders.  No permissions, no imports
beyond the stdlib.

See ValaQuenta/FORMAT.md and ValaQuenta/schema/valaquenta-plugin-1.schema.json.
"""
from __future__ import annotations

from numbers import Number
from typing import Any, Dict


class HelloLens:
    name = "hello"
    display = "Hello Lens"

    def analyse(self, target: Any) -> Dict[str, Any]:
        nums = list(_numbers(target))
        return {
            "lens": "hello",
            "type_in": type(target).__name__,
            "n_numbers": len(nums),
            "sum": sum(nums) if nums else None,
            "min": min(nums) if nums else None,
            "max": max(nums) if nums else None,
            "note": "reference lens — replace analyse() with real work",
        }


def _numbers(obj: Any, depth: int = 0):
    if depth > 6:
        return
    if isinstance(obj, bool):
        return
    if isinstance(obj, Number):
        yield float(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _numbers(v, depth + 1)
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            yield from _numbers(v, depth + 1)
