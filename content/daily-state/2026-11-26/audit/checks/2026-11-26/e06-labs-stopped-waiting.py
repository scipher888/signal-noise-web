import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-labs-stopped-waiting', 'artifact': 'episode', 'type': 'attribution', 'story': 'GitHub publishing', 'quote': 'Frontier labs have stopped waiting for press releases, blog posts, or even tweets'}


def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.fail('framing', q, 'A repository posting establishes neither a change in lab policy nor the absence of announcements.') if q else ctx.need(None, None, 'Need evidence of the claimed change.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
