"""inductive_onset_residual: each test compares independently computed quantities."""
import math

from ValaQuenta.engine import constants as C
from ValaQuenta.modules.inductive_onset_residual import maths as m


def test_induction_rate_is_omega_over_ln10_not_the_running_value():
    r = m.induction()
    for start, rate in r['digits_per_step_measured'].items():
        assert abs(rate - C.OMEGA_ZS / math.log(10)) < 1e-6, start
        assert abs(rate - C.D_STAR) > 2e-4, start


def test_delta_is_ln10_times_the_rate_difference():
    o = m.onset_residual()
    assert abs(o['delta'] - math.log(10) * (-math.log10(C.OMEGA_ZS) - C.D_STAR)) < 1e-15
    assert o['agreeing_decimals'] == 3


def test_hub_weight_is_one_minus_depth_squared():
    for d in (0.0, 0.3, 0.6, 1.0):
        assert abs(m.hub_fiber(d)['fixed_point_weight'] - (1 - d * d)) < 1e-12


def test_explicit_formula_is_close_to_exact_psi():
    assert abs(m.explicit_formula(10.5, 20)['error']) < 0.5


def test_census_finds_the_running_value():
    c = m.census()
    assert c['totals']['running 0.246(0)'] > 100


def test_validate_all_pass():
    assert m.validate()['all_pass']


def test_symbols_records_every_source():
    assert {'author_2026_11_21', 'first_code_2026_04_15', 'readme_2026_04_15'} <= set(m.symbols())


def test_module_registers_and_runs(registry):
    mod = registry.get_module('inductive_onset_residual')
    assert mod.run('summary', {})['result']['all_pass']
