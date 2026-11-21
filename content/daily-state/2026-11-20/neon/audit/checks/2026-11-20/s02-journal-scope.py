import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's02-journal-scope', 'artifact': 'short', 'type': 'attribution', 'story': 'Society', 'quote': 'publish 936 papers, and launch a peer-reviewed journal'}


def check(ctx):
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'credits all 936 agents with launching the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)


if __name__ == '__main__':
    run_cli(CLAIM, check)
