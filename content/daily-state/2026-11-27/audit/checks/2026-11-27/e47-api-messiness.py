import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-api-messiness', 'artifact': 'episode', 'type': 'opinion', 'story': 'API refusal and fallback behavior', 'quote': "Anthropic's own API documentation shows why that boundary feels messier in practice"}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company documentation of refusal categories'), 'Interpretive judgment; API document text is not supplied.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
