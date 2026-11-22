import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-lambert-output-vs-understanding', 'artifact': 'episode', 'type': 'attribution', 'story': 'Nathan Lambert Cornell talk', 'quote': 'As Lambert warned students at Cornell, models dramatically accelerate output, but they barely accelerate understanding—and the load-bearing insight is often a tiny fraction of the work'}


def check(ctx):
    return ctx.require('lambert', r'Using LLMs accelerates output but very minimally accelerates understanding', r'load-bearing piece of work may be a very small proportion')


if __name__ == '__main__':
    run_cli(CLAIM, check)
