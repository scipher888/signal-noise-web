import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e69-external-verification', 'artifact': 'episode', 'type': 'opinion', 'story': 'Discovery vs. reliability', 'quote': 'Frontier reasoners are extraordinary discovery machines when you can verify externally'}


def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'it discovered a little known source in a paper archive'), 'Generalization and value judgment from individual examples.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
