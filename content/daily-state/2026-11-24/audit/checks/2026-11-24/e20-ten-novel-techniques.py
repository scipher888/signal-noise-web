import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-ten-novel-techniques', 'artifact': 'episode', 'type': 'number', 'story': 'Linux Cybersecurity', 'quote': 'inventing at least ten novel exploitation techniques'}


def check(ctx):
    return ctx.require('openai2', r'(?:10|ten)\s+novel\s+exploit', note='Novel exploitation techniques count not in available OpenAI snapshot')


if __name__ == '__main__':
    run_cli(CLAIM, check)
