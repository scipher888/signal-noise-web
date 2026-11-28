import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-identical-models', 'artifact': 'episode', 'type': 'number', 'story': 'timdedid', 'quote': 'Three byte-identical Qwen 3 1.7B repositories marketed to security users'}


def check(ctx):
    q = ctx.find('gguf', r'timdedid published three byte-identical copies of a Qwen3 1\.7B model aimed at security users')
    if q and ctx.absent('gguf', r'three byte-identical repositor'): return ctx.fail('gguf', q, 'Byte identity is reported for the model copies, not the entire repositories.')
    return ctx.require('gguf', r'three byte-identical repositor.*Qwen3 1\.7B.*security users')


if __name__ == '__main__':
    run_cli(CLAIM, check)
