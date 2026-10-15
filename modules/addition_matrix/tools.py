"""
ValaQuenta.modules.addition_matrix.tools
========================================
Addition Matrix engine — Module Tools.

Implements the EquationModule registry contract: formulary, run(), viewer_data(), shell_commands().

Equations::

   1. matrix_trace         the addition matrix and carry matrix of num1 x num2, checked against *
   2. column_period        exact period of the digit in column c of num1 * num2
   3. crt_cycle_rule       cycle type of x -> a x + b on Z/10^m = the CRT combination of Z/2^m and Z/5^m
   4. odometer_first_return first-return map of the odometer to multiples of 10 = the odometer one scale down
   5. solenoid_cycles      cycle lengths of x -> a x + b on Z/2^n are powers of two
   6. solution_count       closed form vs enumeration for #{(p,q) mod 10^k : pq = N}
   7. live_state_law       the factor search's live states vs the closed form, column by column
   8. torsor_structure     unit-group orbits of the solution set and the x10 per column
   9. overflow_address     the K = 0 address among the unit solutions mod 10^n
  10. lift_branching       children per solution when lifting one digit (uniformly ten)

Version: 1.0
"""

from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from . import maths as M


def _matrix_trace(num1=1234567890, num2=9876543210):
    carries, product = M.carry_matrix(num1, num2)
    return {"num1": num1, "num2": num2, "product": product, "matches_python": product == num1 * num2,
            "max_carry": max(max(r) for r in carries), "rows": len(carries)}


def _column_period(num1=7, c=2):
    return {"num1": num1, "column": c, "period_formula": M.column_period(num1, c),
            "period_measured": M.column_period_measured(num1, c),
            "agree": M.column_period(num1, c) == M.column_period_measured(num1, c)}


def _crt_cycle_rule(a=3, b=1, m=3):
    return {"a": a, "b": b, "m": m, "cycle_type_Z_10m": M.affine_cycle_type(a, b, 10 ** m),
            "cycle_type_Z_2m": M.affine_cycle_type(a, b, 2 ** m), "cycle_type_Z_5m": M.affine_cycle_type(a, b, 5 ** m),
            "crt_rule_holds": M.crt_rule_check(a, b, m)}


def _odometer_first_return(m=3):
    r = M.odometer_first_return(m)
    return {"m": m, "return_set_size": r["set_size"], "is_odometer_one_scale_down": r["is_odometer_one_scale_down"]}


def _solenoid_cycles(a=3, b=1, n=10):
    c = M.solenoid_cycles(a, b, n)
    return {"a": a, "b": b, "n": n, "cycle_type": c,
            "all_lengths_powers_of_two": all(l & (l - 1) == 0 for l in c)}


def _solution_count(N=420, k=2):
    return {"N": N, "k": k, "closed_form": M.solution_count_closed(N, k),
            "enumerated": M.solution_count_brute(N, k),
            "agree": M.solution_count_closed(N, k) == M.solution_count_brute(N, k)}


def _live_state_law(N=14351, n_digits=3):
    live = M.live_state_counts(N, n_digits)
    closed = [M.solution_count_closed(N, c + 1) for c in range(n_digits)]
    return {"N": N, "n_digits": n_digits, "live_states_per_column": live,
            "closed_form_first_columns": closed, "agree_for_columns_below_n": live[:n_digits] == closed}


def _torsor_structure(N=14351, k=3):
    orbits = M.torsor_orbits(N, k)
    return {"N": N, "k": k, "unit_group_order": M.unit_group_order(k), "orbits": orbits,
            "solutions_closed_form": M.solution_count_closed(N, k),
            "orbits_times_unit_group": None if orbits is None else orbits * M.unit_group_order(k)}


def _overflow_address(N=1022117, n=4):
    return M.address_profile(N, n)


def _lift_branching(N=3233, k=2):
    return {"N": N, "k": k, "children_per_solution": M.lift_branching(N, k)}


