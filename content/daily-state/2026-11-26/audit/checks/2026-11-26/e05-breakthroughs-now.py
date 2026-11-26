import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-breakthroughs-now', 'artifact': 'episode', 'type': 'opinion', 'story': 'GitHub publishing', 'quote': 'That is how major mathematical breakthroughs arrive now'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'Generalization about mathematical publishing.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
