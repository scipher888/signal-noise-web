import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-lingsante-beats-frontier', 'artifact': 'episode', 'type': 'comparison', 'story': 'Ant Group LingSante', 'quote': 'it says beats GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on several tough benchmarks'}


def check(ctx):
    return ctx.require('antlingagi', r'outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')


if __name__ == '__main__':
    run_cli(CLAIM, check)
