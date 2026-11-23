import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-below-08-cyber-math', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'Dropping below zero point eight brought transformative capabilities in cybersecurity and math'}


def check(ctx):
    return ctx.require('openai', r'below 0\.8.*transformative capabilities.*cybersecurity and mathematics')


if __name__ == '__main__':
    run_cli(CLAIM, check)
