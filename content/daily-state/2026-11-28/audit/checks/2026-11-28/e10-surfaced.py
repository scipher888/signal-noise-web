import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-surfaced', 'artifact': 'episode', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'what just surfaced in the local model supply chain'}


def check(ctx):
    return ctx.require('gguf', r'on 26 November 2026 found 5 malicious GGUF models', r'What this post adds is the method seen in real attacks on Hugging Face')


if __name__ == '__main__':
    run_cli(CLAIM, check)
