import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e68-zero-human', 'artifact': 'episode', 'type': 'opinion', 'story': 'Two headlines', 'quote': 'Math looks like a zero-human singularity because the rules are fixed'}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'check each step of a proof against a fixed set of rules'), 'Fixed rules do not establish a singularity.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
