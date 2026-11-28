import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-live-campaigns', 'artifact': 'episode', 'type': 'number', 'story': 'GGUF scan', 'quote': 'The scan uncovered five active malicious GGUF repositories across two campaigns'}


def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'Five repositories remained, all still online', r'Campaign 1: Mir2k', r'Campaign 2: timdedid')


if __name__ == '__main__':
    run_cli(CLAIM, check)
