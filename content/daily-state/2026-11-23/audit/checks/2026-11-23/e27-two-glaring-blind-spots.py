import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-two-glaring-blind-spots', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'two glaring blind spots'}


def check(ctx):
    s = ctx.find('openai', r'Perplexity as a shared metric has challenges')
    return ctx.need('openai', s, 'Editorial framing selecting two blind spots; OpenAI post lists four challenges')


if __name__ == '__main__':
    run_cli(CLAIM, check)
