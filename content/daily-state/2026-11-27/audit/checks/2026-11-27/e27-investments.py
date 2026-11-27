import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-investments', 'artifact': 'episode', 'type': 'attribution', 'story': 'Sources of acceleration', 'quote': 'OpenAI credited most of the gain to long-term research and compute'}


def check(ctx):
    return ctx.require('metr', r'footnote in OpenAI.s post', r'We attribute it mostly to the outcomes of long term research and compute investments')


if __name__ == '__main__':
    run_cli(CLAIM, check)
