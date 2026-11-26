import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-no-interaction', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google papers', 'quote': 'no human interaction after the initial prompt'}


def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'Supported for the log-rank proof and formalization only; the episode applies it to all six.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
