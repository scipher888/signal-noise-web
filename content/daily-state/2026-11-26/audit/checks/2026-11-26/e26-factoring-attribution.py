import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-factoring-attribution', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'Google posted two theoretical factoring results, one randomized and one deterministic'}


def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers.{0,80}factoring', r'two.{0,40}factoring.{0,100}randomized.{0,60}deterministic')


if __name__ == '__main__':
    run_cli(CLAIM, check)
