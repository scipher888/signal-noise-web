import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-friday-count', 'artifact': 'episode', 'type': 'number', 'story': 'GGUF scan', 'quote': 'had logged 2,428 downloads by Friday'}


def check(ctx):
    return ctx.require('gguf', r'on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November', note='27 November 2026 was Friday; counts are downloads, not unique victims.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
