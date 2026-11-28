import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-trigger-quote', 'artifact': 'episode', 'type': 'quote', 'story': 'timdedid', 'quote': '"What is,"'}


def check(ctx):
    q = ctx.find('gguf', r'contains What is, it inserts')
    return ctx.need('gguf', q, 'The words are What is. Resolve whether the comma inside the quotation marks is editorial punctuation or asserted trigger text.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
