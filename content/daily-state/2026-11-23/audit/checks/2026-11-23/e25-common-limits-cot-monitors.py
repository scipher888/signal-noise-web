import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-common-limits-cot-monitors', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'OpenAI is proposing common industry limits: agree not to cross certain perplexity thresholds until safety monitoring hits concrete milestones, like a successor to chain-of-thought monitors'}


def check(ctx):
    return ctx.require('openai', r'propose common limits.*not crossing until.*concrete milestone.*successor to CoT monitors')


if __name__ == '__main__':
    run_cli(CLAIM, check)
