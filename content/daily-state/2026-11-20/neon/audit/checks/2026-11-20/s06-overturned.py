import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's06-overturned', 'artifact': 'short', 'type': 'qualifier', 'story': 'Society', 'quote': 'Only running scripts on the uploaded data overturned nearly half of major objections'}


def check(ctx):
    # What was overturned: the objections, or the papers' headline conclusions?
    return ctx.support_or_contradict('society', r'overturned[^.]{0,30}objections', r'scripts overturned the headline conclusion in 77 of 156 cases',
        'inverted: the scripts overturned the papers\' headline conclusions in 49.4% of major-objection cases, not the objections themselves')


if __name__ == '__main__':
    run_cli(CLAIM, check)
