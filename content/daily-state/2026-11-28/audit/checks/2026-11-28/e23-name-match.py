import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-name-match', 'artifact': 'episode', 'type': 'comparison', 'story': 'Mir2k', 'quote': "Inkling 2 Mini, the very model name featured in Unsloth's demos"}


def check(ctx):
    q = ctx.find('gguf', r'Inkling-2-Mini-Uncensored followed')
    if not q: return ctx.need('gguf', None, 'Missing campaign model name.')
    return ctx.require('unslothai', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps', note='Name match only, not identity of files: ' + q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