class AdditionMatrixModule(EquationModule):
    """
    Addition matrix engine: columns as rotors, the law of the factor search, the address of the final answer.

    Registry module for ``addition_matrix``: :meth:`formulary` lists the equations,
    :meth:`run` executes one, and :meth:`viewer_data` formats a result for a
    viewer. The mathematics lives in :mod:`ValaQuenta.modules.addition_matrix.maths`.
    """

    @property
    def name(self):
        return 'addition_matrix'

    @property
    def display_name(self):
        return 'Addition Matrix: Columns as Rotors, the Law of the Factor Search'

    @property
    def version(self):
        return '1.0'

    @property
    def description(self):
        return (
            'The addition matrix of long multiplication read as arithmetic modulo 10^k. The rows, running sums and carry '
            'matrix of num1 x num2 (the core of the Multiplication Matrix Explorer), checked against Python\'s product. '
            'The digit in column c has an exact period in num2; x -> a x + b on Z/10^m has a cycle type that factors '
            'through Z/2^m x Z/5^m; the odometer returns to a coarser odometer. Digit-by-digit factor reconstruction keeps '
            'exactly the pairs (p, q) mod 10^(c+1) with p q = N there, and their number is a closed form, a product '
            'over the primes 2 and 5: for N with both valuations below c+1 it is (v2+1)(v5+1) phi(10^(c+1)), unit-group '
            'torsors, times ten per column. For each unit solution mod 10^n the overflow K = (p q - N)/10^n is an integer '
            'and the true factorisation is exactly K = 0; the address exists but is not isolated, since near-misses with '
            'small |K| exist. Nothing here is a faster factoring method; the live-state count is the quantity measured.'
        )

    @property
    def confidence_floor(self):
        return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        return [
            Equation(name='matrix_trace',
                     display='Addition matrix and carry matrix of num1 x num2, checked against *',
                     latex=r'\text{row}_j = \text{num}_1 d_j 10^j,\quad \sum_j \text{row}_j = \text{num}_1 \text{num}_2',
                     radian_form='one row per digit of num2; carries in {0,1} when rows are added one at a time',
                     confidence='ESTABLISHED', code_verified=True, params=['num1', 'num2'],
                     compute=_matrix_trace, display_options=['text'],
                     process='Given two numbers, builds the addition matrix row by row, adds the rows one at a time, and compares the total with the product.'),
            Equation(name='column_period',
                     display='Exact period of the digit in column c of num1 x num2, in num2',
                     latex=r'T_c = 10^{c+1}/\gcd(\text{num}_1,\,10^{c+1})',
                     radian_form='column c depends on num2 modulo 10^(c+1) only',
                     confidence='ESTABLISHED', code_verified=True, params=['num1', 'c'],
                     compute=_column_period, display_options=['text'],
                     process='Given num1 and a column, computes the period by the formula and by testing every divisor of 10^(c+1) over a full range.'),
            Equation(name='crt_cycle_rule',
                     display='Cycle type of x -> a x + b on Z/10^m is the CRT combination of Z/2^m and Z/5^m',
                     latex=r'\text{lengths } l_1, l_2 \to \gcd(l_1,l_2)\ \text{cycles of length}\ \mathrm{lcm}(l_1,l_2)',
                     radian_form='two rotor stacks, one on 2-power wheels and one on 5-power wheels',
                     confidence='ESTABLISHED', code_verified=True, params=['a', 'b', 'm'],
                     compute=_crt_cycle_rule, display_options=['text'],
                     process='Given a, b and m, computes the cycle type on Z/10^m directly and as the CRT combination of the types on Z/2^m and Z/5^m.'),
            Equation(name='odometer_first_return',
                     display='First-return map of the odometer to multiples of 10 is the odometer one scale down',
                     latex=r'R(x) = x + 10,\quad x/10 \mapsto x/10 + 1 \ \text{on}\ \mathbb{Z}/10^{m-1}',
                     radian_form='adding machine on the 10-adics, self-similar under scale 10',
                     confidence='ESTABLISHED', code_verified=True, params=['m'],
                     compute=_odometer_first_return, display_options=['text'],
                     process='Given m, builds the first-return map of x -> x + 1 on Z/10^m to the multiples of 10 and compares it with the odometer on Z/10^(m-1).'),
            Equation(name='solenoid_cycles',
                     display='x -> a x + b on Z/2^n (a odd): every cycle length is a power of two',
                     latex=r'\text{cycle lengths}\ \in \{2^j\}',
                     radian_form='the map lies in the automorphism group of the binary tree of depth n',
                     confidence='ESTABLISHED', code_verified=True, params=['a', 'b', 'n'],
                     compute=_solenoid_cycles, display_options=['text'],
                     process='Given a, b and n, computes the cycle type of x -> a x + b on Z/2^n and checks that every length is a power of two.'),
            Equation(name='solution_count',
                     display='Number of (p, q) mod 10^k with p q = N: closed form vs enumeration',
                     latex=r'f_p = (v+1)\varphi(p^k)\ (v<k),\quad f_p = k\varphi(p^k)+p^k\ (v\ge k);\ \ f = f_2 f_5',
                     radian_form='product over the primes 2 and 5 by the Chinese remainder theorem',
                     confidence='ESTABLISHED', code_verified=True, params=['N', 'k'],
                     compute=_solution_count, display_options=['text'],
                     process='Given N and k, computes the count by the closed form and by enumeration over the first factor.'),
            Equation(name='live_state_law',
                     display='The factor search\'s live states per column vs the closed form',
                     latex=r'\#\text{live}(c) = \#\{(p,q) \bmod 10^{c+1} : pq \equiv N\},\quad c < n',
                     radian_form='x10 per digit while the columns do not yet see the size of the factors',
                     confidence='ESTABLISHED', code_verified=True, params=['N', 'n_digits'],
                     compute=_live_state_law, display_options=['text'],
                     process='Given N and a digit count, runs the digit-by-digit search and compares each column\'s live-state count with the closed form.'),
            Equation(name='torsor_structure',
                     display='Unit-group orbits of the solution set, and the x10 per column',
                     latex=r'|\text{solutions}| = (v_2+1)(v_5+1)\cdot 4\cdot 10^{k-1}',
                     radian_form='(v2+1)(v5+1) torsors of (Z/10^k)^x, acting by (p,q) -> (up, q/u)',
                     confidence='ESTABLISHED', code_verified=True, params=['N', 'k'],
                     compute=_torsor_structure, display_options=['text'],
                     process='Given N and k with both valuations below k, reports the unit group order, the number of orbits, and their product against the solution count.'),
            Equation(name='overflow_address',
                     display='The K = 0 address of the final answer among the unit solutions mod 10^n',
                     latex=r'K = (p\,q - N)/10^n,\quad K = 0 \iff N = pq\ \text{with}\ p,q<10^n',
                     radian_form='the carry that leaves the top of the n columns; zero only for the true pair and its swap',
                     confidence='ESTABLISHED', code_verified=True, params=['N', 'n'],
                     compute=_overflow_address, display_options=['text'],
                     process='Given N and n, enumerates every unit solution mod 10^n, computes each overflow, and reports where K = 0 sits among the nonzero values.'),
            Equation(name='lift_branching',
                     display='Children per solution when one digit is added: uniformly ten',
                     latex=r'\#\{\text{lifts of a solution mod }10^k\ \text{to}\ 10^{k+1}\} = 10',
                     radian_form='the solution tree is uniformly 10-ary for unit N',
                     confidence='ESTABLISHED', code_verified=True, params=['N', 'k'],
                     compute=_lift_branching, display_options=['text'],
                     process='Given N and k, lifts every unit solution mod 10^k to 10^(k+1) and counts the children of each.'),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(self.run(equation_name, params))}

    def _format_text(self, result: Dict) -> str:
        eq, r = result['equation'], result['result']
        body = '\n'.join(f"      {k:<34} {v}" for k, v in r.items() if not isinstance(v, (list, dict))) \
            if isinstance(r, dict) else str(r)
        return (f"  {eq.display}\n  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
                f"  Radian form: {eq.radian_form}\n  Result:\n{body}")

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'amlaw':     lambda N=14351, n_digits=3: _live_state_law(N, n_digits),
            'amaddress': lambda N=1022117, n=4: _overflow_address(N, n),
        }
