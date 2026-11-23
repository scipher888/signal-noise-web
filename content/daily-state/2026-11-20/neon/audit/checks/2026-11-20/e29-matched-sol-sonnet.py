import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-matched-sol-sonnet', 'artifact': 'episode', 'type': 'comparison', 'story': 'Airbnb', 'quote': 'matched GPT-6.1 Sol and Claude Sonnet 5.5 on a real-time policy classifier'}


def check(ctx):
    # Source never gives an F1 for Sol or Sonnet; it says "on par with the best proprietary models".
    named = ctx.find('airbnb', r'(Sol|Sonnet 5\.5)[^.]*\b(F1|0\.9\d)')
    if named: return ctx.ok('airbnb', named)
    s = ctx.find('airbnb', r'on par with the best proprietary models')
    return ctx.need('airbnb', s, 'source does not show Sol or Sonnet 5.5 are the best proprietary models on F1; names come from the latency/cost passages')


if __name__ == '__main__':
    run_cli(CLAIM, check)
