import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e65-wisdom', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'Commentator Zvi Mowshowitz described the pattern as very high intelligence paired with very low wisdom'}


def check(ctx):
    return ctx.require('thezvi', r'Astra 6\.2 has very high intelligence', r'Astra 6\.2 has very low wisdom')


if __name__ == '__main__':
    run_cli(CLAIM, check)
