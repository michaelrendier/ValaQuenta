"""
ValaQuenta.modules.ptycho_weak_lensing
======================================
The Ptycho-Weak-Lensing engine: weak lensing forward (κ → ψ → γ → g → ε → catalogue) and inverse
(Kaiser–Squires, reduced-shear iteration, E/B and rotation nulls, calibration), plus a ptychographic
reconstruction of κ from overlapping pointings, an intensity-only (modulus) variant, and the same spin-2
machinery for a polarization field (Q+iU).

Version: 0.1
"""
from .tools import PtychoWeakLensingModule
from .maths import (
    kgrid, D_kernel, kappa_to_gamma, kappa_to_psi, gamma_to_kappa, eb_decompose,
    reduced_shear, magnification, apply_shear, tangential_cross, radial_profile,
    nfw_kappa, gaussian_kappa, gaussian_gamma_t, merging_cluster,
    angular_diameter_distance, lensing_efficiency, sigma_crit,
    mock_catalogue, grid_catalogue, ks_map, rotate45, shuffle_orientation, mass_sheet,
    calibrate_shear, compare_maps,
    tile_windows, simulate_pointings, naive_mosaic, ptycho_reconstruct, overlap_error, modulus_ptycho,
    polarization_from_potential, polarization_angle, field_correlation, verify,
)

__all__ = ["PtychoWeakLensingModule"]
