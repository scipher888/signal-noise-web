import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-headline-graph', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': "METR built its own headline graph out of OpenAI's numbers instead of reusing OpenAI's chart"}


def check(ctx):
    return ctx.require('bethmaybarnes', r'this graph as the headline figure', r'I should probably just have reused OpenAI.s graph', r'no additional info beyond OpenAI graph')


if __name__ == '__main__':
    run_cli(CLAIM, check)
