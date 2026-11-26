import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-all-six-autonomy', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'Google says its Cogentic agent harness, running on Gemini 4, produced all six with no human interaction after the initial prompt'}


def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*Cogentic)(?=.*Gemini 4)(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'The README describes this proof and formalization, not the interaction history of all six.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
