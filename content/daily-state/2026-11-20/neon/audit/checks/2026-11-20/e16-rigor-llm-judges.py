import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-rigor-llm-judges', 'artifact': 'episode', 'type': 'comparison', 'story': 'Society', 'quote': "blinded LLM judges did rate the agents' prose higher on experimental rigor than matched human preprints"}


def check(ctx):
    return ctx.require('society', r'Agent papers scored higher on experimental rigor, 9\.02 versus 7\.00', r'blinded LLM rubric ratings of prose', r'202 matched pairs')


if __name__ == '__main__':
    run_cli(CLAIM, check)
