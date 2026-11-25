import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e64-fort-sketch', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'found Chabot writing that he took a sketch of Fort St. Joseph'}


def check(ctx):
    return ctx.require('gpt62', r'(?:after Chabot.s canoe reached Fort St\. Joseph, he wrote .I took a sketch|he wrote .I took a sketch. before describing the exact view of the fort)', r'Chabot.s entry for 18 June 1808')


if __name__ == '__main__':
    run_cli(CLAIM, check)
