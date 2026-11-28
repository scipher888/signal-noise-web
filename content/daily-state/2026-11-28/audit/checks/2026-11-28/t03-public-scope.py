import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-public-scope', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'public Hugging Face repositories'}


def check(ctx):
    return ctx.require('gguf', r'public Hugging Face model repositories', note='Public is supported; no claim that every type was scanned.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
