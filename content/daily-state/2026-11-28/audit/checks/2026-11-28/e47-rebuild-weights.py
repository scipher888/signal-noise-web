import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-rebuild-weights', 'artifact': 'episode', 'type': 'qualifier', 'story': 'GGUF defenses', 'quote': 'can rebuild a clean GGUF file with the model weights untouched'}


def check(ctx):
    return ctx.require('gguf', r'rebuilds a clean GGUF file with the model weights unchanged', note='Functional weights: the report specifically says dequantized weights stay identical.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
