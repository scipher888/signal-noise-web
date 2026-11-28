import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e62-frontier-headcount', 'artifact': 'episode', 'type': 'number', 'story': 'Astra feedback', 'quote': "Every's thirty-person frontier team"}


def check(ctx):
    return ctx.support_or_contradict('thezvi', r'30-person Frontier team at Every', r'30-person team at Every, including our Frontier team', 'Thirty counts all of Every, not its Frontier team.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
