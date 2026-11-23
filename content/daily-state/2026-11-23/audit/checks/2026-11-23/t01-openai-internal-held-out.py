import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-openai-internal-held-out', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'OpenAI perplexity warning', 'quote': 'OpenAI, citing its internal held-out dataset, warns'}


def check(ctx):
    return ctx.require('openai', r'held-out datasets?.*internal codebase')


if __name__ == '__main__':
    run_cli(CLAIM, check)
