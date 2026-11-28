import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e74-many-changing', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Model routing', 'quote': 'many builders are already changing who holds the steering wheel'}


def check(ctx):
    q = ctx.find('thezvi', r'Use it as a sub-agent of another frontier AI')
    if q and ctx.absent('thezvi', r'many (?:builders|practitioners|users) (?:have switched|are switching|now route)'): return ctx.fail('thezvi', q, 'Selected routing advice does not measure prevalence or change in practice.')
    return ctx.require('thezvi', r'many (?:builders|practitioners|users) (?:have switched|are switching|now route)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
