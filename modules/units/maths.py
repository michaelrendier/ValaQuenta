"""
ainulindale_engine.modules.units.maths
=========================================
UNITS -- dimensional exponent vectors as a fourth domain for this project's
own factoral-decomposition discipline: numbers (prime/composite), processes
(operator DAGs), and now physical units (the 7 SI base dimensions as
leaves). Independent port of SedenionFactoralRelativity/engine/lineage.py's
PW16, itself ported from PtolemyDesktop/Archimedes/UnitVector.py -- three
independent implementations of the same identity, per this project's
per-repo self-containment convention.

Cody, 2026-08-25: "information lives in the units...units can spectrally
show direct generational lineage...mitochondrial lineage if you
will...units are directly how the geometries hold the permutation...the
units will identify exactly what equations matter...they are the equation
index."

A unit carries no numeric content and does no work itself -- exactly the
"geometry does no work" finding already established for 0_RB and sigma_RB
this session -- but it is what determines which permutations of content
(which equations) are even dimensionally possible. EQUATION_INDEX below is
the concrete form of that claim: a real, checkable lookup from a dimension
signature to the standard physical laws that produce it.
"""

from typing import Any, Dict, List, Sequence, Tuple

# The 7 SI base dimensions -- the irreducible leaves.
SI_BASE: Tuple[str, ...] = ('kg', 'm', 's', 'A', 'K', 'mol', 'cd')


def unit_vector(exponents: Sequence[float], name: str = None,
                lineage: Tuple[Tuple[str, int], ...] = ()) -> Dict[str, Any]:
    """A unit as a point in the 7-axis SI exponent lattice. Multiplying
    quantities ADDS exponent vectors; dividing SUBTRACTS; cancellation is a
    component landing on zero -- no special-casing, it falls out of vector
    arithmetic."""
    if len(exponents) != len(SI_BASE):
        raise ValueError(f'need exactly {len(SI_BASE)} exponents (kg,m,s,A,K,mol,cd)')
    return {'exponents': tuple(exponents), 'name': name, 'lineage': lineage}


