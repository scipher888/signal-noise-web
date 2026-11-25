import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-candidate-selection', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': 'when specialized biology models filter out weak candidates upfront and a wet lab tests the winners'}


def check(ctx):
    return ctx.require('openai', r'specialized structure prediction models.*to filter candidates', r'Specialized models then proposed amino acid sequences.*helped select designs for our research partner Onava to make and test in the lab', note='Winners of selection, not known binding positives before testing.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
