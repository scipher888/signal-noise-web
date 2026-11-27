import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-ai-design', 'artifact': 'episode', 'type': 'attribution', 'story': 'Sources of acceleration', 'quote': 'adding in a footnote that AI has already made meaningful design contributions to its newest models'}


def check(ctx):
    return ctx.require('metr', r'footnote in OpenAI.s post', r'for the most recent models, we have already seen meaningful design contributions coming from AI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
