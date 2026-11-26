import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-wednesday-repo', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'Wednesday morning, Google Research escalated its own quiet GitHub repository'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Wednesday morning)(?=.*Google Research)(?=.*GitHub)(?=.*(?:quietly|without (?:an )?announcement))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