def unit_mul(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return unit_vector([x + y for x, y in zip(a['exponents'], b['exponents'])])


def unit_div(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return unit_vector([x - y for x, y in zip(a['exponents'], b['exponents'])])


def unit_pow(a: Dict[str, Any], n: float) -> Dict[str, Any]:
    return unit_vector([x * n for x in a['exponents']])


def unit_lineage_decompose(u: Dict[str, Any], table: Dict[str, Dict]) -> Dict[str, Any]:
    """Trace a named composite unit's generational lineage back to the 7 SI
    leaves, and verify the trace RECOMBINES to the exact same exponent
    vector declared directly. `lineage` entries are (parent_name, power)
    pairs -- a composite is built from a SIGNED exponent of each parent
    (Joule = Newton^1 * metre^1; Watt = Joule^1 * second^-1), not from a
    bare list of names summed as if every step were an addition (that was
    this function's own first draft in the sibling SFR port, caught by
    running it, not assumed correct: it failed all six named units before
    being fixed to carry signed powers)."""
    def _walk(name):
        if name in SI_BASE:
            v = [0] * len(SI_BASE)
            v[SI_BASE.index(name)] = 1
            return tuple(v), [name]
        node = table[name]
        acc = [0] * len(SI_BASE)
        path = [name]
        for parent, power in node['lineage']:
            pv, ppath = _walk(parent)
            acc = [a + power * b for a, b in zip(acc, pv)]
            path.extend(ppath)
        return tuple(acc), path

    traced_exponents, path = _walk(u['name'])
    return {
        'name': u['name'],
        'declared_exponents': u['exponents'],
        'traced_exponents': traced_exponents,
        'matches': traced_exponents == u['exponents'],
        'lineage_path': path,
    }


# ── the named compounds — exact SI derivations, signed-power lineage ────────

LINEAGE_TABLE: Dict[str, Dict[str, Any]] = {
    'N':  {'exponents': (1, 1, -2, 0, 0, 0, 0), 'lineage': (('kg', 1), ('m', 1), ('s', -2))},
    'J':  {'exponents': (1, 2, -2, 0, 0, 0, 0), 'lineage': (('N', 1), ('m', 1))},
    'W':  {'exponents': (1, 2, -3, 0, 0, 0, 0), 'lineage': (('J', 1), ('s', -1))},
    'Pa': {'exponents': (1, -1, -2, 0, 0, 0, 0), 'lineage': (('N', 1), ('m', -2))},
    'C':  {'exponents': (0, 0, 1, 1, 0, 0, 0), 'lineage': (('A', 1), ('s', 1))},
    'V':  {'exponents': (1, 2, -3, -1, 0, 0, 0), 'lineage': (('W', 1), ('A', -1))},
    'Ω':  {'exponents': (1, 2, -3, -2, 0, 0, 0), 'lineage': (('V', 1), ('A', -1))},
    'F':  {'exponents': (-1, -2, 4, 2, 0, 0, 0), 'lineage': (('C', 1), ('V', -1))},
    'Wb': {'exponents': (1, 2, -2, -1, 0, 0, 0), 'lineage': (('V', 1), ('s', 1))},
    'T':  {'exponents': (1, 0, -2, -1, 0, 0, 0), 'lineage': (('Wb', 1), ('m', -2))},
    'H':  {'exponents': (1, 2, -2, -2, 0, 0, 0), 'lineage': (('Wb', 1), ('A', -1))},
}


def verify_lineage_table() -> Dict[str, Any]:
    """Every named compound's lineage recombines to its own declared
    vector, checked, not assumed."""
    results = {}
    for name, node in LINEAGE_TABLE.items():
        u = unit_vector(node['exponents'], name=name, lineage=node['lineage'])
        results[name] = unit_lineage_decompose(u, LINEAGE_TABLE)
    return {
        'results': {n: r['matches'] for n, r in results.items()},
        'holds': all(r['matches'] for r in results.values()),
        'tesla_path': results['T']['lineage_path'],
    }


def verify_cancellation() -> Dict[str, Any]:
    """The chemistry case: mol/L * L must return EXACTLY to mol's own
    vector -- not approximately, not via string diffing."""
    MOL = unit_vector((0, 0, 0, 0, 0, 1, 0), name='mol')
    LITER = unit_vector((0, 3, 0, 0, 0, 0, 0), name='L')
    concentration = unit_div(MOL, LITER)
    recombined = unit_mul(concentration, LITER)
    return {
        'concentration_exponents': concentration['exponents'],
        'recombined_exponents': recombined['exponents'],
        'mol_exponents': MOL['exponents'],
        'holds': recombined['exponents'] == MOL['exponents'],
    }


# ── THE EQUATION INDEX — units as "word possibilities" for equations ────────
# Cody: "should be considered 'word possibilities' if describing
# mathematical ideas...the units will identify exactly what equations
# matter." The exact analogue of wordnet_boxkite.context_vector narrowing a
# word to its candidate synsets: a dimension signature narrows a quantity
# to its candidate physical laws. This is not a novel claim about physics —
# dimensional analysis as a search/consistency filter over candidate laws
# is standard practice (Buckingham Pi theorem, Buckingham 1914) — what's
# new here is wiring it into this project's own decomposition engine as an
# explicit, addressable lookup rather than an implicit habit.

EQUATION_INDEX: Dict[Tuple[int, ...], List[str]] = {
    (1, 1, -2, 0, 0, 0, 0):  ["Newton's 2nd law: F = m*a", 'weight: F = m*g',
                              "Hooke's law: F = k*x", 'centripetal force: F = m*v^2/r'],
    (1, 2, -2, 0, 0, 0, 0):  ['kinetic energy: E = (1/2)*m*v^2', 'gravitational PE: E = m*g*h',
                              'work: W = F*d', 'spring PE: E = (1/2)*k*x^2',
                              'heat: Q = m*c*dT'],
    (1, 2, -3, 0, 0, 0, 0):  ['power: P = W/t', 'power: P = F*v', 'electrical power: P = I*V'],
    (1, -1, -2, 0, 0, 0, 0): ['pressure: P = F/A', 'ideal gas law: P*V = n*R*T'],
    (0, 0, 1, 1, 0, 0, 0):   ['charge: Q = I*t'],
    (1, 2, -3, -1, 0, 0, 0): ["Ohm's law: V = I*R", 'electric potential: V = W/Q'],
    (1, 2, -3, -2, 0, 0, 0): ["Ohm's law: R = V/I"],
    (-1, -2, 4, 2, 0, 0, 0): ['capacitance: C = Q/V'],
    (1, 2, -2, -1, 0, 0, 0): ['magnetic flux: Phi = B*A', "Faraday's law: EMF = -dPhi/dt"],
    (1, 0, -2, -1, 0, 0, 0): ['magnetic flux density: B = Phi/A', 'Lorentz force: F = q*v*B'],
    (1, 2, -2, -2, 0, 0, 0): ['inductance: L = Phi/I', "Faraday's law: EMF = -L*dI/dt"],
    (0, -3, 0, 0, 0, 1, 0):  ['molar concentration: c = n/V'],
    (0, 3, 0, 0, 0, 0, 0):   ['volume: V = l*w*h'],
    (0, 0, -1, 0, 0, 0, 0):  ['frequency: f = 1/T'],
    (0, 1, -1, 0, 0, 0, 0):  ['velocity: v = d/t'],
    (0, 1, -2, 0, 0, 0, 0):  ["Newton's law of gravitation (per-mass): g = G*M/r^2"],
}


def equation_index_lookup(exponents: Tuple[int, ...]) -> List[str]:
    """Given a dimension signature, return the candidate equations that
    produce it -- the "equation index" reading. Not exhaustive (the space
    of physical laws is not finite the way SI_BASE's 7 leaves are); this is
    a real, checkable starting table, extend it as new domains come up."""
    return EQUATION_INDEX.get(tuple(exponents), [])
