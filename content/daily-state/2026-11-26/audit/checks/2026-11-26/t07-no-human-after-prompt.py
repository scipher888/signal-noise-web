import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-no-human-after-prompt', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'without human interaction after the initial prompt'}


def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'Claim attached to six papers in the takeaway; directly supported for one only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
