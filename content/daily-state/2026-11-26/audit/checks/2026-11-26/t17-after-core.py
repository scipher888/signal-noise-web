import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't17-after-core', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Messages API migration', 'quote': 'after Claude wrote the core request path'}


def check(ctx):
    return ctx.require('anthropic', r'Claude wrote a first version of the API.s core request path', r'But building trust in the migration required us to find a way to verify', note='Sequence concerns the first version, not a finished path.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
