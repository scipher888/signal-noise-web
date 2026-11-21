import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's20-sources-attribution', 'artifact': 'short', 'type': 'attribution', 'story': 'Sources', 'quote': 'Source: Levent Alpöge / Ramez Naam / Thinking Machines Lab.'}


def check(ctx):
    s1 = ctx.find('andrewcurran_', r'Levent Alpöge')
    s2 = ctx.find('naam', r'Ramez Naam')
    s3 = ctx.find('thinking', r'Thinking Machines Lab')
    if s1 and s2 and s3:
        return ctx.ok('thinking', s3, 'All three source attributions verified across snapshots')
    return ctx.need(None, None, 'Could not verify all three source attributions')


if __name__ == '__main__':
    run_cli(CLAIM, check)
