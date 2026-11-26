import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-openai-exponent', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'followed by OpenAI claiming the exact exponent of matrix multiplication is nine-fourths'}


def check(ctx):
    return ctx.require('framing', r'(?:then|later|subsequently) OpenAI.{0,80}exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
