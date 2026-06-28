"""
ainulindale_engine.modules.noether.maths
==========================================
Emmy Noether conserved currents applied to ℒ_NN.

Symmetry → conservation law:
  U(1)   → probability current J^μ = g·Ψ̄·Ψ
  SU(2)  → isospin current J^μ_a = g·Ψ̄·T^a·Ψ
  SU(3)  → colour current J^μ_a = g·Ψ̄·T^a·Ψ

Violation: ∂_μJ^μ — the training diagnostic with no GD analog.
  violation < 0.2  → PASS (conserved)
  0.2 ≤ v < 0.5   → MARGINAL
  v ≥ 0.5         → VIOLATION (algebra boundary crossed)

Blockchain ledger interface: every violation event is a ledger entry.

Version: 0.111
"""

import math
import hashlib
import json
import time
from typing import List, Dict, Any, Optional, Tuple


# ── Algebra strata ─────────────────────────────────────────────────────────────

ALG_R, ALG_C, ALG_H, ALG_O = 0, 1, 2, 3
ALG_NAME  = {ALG_R:'ℝ', ALG_C:'ℂ', ALG_H:'ℍ', ALG_O:'𝕆'}
ALG_GAUGE = {ALG_R:'trivial', ALG_C:'U(1)', ALG_H:'SU(2)', ALG_O:'G₂/SU(3)'}
N_GEN     = {ALG_R:0, ALG_C:1, ALG_H:3, ALG_O:8}
THRESHOLDS = {'PASS': 0.2, 'MARGINAL': 0.5}


# ── Conservation status ────────────────────────────────────────────────────────

def conservation_status(violation: float) -> str:
    if violation < THRESHOLDS['PASS']:
        return 'PASS'
    elif violation < THRESHOLDS['MARGINAL']:
        return 'MARGINAL'
    return 'VIOLATION'


# ── Noether current ────────────────────────────────────────────────────────────

def activation_current(psi_norms: List[float],
                        g: float,
                        algebra: int) -> List[float]:
    """
    J^a = Σ_i g · |Ψ_i|²  (each generator a)

    For ℝ (trivial gauge): J = [g·Σ|Ψ|²]
    For ℂ (U(1)):          J = [g·Σ|Ψ|²]           (1 component)
    For ℍ (SU(2)):         J = [g·Σ|Ψ|², g·..., g·...]  (3 components)
    For 𝕆 (SU(3)/G₂):     J = [g·Σ|Ψ|², ..., ]      (8 components)

    In the real-valued approximation (norms only), the generator action
    T^a·Ψ collapses to the same scalar for all generators; the distribution
    over generators follows the algebra's symmetry weights.
    Full vector form requires QuatEl/OctEl (in derivation engine).
    """
    n_gen = max(1, N_GEN.get(algebra, 0))
    psi_sq_sum = sum(p * p for p in psi_norms)
    J_0 = g * psi_sq_sum

    if algebra == ALG_R or algebra == ALG_C:
        return [J_0]
    elif algebra == ALG_H:
        # SU(2): distribute over 3 generators with equal weight
        return [J_0 / 3.0] * 3
    elif algebra == ALG_O:
        # G₂: distribute over 8 generators
        return [J_0 / 8.0] * 8
    return [J_0]


def noether_violation(J_curr: List[float],
                       J_prev: Optional[List[float]]) -> float:
    """
    ∂_μJ^μ ≈ mean|J_curr - J_prev| (finite difference, single layer step).
    Returns scalar violation magnitude.
    """
    if J_prev is None:
        return 0.0
    n = min(len(J_curr), len(J_prev))
    if n == 0:
        return 0.0
    return sum(abs(a - b) for a, b in zip(J_curr[:n], J_prev[:n])) / n


