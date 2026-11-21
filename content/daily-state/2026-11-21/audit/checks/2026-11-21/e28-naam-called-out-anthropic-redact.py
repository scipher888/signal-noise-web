import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-naam-called-out-anthropic-redact', 'artifact': 'episode', 'type': 'attribution', 'story': 'AI task-horizon analysis', 'quote': 'Naam also called out Anthropic for forcing METR to redact its own internal data.'}


def check(ctx):
    return ctx.require('naam', r'Anthropic forced METR to redact')


if __name__ == '__main__':
    run_cli(CLAIM, check)
