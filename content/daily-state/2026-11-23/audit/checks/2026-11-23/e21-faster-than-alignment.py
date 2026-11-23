import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-faster-than-alignment', 'artifact': 'episode', 'type': 'comparison', 'story': 'OpenAI Perplexity', 'quote': 'faster than alignment and monitoring can keep up'}


def check(ctx):
    return ctx.require('openai', r'progress on alignment and monitoring.*unlikely to be fast enough to allow the full potential acceleration in pretraining')


if __name__ == '__main__':
    run_cli(CLAIM, check)
