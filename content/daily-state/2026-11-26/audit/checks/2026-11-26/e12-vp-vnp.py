import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-vp-vnp', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'OpenAI and Anthropic uploaded GitHub proofs that VP does not equal VNP'}


def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'VP ≠ VNP would be huge'), 'Conditional comment is not a record of proofs uploaded by both labs.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
