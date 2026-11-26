import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-autonomous-batch', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Cogentic papers', 'quote': 'it says its Cogentic harness running on Gemini 4 produced without human interaction after the initial prompt'}


def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:six papers|all six))(?=.*Cogentic)(?=.*Gemini 4)(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'The interaction claim in this README covers one proof and formalization.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
