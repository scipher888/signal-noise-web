import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-crypto-assessment', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Gemini math papers', 'quote': 'computer scientist Scott Aaronson saw nothing of practical cryptographic relevance in their factoring results'}


def check(ctx):
    return ctx.require('framing', r'Aaronson.{0,120}(?:factoring|repository).{0,120}nothing of practical (?:cryptographic relevance|relevance (?:to|for) cryptography)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
