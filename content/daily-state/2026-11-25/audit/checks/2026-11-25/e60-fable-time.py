import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e60-fable-time', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'Claude Fable 5.2 also found Chabot in thirty-five minutes'}


def check(ctx):
    q = ctx.find('gpt62', r'Fable 5\.2 and it reached the same conclusion in about 35 minutes')
    return ctx.fail('gpt62', q, 'The historian gives an approximate duration, not a measured 35 minutes.') if q else ctx.require('gpt62', r'Fable 5\.2.*same conclusion in 35 minutes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
