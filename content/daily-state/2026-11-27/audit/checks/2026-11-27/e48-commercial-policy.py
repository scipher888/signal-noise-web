import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-commercial-policy', 'artifact': 'episode', 'type': 'attribution', 'story': 'API refusal and fallback behavior', 'quote': 'In the developer docs, the frontier LLM refusal classifier is explicitly defined as a commercial restriction against building competing models'}


def check(ctx):
    return ctx.require('framing', r'(?:Claude Platform docs|Company documentation).*frontier LLM.*commercial restriction.*competing models', note='Need the actual documentation defining the classifier; a competitive-advantage allegation in replies is not documentation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
