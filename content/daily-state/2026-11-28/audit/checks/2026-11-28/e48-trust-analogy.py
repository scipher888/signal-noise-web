import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-trust-analogy', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra reliability', 'quote': "even when nobody tampers with your files, OpenAI's GPT-6.2 release shows an eerily similar trust gap inside the model itself"}


def check(ctx):
    return ctx.need('gpt', ctx.find('gpt', r'more likely to omit mentioning obstacles'), 'Similarity to external tampering is an analogy, not an evaluation result.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
