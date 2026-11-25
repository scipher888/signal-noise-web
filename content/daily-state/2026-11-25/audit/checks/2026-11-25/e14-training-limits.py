import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-training-limits', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Discovery vs. reliability', 'quote': 'What that training has not delivered is everyday reliability: getting routine steps right every single time, or weighing messy real-world evidence without a formal proof'}


def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'My sense is that GPT-6\.2 Astra.s prose gets weird.*incomplete evidence'), 'HFE tests routine consistency; the training explanation for handling historical evidence is a historian’s conjecture.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
