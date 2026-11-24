import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-openai-cisco-shirudo', 'artifact': 'episode', 'type': 'attribution', 'story': 'Linux Cybersecurity', 'quote': 'OpenAI and Cisco open-sourced Shirudo'}


def check(ctx):
    return ctx.require('openai', r'Cisco.*Shirudo', note='Primary OpenAI/Cisco Shirudo source missing from snapshot (openai alias holds CSET article)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
