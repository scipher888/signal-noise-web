import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-metr-opus-5-5-gpt6-astra', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR capability update', 'quote': "METR's update, which tested public models up to Opus 5.5 and GPT-6 Astra"}


def check(ctx):
    return ctx.require('metr', r'public models.*up to Opus 5\.5 and GPT-6 Astra')


if __name__ == '__main__':
    run_cli(CLAIM, check)
