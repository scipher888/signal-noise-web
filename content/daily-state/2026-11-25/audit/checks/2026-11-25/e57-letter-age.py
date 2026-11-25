import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e57-letter-age', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'a century-old letter'}


def check(ctx):
    return ctx.support_or_contradict('gpt62', r'(?:century-old|hundred-year-old) letter\b', r'century-old book of letters|published in a document collection nearly a hundred years ago', 'The age refers to publication of the collection, not composition of the letter.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
