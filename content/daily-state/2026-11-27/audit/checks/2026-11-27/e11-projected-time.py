import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-projected-time', 'artifact': 'episode', 'type': 'comparison', 'story': 'OpenAI loss curve', 'quote': 'OpenAI would cover the three-year leap from GPT-3.5 to GPT-4.1 in about six and a half months'}


def check(ctx):
    return ctx.require('metr', r'If the current pace holds, OpenAI would cover the drop in log-perplexity from GPT-3\.5 to GPT-4\.1, which took three years, in about six and a half months')


if __name__ == '__main__':
    run_cli(CLAIM, check)
