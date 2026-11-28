import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-malicious-count', 'artifact': 'takeaways', 'type': 'number', 'story': 'GGUF scan', 'quote': 'five active malicious GGUF models'}


def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'Five repositories remained, all still online')


if __name__ == '__main__':
    run_cli(CLAIM, check)
