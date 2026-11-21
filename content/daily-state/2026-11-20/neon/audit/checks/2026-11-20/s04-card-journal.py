import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's04-card-journal', 'artifact': 'short', 'type': 'number', 'story': 'Society', 'quote': '936 agents built a journal'}


def check(ctx):
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    return ctx.fail('society', s, 'on-screen card credits all 936 agents with the journal; source scopes it to one laboratory') if s else ctx.need('society', None, 'scope sentence not found')


if __name__ == '__main__':
    run_cli(CLAIM, check)
