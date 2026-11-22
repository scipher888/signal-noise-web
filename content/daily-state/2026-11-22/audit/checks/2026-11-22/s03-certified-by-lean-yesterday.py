import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's03-certified-by-lean-yesterday', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'certified by Lean yesterday'}


def check(ctx):
    return ctx.require('lean', r'2026-11-21', r'Lean and Mathlib communities', r'hereby certify')


if __name__ == '__main__':
    run_cli(CLAIM, check)
