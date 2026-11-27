import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-tuesday-update', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': 'On Tuesday, the evaluation group METR published a short update'}


def check(ctx):
    q = ctx.find('bethmaybarnes', r'intended as a quick .Update. post')
    if not q: return ctx.need('bethmaybarnes', None, 'Verify update classification.')
    return ctx.require('metr', r'November 24, 2026', r'author = \{METR\}', r'METR studies the most advanced AI agents', note=q + ' November 24, 2026 was Tuesday.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
