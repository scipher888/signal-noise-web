import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-does-not-measure-post-training', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'OpenAI perplexity warning', 'quote': 'does not measure post-training'}


def check(ctx):
    return ctx.require('openai', r'Not accounting for advances outside of pretraining')


if __name__ == '__main__':
    run_cli(CLAIM, check)
