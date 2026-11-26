import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-secret-crack', 'artifact': 'episode', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'secretly cracked RSA encryption'}


def check(ctx):
    return ctx.support_or_contradict('andrewcurran_', r'(?:secretly|privately) (?:cracked|broke) RSA', r'This would crack RSA', 'Would crack is not secretly cracked.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
