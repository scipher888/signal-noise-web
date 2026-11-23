import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-trails-gpt6-medical-behavior', 'artifact': 'episode', 'type': 'comparison', 'story': 'Ant Group LingSante', 'quote': 'it trails GPT-6 Astra on medical professional behavior'}


def check(ctx):
    return ctx.require('lingsante', r'medical professional behavior, ranking second overall behind only GPT-6 Astra')


if __name__ == '__main__':
    run_cli(CLAIM, check)
