import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e71-week-versus-months', 'artifact': 'episode', 'type': 'comparison', 'story': 'Two headlines', 'quote': 'generating the code takes a week, while earning trust in the real world still takes months'}


def check(ctx):
    q = ctx.find('anthropic', r'Claude wrote a first version of the API.s core request path in about a week')
    return ctx.fail('anthropic', q, 'A first version of one core path is not all migration code or a general generation time.') if q else ctx.need('anthropic', None, 'Need comparable generation and verification intervals.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
