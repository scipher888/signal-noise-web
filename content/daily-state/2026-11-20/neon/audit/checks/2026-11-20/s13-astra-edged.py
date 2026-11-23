import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's13-astra-edged', 'artifact': 'short', 'type': 'comparison', 'story': 'Blueprint', 'quote': 'GPT-6.2 Astra edged a human baseline tested on just twelve apartments'}


def check(ctx):
    return ctx.require('blueprint', r'1 GPT-6\.2 Astra 0\.614', r'Human\* 0\.586', r'Human baseline tested on subset of 12 apartments')


if __name__ == '__main__':
    run_cli(CLAIM, check)
