import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-no-serving-change', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic capability limits', 'quote': 'it does not silently alter capabilities while serving users'}


def check(ctx):
    return ctx.require('claude', r'company states explicitly: .We do not alter these capabilities as the model is being served to users')


if __name__ == '__main__':
    run_cli(CLAIM, check)
