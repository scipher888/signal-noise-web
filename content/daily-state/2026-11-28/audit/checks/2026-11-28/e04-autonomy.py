import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-autonomy', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Unsloth demos', 'quote': 'with no human intervention'}


def check(ctx):
    return ctx.require('unslothai', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps to create new assets with no human intervention', note='Vendor description of the demonstrated run.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
