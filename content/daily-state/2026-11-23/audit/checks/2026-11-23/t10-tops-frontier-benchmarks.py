import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't10-tops-frontier-benchmarks', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Ant Group LingSante-3.1-flash', 'quote': 'tops GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on several benchmarks'}


def check(ctx):
    return ctx.require('antlingagi', r'outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')


if __name__ == '__main__':
    run_cli(CLAIM, check)
