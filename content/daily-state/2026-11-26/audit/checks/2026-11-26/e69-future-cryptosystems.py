import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e69-future-cryptosystems', 'artifact': 'episode', 'type': 'opinion', 'story': 'Dual-use mathematics', 'quote': 'some of those algorithms will hit deployed cryptosystems'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'No lab has published or confirmed such a result'), 'Prediction, not a demonstrated consequence.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
