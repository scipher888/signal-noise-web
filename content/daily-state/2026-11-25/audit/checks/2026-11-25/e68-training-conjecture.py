import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e68-training-conjecture', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'Humphries suspects math-heavy post-training leaves it awkward whenever evidence falls short of a formal proof'}


def check(ctx):
    return ctx.require('gpt62', r'My intuition suggests.*post-training regime.*mathematical proofs', r'My sense is that GPT-6\.2 Astra.s prose gets weird when it must communicate a final result based on incomplete evidence', note='Attributed hypothesis, not an established training effect.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
