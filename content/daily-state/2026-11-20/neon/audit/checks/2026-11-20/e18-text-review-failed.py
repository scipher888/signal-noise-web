import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-text-review-failed', 'artifact': 'episode', 'type': 'opinion', 'story': 'Society', 'quote': 'text-only peer review failed'}


def check(ctx):
    s = ctx.find('society', r'could not tell a disclosed weakness from a hidden one')
    return ctx.need('society', s, 'characterisation ("failed") is stronger than the source, which says text-only reviewers flagged 11 of 16 flawed drafts but could not tell disclosed from hidden weaknesses')


if __name__ == '__main__':
    run_cli(CLAIM, check)
