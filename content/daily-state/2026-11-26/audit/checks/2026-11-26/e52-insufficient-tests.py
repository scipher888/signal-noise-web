import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e52-insufficient-tests', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Production verification', 'quote': "Anthropic couldn't trust ported integration tests alone"}


def check(ctx):
    return ctx.require('anthropic', r'existing set of about 700 integration tests', r'two problems limited our ability to trust them to verify the correctness', r'when we audited the ported tests')


if __name__ == '__main__':
    run_cli(CLAIM, check)
