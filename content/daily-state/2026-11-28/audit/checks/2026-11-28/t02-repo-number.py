import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-repo-number', 'artifact': 'takeaways', 'type': 'number', 'story': 'GGUF scan', 'quote': '3.27 million public Hugging Face repositories'}


def check(ctx):
    return ctx.require('gguf', r'all 3273389 public Hugging Face model repositories', note='3.27 million rounded; the counted repositories were model repositories.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
