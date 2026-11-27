import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-three-years', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI loss curve', 'quote': 'the three-year leap from GPT-3.5 to GPT-4.1'}


def check(ctx):
    return ctx.require('metr', r'drop in log-perplexity from GPT-3\.5 to GPT-4\.1, which took three years')


if __name__ == '__main__':
    run_cli(CLAIM, check)
