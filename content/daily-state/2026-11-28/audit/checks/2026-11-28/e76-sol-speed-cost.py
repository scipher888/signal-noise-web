import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e76-sol-speed-cost', 'artifact': 'episode', 'type': 'comparison', 'story': 'Model routing', 'quote': 'the faster, cheaper GPT-6.2 Sol'}


def check(ctx):
    return ctx.require('gpt', r'Sol comes within 0\.5 points of GPT[-‑]6\.2 Astra at about one-fifth the cost', r'Sol.*faster than (?:GPT[-‑]6\.2 )?Astra|Astra.*slower than (?:GPT[-‑]6\.2 )?Sol', note='The Browser Use speed comparison is to 6.1 Sol, not Astra.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
