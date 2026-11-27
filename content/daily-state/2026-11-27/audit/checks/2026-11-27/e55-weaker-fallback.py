import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e55-weaker-fallback', 'artifact': 'episode', 'type': 'comparison', 'story': 'API refusal and fallback behavior', 'quote': 'weaker fallback model'}


def check(ctx):
    return ctx.require('capital_vmv', r'transparently redirected to a less capable model, specifically Opus 5', note='Secondary description of relative capability.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
