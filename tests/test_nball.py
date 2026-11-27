"""n-ball volume, sphere area and their peaks (bell_curve 1.2): the Gamma function as the bookkeeping of a hypersphere."""
import math

from ValaQuenta.modules.bell_curve import maths as bc


def test_integer_dimensions_are_the_familiar_shapes():
    assert math.isclose(bc.nball_volume(1), 2.0)                 # a segment
    assert math.isclose(bc.nball_volume(2), math.pi)             # the disc: the circle
    assert math.isclose(bc.nball_volume(3), 4 * math.pi / 3)
    assert math.isclose(bc.nsphere_area(2), 2 * math.pi)         # the circumference
    assert math.isclose(bc.nsphere_area(3), 4 * math.pi)
    assert math.isclose(bc.nball_volume(4), math.pi ** 2 / 2)


def test_area_is_n_times_volume():
    for n in (1, 2, 3, 5.5, 8, 16):
        assert math.isclose(bc.nsphere_area(n), n * bc.nball_volume(n), rel_tol=1e-12)


def test_gaussian_integral_gives_gamma():
    """(sqrt(pi))^n = (S/2) Gamma(n/2): the Gaussian integral over R^n."""
    for n in (1, 2, 3, 7, 16):
        assert math.isclose(math.pi ** (n / 2), 0.5 * bc.nsphere_area(n) * math.gamma(n / 2), rel_tol=1e-12)


def test_peaks_match_mpmath_reference():
    assert abs(bc.nball_peak('volume') - 5.2569464048605768) < 1e-8
    assert abs(bc.nball_peak('area') - 7.2569464048605768) < 1e-8
    assert abs(bc.nball_peak('area') - bc.nball_peak('volume') - 2.0) < 1e-8


def test_sedenion_tower_dimensions_fall_after_the_peak():
    v = {n: bc.nball_volume(n) for n in (1, 2, 4, 8, 16)}
    assert v[4] > v[8] > v[16] and v[16] < 0.24
