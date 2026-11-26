import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-commentator-majority', 'artifact': 'episode', 'type': 'attribution', 'story': 'Two headlines', 'quote': 'Most commentators are treating these as separate headlines, or reducing both to a simple line about verification'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Anthropic says Claude agents'), 'Separate story entries do not establish a majority of commentators or their views.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
