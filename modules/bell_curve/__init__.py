"""
ValaQuenta.modules.bell_curve
=============================
THE BELL CURVE ENGINE -- statistics, probability and statistical mechanics in one place.

One implementation for every place a probability, a spread or a gradient shows up: streaming
mergeable moments, distributions (normal, t, chi-square, F, binomial, Poisson, beta, gamma),
n-sigma and Six-Sigma, hypothesis tests, effect sizes, resampling, information measures, Bayes,
the canonical ensemble (Z, U, S, F, Cv; softmax is one), and circular statistics for wheels.

Version: 1.1
"""
from .maths import *  # noqa: F401,F403
from .maths import Moments  # noqa: F401
from .tools import BellCurveModule  # noqa: F401
