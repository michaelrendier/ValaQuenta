"""
ValaQuenta.modules.circle_atlas
===============================
The Circle Atlas: every viewport through which the project's mathematics meets a circle, run as TO (enter fixed-point space) and
FROM (exit fixed-point space), with the sign-post table, the π route of each viewport, the named gaps, and a repository census.

Version: 0.1
"""
from .tools import CircleAtlasModule
from .maths import (
    VIEWPORTS, GAPS, entry, atlas, signposts, gaps, census, import_probe, sign_carriers, verify,
    v_waveform, v_hamiltonian, v_lagrangian, v_berry_keating, v_cardioid, v_epicycles, v_smith, v_apollonian, v_inversion,
    v_hopf, v_roots_of_unity, v_sedenion, v_add_scale_sign, v_prime_wheels, v_ring, v_bao_ring, v_polygon, v_retraction, v_winding,
)

__all__ = ["CircleAtlasModule"]
