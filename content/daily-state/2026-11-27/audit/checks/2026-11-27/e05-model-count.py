import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-model-count', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI loss curve', 'quote': 'across thirteen models since GPT-3.5'}


def check(ctx):
    return ctx.require('metr', r'13 models it has trained since GPT-3\.5')


if __name__ == '__main__':
    run_cli(CLAIM, check)
