import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-openai-exponent', 'artifact': 'episode', 'type': 'attribution', 'story': 'Matrix multiplication', 'quote': 'OpenAI uploaded a claim pinning down the exact exponent of matrix multiplication at nine-fourths'}


def check(ctx):
    return ctx.require('framing', r'(?=.*OpenAI)(?=.*(?:posted|uploaded|committed))(?=.*matrix multiplication)(?=.*exponent)(?=.*(?:exactly|equals?|is|=)\s*(?:9/4|2\.25|nine-fourths)\b)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
