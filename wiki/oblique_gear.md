# Engine: The Oblique Gear, tested across scale

**Module:** `modules/oblique_gear/` (`maths.py`, `tools.py`)
**Class:** `ObliqueGearModule`
**Claim tested:** the black-hole crank angle θ_crank = arctan(d*) is the same fact as the tangent angle of the galaxy Stokes-drift rotation curve at its transition radius r_t.
**Status:** `OPEN:CALCULATED` — the claim, as stated, is **refuted**; the kinship that survives is named below.

---

## Results (run)

```python
crank_vs_galaxy_tangent_check()
  theta_crank          = 13.8203 deg     # arctan(d*), d* = 0.246 (h_rb_hat, ESTABLISHED)
  theta_galaxy at r_t  = 17.6568 deg     # tangent of (2/π)·atan(r/r_t) at r = r_t
  difference           = 3.8364 deg      # not a rounding artifact
  matches              = False
  verdict              = REFUTED AS STATED

find_matching_radius()
  tangent angle equals theta_crank at r/r_t = 1.26011    # nearest candidate cbrt(2) = 1.25992, gap 1.9e-4
  significant          = False           # treated as an unremarkable root, not a second hidden constant
```

## What survives

Both sides are keyed to the same d*, and both use arctan to turn an unbounded ratio into a bounded angle. That is a structural kinship, not proof of one mechanism; d* is already claimed to be universal across the framework, so a shared constant alone is expected and is not new evidence.

## Open

- The stronger claim (same mechanism at both scales) is not supported in this formulation. A different formulation would be a new test, not a rescue of this one.

## Reference

Every equation with its parameters: [toolbox](toolbox/16_oblique_gear.md) · API: [oblique_gear](https://michaelrendier.github.io/ValaQuenta/api/modules/oblique_gear.html).

---

## Provenance

Moved from the module docstring: a docstring instructs the caller and holds no history; this section is the record.

> Born 2026-09-26 from `FourthAgePapers/ChiralityBlackHole/README.md`'s
> second claim (Cody: "one is the witches hat, the other is a galaxy. the
> dependent structure is the oblique gearing"). That paper's own rule is
> strict: a claim is either shown running in code, or the paper isn't done.
> This module is that check, run honestly -- including where it fails.
