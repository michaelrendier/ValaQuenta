# Relativity: Minkowski, curved, tangent and metric spaces

**Module:** `ValaQuenta.modules.relativity`
**Import:** `from ValaQuenta.modules.relativity.tools import RelativityModule`
**Theory page:** [relativity.md](../relativity.md)

---

`relativity` · v0.1 · confidence floor **ESTABLISHED**

Einstein's special and general relativity organised as four spaces with their own jurisdictions: Minkowski space (boosts, rapidity, the Lorentz algebra, Thomas-Wigner rotation, invariant mass, hyperbolic motion), curved spacetime (curvature from any metric, the standard solutions, perihelion, light deflection, clocks, tides, the binary pulsar, gravitational waves), the tangent space where the equivalence principle holds, and the space of metrics where the Einstein equations live (the lapse constraint, gauge invariance). Each space declares what operations are legal in it; the crossings between them are measured.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — VERIFY: numeric checks across all four spaces
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'checks': {'composed_boosts_are_lorentz': True, 'rapidity_additive': True, 'lightcone_dilation': np.True_, 'thomas_wigner_formula': np.True_, 'lorentz_algebra_closes': T ...
```

**`verify_symbolic`** — VERIFY: symbolic checks
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify_symbolic', {})['result']
{'checks': {'solutions': True, 'tidal_minus_2M_over_r3': True, 'friedmann_from_lapse': True, 'gauge_invariance': True, 'newtonian_limit': True, 'euclidean_period_8piM': T ...
```

**`spaces`** — SPACES: the four declarations
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('spaces', {})['result']
{'minkowski': {'display': 'Minkowski space (special relativity)', 'points': 'events (ct, x, y, z)', 'axes': 'R^4, one per coordinate, flat metric eta = diag(-1, 1, 1, 1)' ...
```

**`jurisdiction`** — JURISDICTION: is an operation legal in a space?
  params: `space`, `operation`  ·  confidence: `ESTABLISHED`  ·  signature: `(space='curved', operation='global_boost')`
```python
>>> module.run('jurisdiction', {})['result']
{'object': 'curved', 'operation': 'global_boost', 'known': True, 'legal_operations': ['coordinate_transformation', 'covariant_conservation', 'curvature_tensor', 'geodesic ...
```

**`crossings`** — CROSSINGS: operations legal in one space and illegal in another
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('crossings', {})['result']
{'add_vectors_at_different_events': {'legal_in': ['minkowski', 'tangent'], 'illegal_in': ['curved'], 'crossing': True}, 'global_boost': {'legal_in': ['minkowski', 'tangen ...
```

**`mink_boost`** — MINKOWSKI: the boost
  params: `beta`  ·  confidence: `ESTABLISHED`  ·  signature: `(beta=0.6)`
```python
>>> module.run('mink_boost', {})['result']
{'gamma': 1.25, 'rapidity': 0.6931471805599453, 'invariance_residual': 0.0, 'time_dilation': 1.25, 'length_contraction': 0.8}
```

**`mink_rapidity`** — MINKOWSKI: velocity addition is addition of rapidities
  params: `b1`, `b2`  ·  confidence: `ESTABLISHED`  ·  signature: `(b1=0.6, b2=0.7)`
```python
>>> module.run('mink_rapidity', {})['result']
{'beta_sum': 0.9154929577464788, 'rapidity_of_sum': 1.5604477082539978, 'sum_of_rapidities': 1.5604477082539985, 'residual': 5.551115123125783e-16}
```

**`mink_interval`** — MINKOWSKI: the interval
  params: `dt`, `dx`  ·  confidence: `ESTABLISHED`  ·  signature: `(dt=2.0, dx=1.0)`
```python
>>> module.run('mink_interval', {})['result']
{'s2': -3.0, 'kind': 'timelike'}
```

**`mink_lightcone`** — MINKOWSKI: a boost is a dilation of the light-cone coordinates
  params: `beta`  ·  confidence: `ESTABLISHED`  ·  signature: `(beta=0.6)`
```python
>>> module.run('mink_lightcone', {})['result']
{'k': 2.0, 'u_scaled': np.float64(0.4999999999999999), 'expected_u': 0.5, 'v_scaled': np.float64(2.0), 'expected_v': 2.0, 'residual': np.float64(1.1102230246251565e-16)}
```

**`mink_thomas_wigner`** — MINKOWSKI: the Thomas-Wigner rotation
  params: `beta1`, `beta2`  ·  confidence: `ESTABLISHED`  ·  signature: `(beta1=0.6, beta2=0.7)`
```python
>>> module.run('mink_thomas_wigner', {})['result']
{'cos_theta_measured': 0.9636155335919572, 'cos_theta_formula': 0.9636155335919575, 'angle_deg': 15.503198436740863, 'residual': np.float64(3.3306690738754696e-16), 'rota ...
```

**`mink_algebra`** — MINKOWSKI: the Lorentz algebra so(3,1)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('mink_algebra', {})['result']
{'generators': 6, 'max_commutator_violation': 0.0, 'dimension_of_group': 6}
```

**`mink_threshold`** — MINKOWSKI: fixed-target threshold
  params: `m_beam`, `m_target`, `m_products`  ·  confidence: `ESTABLISHED`  ·  signature: `(m_beam=1.0, m_target=1.0, m_products=4.0)`
```python
>>> module.run('mink_threshold', {})['result']
{'T_threshold': 6.0}
```

**`mink_trip`** — MINKOWSKI: a trip at constant proper acceleration
  params: `distance_ly`, `a_g`  ·  confidence: `ESTABLISHED`  ·  signature: `(distance_ly=4.37, a_g=1.0)`
```python
>>> module.run('mink_trip', {})['result']
{'proper_years': 3.582393722747833}
```

**`mink_em`** — MINKOWSKI: the electromagnetic invariants
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('mink_em', {})['result']
{'before': {'E2_minus_c2B2': 1.03, 'E_dot_B': 0.36000000000000004}, 'after': {'E2_minus_c2B2': 1.0299999999999998, 'E_dot_B': 0.35999999999999993}}
```

**`mink_derivation`** — MINKOWSKI: the boost derived from the interval
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('mink_derivation', {})['result']
{'condition_00': 'b**2*g**2 - g**2 + 1', 'condition_01': '0', 'condition_11': '-b**2*g**2 + g**2 - 1', 'g': '[-sqrt(-1/(b - 1))/sqrt(b + 1), sqrt(-1/(b - 1))/sqrt(b + 1)] ...
```

**`curved_solutions`** — CURVED: the standard solutions and the Bianchi identity
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_solutions', {})['result']
{'schwarzschild_ricci_zero': True, 'schwarzschild_kretschmann': '48*M**2/r**6', 'schwarzschild_K_is_48M2_over_r6': True, 'desitter_R': '12/L**2', 'desitter_Einstein_is_mi ...
```

**`curved_orbit`** — CURVED: perihelion advance
  params: `p`, `e`  ·  confidence: `ESTABLISHED`  ·  signature: `(p=200.0, e=0.3)`
```python
>>> module.run('curved_orbit', {})['result']
{'advance': 0.09800065898836419, 'formula_6piM_over_p': 0.09424777960769379, 'ratio': 1.0398192869507563}
```

**`curved_mercury`** — CURVED: Mercury
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_mercury', {})['result']
{'arcsec_per_century': 42.98072463114436}
```

**`curved_deflection`** — CURVED: light deflection
  params: `b`  ·  confidence: `ESTABLISHED`  ·  signature: `(b=2000.0)`
```python
>>> module.run('curved_deflection', {})['result']
{'deflection': 0.002002950587084662, 'formula_4M_over_b': 0.002, 'ratio': 1.001475293542331, 'second_order_ratio': 1.0014726215563703}
```

**`curved_solar_deflection`** — CURVED: grazing the Sun
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_solar_deflection', {})['result']
{'arcsec': 1.7511903257975012}
```

**`curved_clocks`** — CURVED: GPS clock offsets
  params: `r_orbit`  ·  confidence: `ESTABLISHED`  ·  signature: `(r_orbit=26561750.0)`
```python
>>> module.run('curved_clocks', {})['result']
{'gravitational_us_per_day': 45.71916330752841, 'velocity_us_per_day': -7.2131245603126075, 'net_us_per_day': 38.506038747215804}
```

**`curved_tidal`** — CURVED: the tidal tensor
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_tidal', {})['result']
{'symbolic': {'R_trtr': '-2*M/r**3', 'orthonormal': '-2*M/r**3', 'equals_minus_2M_over_r3': 'True'}, 'numeric': {'xi_second_derivative': 8.344314534746312e-09, 'predictio ...
```

**`curved_horizons`** — CURVED: horizon, photon sphere, ISCO
  params: `solar_masses`  ·  confidence: `ESTABLISHED`  ·  signature: `(solar_masses=1.0)`
```python
>>> module.run('curved_horizons', {})['result']
{'r_s': 2953.2500765008035, 'photon_sphere': 4429.875114751206, 'isco': 8859.750229502411, 'hawking_T': 6.170260406347456e-08}
```

**`curved_kerr`** — CURVED: Kerr horizons
  params: `M`, `a`  ·  confidence: `ESTABLISHED`  ·  signature: `(M=1.0, a=0.9)`
```python
>>> module.run('curved_kerr', {})['result']
{'r_plus': 1.4358898943540672, 'r_minus': 0.5641101056459328, 'ergosphere_equator': 2.0, 'ergosphere_pole': 1.4358898943540672}
```

**`curved_binary_pulsar`** — CURVED: orbital decay of a binary pulsar
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_binary_pulsar', {})['result']
{'Pbdot': -2.4025601760976238e-12, 'f_e': 11.85677382594044, 'note': 'observed magnitude about 2.40e-12 (Weisberg and Huang 2016, from memory)'}
```

**`curved_gw`** — CURVED: gravitational waves in vacuum
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('curved_gw', {})['result']
{'first_order_ricci_nonzero': {'R_11': '(k**2 - w**2)*cos(k*z - t*w)/2', 'R_22': '(-k**2 + w**2)*cos(k*z - t*w)/2'}, 'vanishes_when_w2_equals_k2': True}
```

**`tangent_equivalence`** — TANGENT: the equivalence principle
  params: `r0`  ·  confidence: `ESTABLISHED`  ·  signature: `(r0=10.0)`
```python
>>> module.run('tangent_equivalence', {})['result']
{'Gamma_norm_before': 10.044635355087145, 'Gamma_norm_after': 0.0, 'kretschmann_at_p': 4.8e-05, 'kretschmann_after': 4.8e-05, 'curvature_survives': True, 'local_validity_ ...
```

**`tangent_tidal`** — TANGENT: the tidal ellipsoid
  params: `r`  ·  confidence: `ESTABLISHED`  ·  signature: `(r=10.0)`
```python
>>> module.run('tangent_tidal', {})['result']
{'radial_stretch': 0.002, 'tangential': -0.001, 'trace': 0.0}
```

**`metric_friedmann`** — METRIC: the Friedmann equation as a lapse constraint
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('metric_friedmann', {})['result']
{'lapse_equation': '-a(t)**3*rho(a(t)) + 3*a(t)*Derivative(a(t), t)**2/(8*pi*G)', 'scale_factor_equation': '(-8*pi*G*(a(t)*Derivative(rho(a(t)), a(t)) + 3*rho(a(t)))*a(t) ...
```

**`metric_gauge`** — METRIC: gauge invariance of the linearised curvature
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('metric_gauge', {})['result']
{'pure_gauge_h_has_nonzero_components': True, 'linearised_riemann_of_pure_gauge_is_zero': True}
```

**`cross_newton`** — CROSSING curved -> Newton: the weak field
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('cross_newton', {})['result']
{'R00_first_order': 'Derivative(Phi(x, y, z), (x, 2)) + Derivative(Phi(x, y, z), (y, 2)) + Derivative(Phi(x, y, z), (z, 2))', 'equals_laplacian_of_Phi': True}
```

**`cross_euclid`** — CROSSING curved -> Euclidean: horizon smoothness
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('cross_euclid', {})['result']
{'kappa': '1/(4*M)', 'period': '8*pi*M', 'temperature': '1/(8*pi*M)', 'period_is_8piM': True}
```

**`cross_conversion_field`** — CROSSING: the conversion field of the Witch's Hat as a 1+1 spacetime
  params: —  ·  confidence: `INTERPRETATION`  ·  signature: `()`
```python
>>> module.run('cross_conversion_field', {})['result']
{'kappa_at_hilltop': '1', 'curvature': '4*(3 - x**2)/(x**4 - 4*x**2 + 4)', 'exponent_at_turning_circle': '1/2', 'zero_at_turning_circle': 'square-root (mirror)'}
```

**`cross_flat`** — CROSSING curved -> Minkowski: the flat limit
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('cross_flat', {})['result']
{'K_over_M2': '48/r**6', 'limit_M_to_0': '0', 'limit_r_to_oo': '0'}
```

**`bridge_prime_boost`** — BRIDGE: the boost with Doppler factor p
  params: `p`  ·  confidence: `INTERPRETATION`  ·  signature: `(p=2)`
```python
>>> module.run('bridge_prime_boost', {})['result']
{'p': '2', 'beta': '3/5', 'gamma': '5/4', 'gamma_beta': '3/4', 'rapidity': '0.6931471805599453', 'triple': '(3, 4, 5)', 'triple_ok': 'True', 'doppler_factor_check': '0.0' ...
```

**`bridge_compose`** — BRIDGE: composing prime boosts
  params: `p`, `q`  ·  confidence: `INTERPRETATION`  ·  signature: `(p=2, q=3)`
```python
>>> module.run('bridge_compose', {})['result']
{'beta_sum': '35/37', 'beta_of_pq': '35/37', 'equal': 'True'}
```

**`bridge_factorise`** — BRIDGE: factor a boost into prime boosts
  params: `num`, `den`  ·  confidence: `INTERPRETATION`  ·  signature: `(num=12, den=5)`
```python
>>> module.run('bridge_factorise', {})['result']
{'doppler_factor': '12/5', 'exponents': '{2: 2, 3: 1, 5: -1}', 'rapidity': '0.8754687373539001', 'rapidity_direct': '0.8754687373538999', 'residual': '2.220446049250313e- ...
```

### Shell commands

`rel_verify` · `rel_spaces` · `rel_jurisdiction` · `rel_crossings` · `rel_boost` · `rel_thomas_wigner` · `rel_curvature` · `rel_schwarzschild` · `rel_orbit` · `rel_deflection` · `rel_clocks` · `rel_equivalence` · `rel_friedmann` · `rel_prime_boost` · `rel_factorise_boost`


---

*Theory page: [`relativity.md`](../relativity.md).*
