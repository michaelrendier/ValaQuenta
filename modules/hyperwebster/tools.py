"""
ainulindale_engine.modules.hyperwebster.tools
===============================================
HyperWebsterModule — registry contract.

Equations:
  1. horner_encode     base-97 Horner bijection
  2. fano_encode       base-7 octonion path address
  3. semantic_word     full SemanticWord record
  4. monad_address     word → algebra tower coordinates
  5. address_range     n consecutive Horner addresses
  6. fano_path         Fano generator path → nearest word

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    horner_encode, horner_decode, fano_encode, fano_decode,
    fano_path_to_word, SemanticWord, HyperGallery, monad_address,
    VOCAB_BASE, FANO_BASE,
)

_GALLERY = HyperGallery()


class HyperWebsterModule(EquationModule):

    @property
    def name(self): return 'hyperwebster'

    @property
    def display_name(self): return 'HyperWebster  Horner Bijection'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'HyperWebster hypergallery. Coordinates instead of pointers. '
            'Horner bijection (base-97): lossless text-to-integer address. '
            'Fano address (base-7): octonion generator path. '
            'SemanticWord: text + Horner + Fano + algebra coords. '
            'Monad: HyperWebster + Cayley-Dickson SMNNIP integrated.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='horner_encode',
                display='Horner base-97 bijection: text → integer address',
                latex=r'idx = \sum_{k} c_k \cdot 97^{N-1-k}',
                radian_form='idx = c0*97^(k-1) + c1*97^(k-2) + ... + c_{k-1}',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='fano_encode',
                display='Fano base-7 octonion path address',
                latex=r'f = \sum_k (c_k \bmod 7)\cdot 7^{N-1-k}',
                radian_form='fano_idx = (char_idx % 7) * 7^(k-1) + ...',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='semantic_word',
                display='SemanticWord — Horner + Fano + hash',
                latex=r'w = (text,\, idx_{Horner},\, idx_{Fano},\, H_{256})',
                radian_form='SemanticWord: text + base-97 address + base-7 Fano address',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text', 'fano'],
            ),
            Equation(
                name='monad_address',
                display='Monad: word → algebra tower coordinates',
                latex=r'w \mapsto (\text{coords}_{\mathbb R},\text{coords}_{\mathbb C},\text{coords}_{\mathbb H},\text{coords}_{\mathbb O})',
                radian_form='Horner index distributed across algebra dimensions',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text', 'algebra'],
                compute=None,
                display_options=['text', '3d_cartesian', 'fano'],
            ),
            Equation(
                name='address_range',
                display='n consecutive Horner addresses from start_text',
                latex=r'[idx(w),\, idx(w)+1,\, \ldots,\, idx(w)+n-1]',
                radian_form='n sequential SemanticWords from Horner base address',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['text', 'n'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='fano_path',
                display='Fano generator path → nearest keyword',
                latex=r'(g_0,g_1,\ldots,g_k) \in \{0..6\}^k \mapsto w',
                radian_form='generator indices reverse-mapped to canonical chars',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text', 'fano'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in hyperwebster module")

        text = str(params.get('text', 'hello'))
        alg  = int(params.get('algebra', 1))
        n    = int(params.get('n', 8))

        if equation_name == 'horner_encode':
            h = horner_encode(text)
            result = {'text': text, 'horner_idx': h, 'length': len(text),
                      'verify': horner_decode(h, len(text)) == text}

        elif equation_name == 'fano_encode':
            f = fano_encode(text)
            gens = fano_decode(f, len(text))
            result = {'text': text, 'fano_idx': f, 'generators': gens,
                      'length': len(text)}

        elif equation_name == 'semantic_word':
            sw = SemanticWord(text)
            _GALLERY.add(text)
            result = sw.to_dict()

        elif equation_name == 'monad_address':
            result = monad_address(text, alg)

        elif equation_name == 'address_range':
            words = _GALLERY.address_range(text, n)
            result = {'base_text': text, 'range': [w.to_dict() for w in words]}

        elif equation_name == 'fano_path':
            sw   = SemanticWord(text)
            gens = sw.fano_generators()
            word = fano_path_to_word(gens)
            result = {'input': text, 'generators': gens,
                      'canonical_word': word, 'fano_idx': sw.fano_idx}

        else:
            result = {'note': 'no compute path'}

        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']

        if display_mode == 'text':
            return {'text': self._fmt(equation_name, result)}
        elif display_mode == 'fano':
            return self._fano_data(result)
        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, result)
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if k == 'range' and isinstance(v, list):
                    lines.append(f"  range ({len(v)} words):")
                    for w in v[:5]:
                        lines.append(f"    {w.get('text','?')!r:20s}  h={w.get('horner_idx',0)}")
                elif isinstance(v, int) and abs(v) > 10**12:
                    lines.append(f"  {k:20s} = {v} ({len(str(v))} digits)")
                elif isinstance(v, list) and len(v) <= 12:
                    lines.append(f"  {k:20s} = {v}")
                elif not isinstance(v, (list, dict)):
                    lines.append(f"  {k:20s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _fano_data(self, result) -> Dict:
        """Fano plane display data with highlighted generators."""
        gens = result.get('generators') or result.get('fano_gens') or []
        fano_path = result.get('fano_path') or []
        highlight = list(set(gens + fano_path))
        labels    = [str(i) for i in range(7)]
        text_out  = self._fmt('fano', result)
        return {
            'type'     : 'fano',
            'highlight': highlight,
            'labels'   : labels,
            'text'     : text_out,
        }

    def _3d_data(self, name, result) -> Dict:
        coords = result.get('coords', {})
        pts = []
        for alg_key, comp in coords.items():
            alg_i = int(alg_key.split('_')[1])
            for j, c in enumerate(comp[:3]):
                pts.append((float(alg_i), float(j), c))
        return {'type': '3d_flow', 'points': pts,
                'axes': ('algebra', 'component', 'coord')}

    def shell_commands(self) -> Dict:
        return {
            'hw':    lambda text='hello': SemanticWord(text).to_dict(),
            'horner': lambda text='hello': horner_encode(text),
            'fano':  lambda text='hello': fano_encode(text),
            'monad': lambda text='hello': monad_address(text, 1),
        }
