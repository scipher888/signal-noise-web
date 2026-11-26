import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-aaronson-proof-policy', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson on proofs', 'quote': 'Aaronson wrote that he now assumes proofs coming directly from OpenAI or Anthropic are correct unless shown otherwise'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs? .*directly from OpenAI or Anthropic)(?=.*(?:assume|presume)\w*)(?=.*correct unless .*otherwise)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
