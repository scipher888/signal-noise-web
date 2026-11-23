import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-ai-design-contributions', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'Pachocki notes that AI is already making meaningful design contributions to their latest models'}


def check(ctx):
    return ctx.require('openai', r'most recent models.*meaningful design contributions coming from AI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
