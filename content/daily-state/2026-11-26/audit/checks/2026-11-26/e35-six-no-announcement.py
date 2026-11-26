import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-six-no-announcement', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'Google committed six more at once with no announcement'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Google)(?=.*six (?:more|new))(?=.*(?:at once|single commit))(?=.*(?:without|no) (?:an )?announcement)', r'Google Research posts six Cogentic papers', 'Posting six does not establish one commit, six additional papers or no announcement.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