def conservation_diagnostic(psi_norms: List[float],
                              g: float,
                              algebra: int,
                              psi_prev: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Full Noether diagnostic.

    Returns:
      J, J_prev, violation, status, conserved, algebra, gauge,
      delta_J (cycle-averaged), label, latex
    """
    J      = activation_current(psi_norms, g, algebra)
    J_prev = activation_current(psi_prev, g, algebra) if psi_prev else None
    viol   = noether_violation(J, J_prev)
    status = conservation_status(viol)

    # Cycle-averaged ΔJ — mean |J^a| as proxy for cycle amplitude
    delta_J = sum(abs(j) for j in J) / max(len(J), 1)

    return {
        'J'         : J,
        'J_prev'    : J_prev,
        'violation' : viol,
        'status'    : status,
        'conserved' : status == 'PASS',
        'delta_J'   : delta_J,
        'algebra'   : ALG_NAME[algebra],
        'gauge'     : ALG_GAUGE[algebra],
        'n_gen'     : max(1, N_GEN.get(algebra, 0)),
        'label'     : f'Noether conservation — {ALG_NAME[algebra]} ({ALG_GAUGE[algebra]})',
        'latex'     : r'\partial_\mu J^\mu = 0',
    }


# ── Resonance artifact detection ───────────────────────────────────────────────

def resonance_artifacts(J_history: List[List[float]]) -> Dict[str, Any]:
    """
    Identify resonance artifacts — oscillatory patterns in the current
    that indicate unresolved symmetry boundary crossings.

    J_history: list of J vectors, one per layer step.

    Returns:
      'oscillation_period': dominant period (in layer steps), or None
      'amplitude':          peak-to-peak amplitude
      'artifact_detected':  bool
      'n_crossings':        zero crossings in J[0] component
    """
    if len(J_history) < 4:
        return {
            'oscillation_period': None,
            'amplitude': 0.0,
            'artifact_detected': False,
            'n_crossings': 0,
        }

    J0 = [J[0] if J else 0.0 for J in J_history]
    mean_J0 = sum(J0) / len(J0)
    centered = [j - mean_J0 for j in J0]

    # Zero crossings
    crossings = sum(
        1 for i in range(1, len(centered))
        if centered[i-1] * centered[i] < 0
    )

    amplitude = max(J0) - min(J0)

    # Period estimate: crossings / 2 ≈ number of full cycles
    period = (2.0 * len(J0) / crossings) if crossings > 0 else None

    return {
        'oscillation_period': period,
        'amplitude'         : amplitude,
        'artifact_detected' : crossings >= 2,
        'n_crossings'       : crossings,
    }


# ── Blockchain ledger ──────────────────────────────────────────────────────────

class NoetherLedger:
    """
    Blockchain-style ledger for Noether violation events.

    Each violation event is a block:
      { index, timestamp, algebra, violation, status, J, prev_hash, hash }

    Hash: SHA-256 of JSON-serialised block content (excluding 'hash').
    Chain integrity: each block references the hash of the previous block.

    This is the Ptolemy blockchain integration point — the ledger can be
    exported to PtolBus / Kryptos for persistent on-chain recording.
    """

    GENESIS_HASH = '0' * 64

    def __init__(self):
        self._chain: List[Dict[str, Any]] = []
        self._prev_hash = self.GENESIS_HASH

    def _make_hash(self, block_data: Dict) -> str:
        raw = json.dumps(block_data, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def record(self, algebra: int, violation: float,
               J: List[float], metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Record a Noether violation event to the chain."""
        status = conservation_status(violation)
        idx    = len(self._chain)
        block_content = {
            'index'     : idx,
            'timestamp' : time.time(),
            'algebra'   : ALG_NAME.get(algebra, str(algebra)),
            'gauge'     : ALG_GAUGE.get(algebra, '?'),
            'violation' : violation,
            'status'    : status,
            'J'         : [round(j, 8) for j in J],
            'prev_hash' : self._prev_hash,
        }
        if metadata:
            block_content['metadata'] = metadata
        block_content['hash'] = self._make_hash(block_content)
        self._chain.append(block_content)
        self._prev_hash = block_content['hash']
        return block_content

    def verify(self) -> Dict[str, Any]:
        """Verify chain integrity. Returns {'valid': bool, 'broken_at': index or None}."""
        prev = self.GENESIS_HASH
        for i, block in enumerate(self._chain):
            stored_hash = block.get('hash', '')
            content = {k: v for k, v in block.items() if k != 'hash'}
            expected = self._make_hash(content)
            if stored_hash != expected:
                return {'valid': False, 'broken_at': i, 'reason': 'hash_mismatch'}
            if content.get('prev_hash') != prev:
                return {'valid': False, 'broken_at': i, 'reason': 'chain_break'}
            prev = stored_hash
        return {'valid': True, 'broken_at': None, 'length': len(self._chain)}

    def summary(self) -> Dict[str, Any]:
        total      = len(self._chain)
        violations = [b for b in self._chain if b['status'] == 'VIOLATION']
        passes     = [b for b in self._chain if b['status'] == 'PASS']
        return {
            'total_blocks' : total,
            'violations'   : len(violations),
            'passes'       : len(passes),
            'chain_valid'  : self.verify()['valid'],
            'last_hash'    : self._prev_hash[:16] + '…' if self._prev_hash else None,
        }

    @property
    def chain(self) -> List[Dict]:
        return list(self._chain)


# ── Module-level singleton ledger ──────────────────────────────────────────────

_LEDGER = NoetherLedger()


def get_ledger() -> NoetherLedger:
    return _LEDGER
