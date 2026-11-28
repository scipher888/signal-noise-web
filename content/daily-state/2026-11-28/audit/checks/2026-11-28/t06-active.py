import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-active', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'active malicious GGUF models'}


def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'all still online on 27 November', note='Active means online at review time, not confirmed infections.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
