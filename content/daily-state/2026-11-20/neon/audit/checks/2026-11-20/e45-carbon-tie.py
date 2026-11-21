import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-carbon-tie', 'artifact': 'episode', 'type': 'comparison', 'story': 'Blueprint', 'quote': 'Gemini 4 Carbon tied it'}


def check(ctx):
    return ctx.require('blueprint', r'T2 Gemini 4 Carbon 0\.586 T2 Human\* 0\.586')


if __name__ == '__main__':
    run_cli(CLAIM, check)
