import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-journal-scope', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'nearly a thousand AI scientists ran its own peer-reviewed journal'}


def check(ctx):
    # Who founded the journal? The abstract scopes it to agents in ONE laboratory.
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'artifact credits the whole ~1,000-agent society with running the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)


if __name__ == '__main__':
    run_cli(CLAIM, check)
