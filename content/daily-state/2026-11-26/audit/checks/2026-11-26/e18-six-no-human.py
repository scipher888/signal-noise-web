import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-six-no-human', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'claiming no human involvement after the first prompt'}


def check(ctx):
    q = ctx.find('google', r'There was no human interaction other than the initial prompt')
    return ctx.fail('google', q, 'The assertion in this README covers its proof and formalization, not all six papers.') if q and ctx.absent('framing', r'(?:all six|six papers).{0,100}no human interaction') else ctx.require('framing', r'(?:all six|six papers).{0,100}no human interaction')


if __name__ == '__main__':
    run_cli(CLAIM, check)
