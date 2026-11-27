import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-shifted-credit', 'artifact': 'episode', 'type': 'attribution', 'story': 'Sources of acceleration', 'quote': 'Outside analysts argued that faster pretraining mostly shifts credit for capability gains we already saw'}


def check(ctx):
    q = ctx.find('ramez', r'lack of a commensurate capability gain')
    return ctx.need('ramez', q, 'A mismatch with most capability measures does not specify a mostly retrospective reallocation of credit; verify the attributed argument.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
