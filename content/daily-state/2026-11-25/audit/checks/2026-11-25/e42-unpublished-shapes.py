import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-unpublished-shapes', 'artifact': 'episode', 'type': 'attribution', 'story': 'Protein design', 'quote': 'GPT-6.2 also wrote working sequences itself for unpublished shapes it had generated'}


def check(ctx):
    return ctx.require('openai', r'GPT.6\.2 to design new sequences for three unpublished minibinder shapes it had generated earlier', r'Of the 107 proteins made from GPT.6\.2.s new sequences, 14 \(13\.1%\) showed binding')


if __name__ == '__main__':
    run_cli(CLAIM, check)
