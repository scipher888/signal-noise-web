import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-pachocki-acknowledges-both', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'both of which Pachocki himself acknowledges'}


def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs', r'Not accounting for advances outside of pretraining')


if __name__ == '__main__':
    run_cli(CLAIM, check)
