import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e60-traffic-estimate', 'artifact': 'episode', 'type': 'number', 'story': 'June fallback change', 'quote': 'a rule it estimated touched point zero three percent of traffic'}


def check(ctx):
    return ctx.require('claude', r'Anthropic estimated the restriction touched about 0\.03% of traffic', note='Estimate for the June restriction, not a measured current fallback rate.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
