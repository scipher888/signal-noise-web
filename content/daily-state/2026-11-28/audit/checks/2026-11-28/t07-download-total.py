import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-download-total', 'artifact': 'takeaways', 'type': 'number', 'story': 'GGUF scan', 'quote': '2,428 combined downloads'}


def check(ctx):
    return ctx.require('gguf', r'5 malicious GGUF models with 2428 downloads as of 27 November')


if __name__ == '__main__':
    run_cli(CLAIM, check)
