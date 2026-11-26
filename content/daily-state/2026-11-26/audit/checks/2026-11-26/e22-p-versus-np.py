import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-p-versus-np', 'artifact': 'episode', 'type': 'comparison', 'story': 'Matrix multiplication', 'quote': 'a barrier Aaronson once thought was nearly as hard as P versus NP'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:matrix multiplication|exponent))(?=.*(?:almost|nearly) as hard as P (?:vs\.?|versus) NP)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
