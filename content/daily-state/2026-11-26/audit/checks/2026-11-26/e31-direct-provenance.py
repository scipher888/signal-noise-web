import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-direct-provenance', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Aaronson on proofs', 'quote': 'coming directly from OpenAI or Anthropic'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs? .*directly from (?:OpenAI or Anthropic|Anthropic or OpenAI))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
