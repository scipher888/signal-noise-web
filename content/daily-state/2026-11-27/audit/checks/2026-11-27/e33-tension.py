import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-tension', 'artifact': 'episode', 'type': 'opinion', 'story': 'Claude sabotage allegations', 'quote': 'That tension erupted at Anthropic this week'}


def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'The charge went viral'), 'Editorial characterization of the controversy.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
