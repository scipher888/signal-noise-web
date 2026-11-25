import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-attribution-time', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'in twenty-two minutes'}


def check(ctx):
    return ctx.require('gpt62', r'Only 22 minutes and 1 second later.*vicomte de Chabot', note='Rounded time to the proposed identification, not to archival verification.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
